from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Producto,ProductoBase, ProductoCreate, Categoria

router = APIRouter()

@router.post("/productos/", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, session: SessionDep):
    query = select(Producto).where(Producto.nombre == producto.nombre)
    existente = session.exec(query).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre.")

    if producto.stock is not None and producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo.")

    if producto.precio is not None and producto.precio < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo.")

    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="La categoría asociada no existe.")
    if not categoria.status:
        raise HTTPException(status_code=400, detail="La categoría asociada está inactiva.")

    nuevo_producto = Producto.model_validate(producto)
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)

    return nuevo_producto

@router.get("/", response_model=list[Producto])
async def listar_productos(session: SessionDep):
    query = select(Producto).where(Producto.status == True)
    productos = session.exec(query).all()

    if not productos:
        raise HTTPException(status_code=404, detail="No hay productos activos registrados")

    return productos

@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto_con_categoria(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.categoria_id:
        categoria = session.get(Categoria, producto.categoria_id)
        producto.categoria = categoria

    return producto

@router.get("/nombre/{nombre_producto}", response_model=Producto)
async def obtener_producto_por_nombre(nombre_producto: str, session: SessionDep):
    query = select(Producto).where(Producto.nombre.ilike(nombre_producto))
    producto = session.exec(query).first()

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.categoria_id:
        producto.categoria = session.get(Categoria, producto.categoria_id)

    return producto


@router.put("/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: int, datos: ProductoBase, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if datos.nombre:
        query = select(Producto).where(
            Producto.nombre == datos.nombre,
            Producto.id != producto_id
        )
        existente = session.exec(query).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")

    if datos.stock is not None and datos.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

    if datos.categoria_id:
        categoria = session.get(Categoria, datos.categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(producto, key, value)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

@router.patch("/{producto_id}/desactivar", response_model=Producto)
async def desactivar_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.status:
        raise HTTPException(status_code=400, detail="El producto ya está inactivo")

    producto.status = False
    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto

@router.patch("/{producto_id}/activar", response_model=Producto)
async def activar_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.status:
        raise HTTPException(status_code=400, detail="El producto ya está activo")

    if producto.categoria_id:
        categoria = session.get(Categoria, producto.categoria_id)
        if categoria and not categoria.status:
            raise HTTPException(status_code=400, detail="No se puede activar el producto porque su categoría está inactiva")

    producto.status = True
    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto

@router.patch("/{producto_id}/restar_stock", response_model=Producto)
async def restar_stock(producto_id: int, cantidad: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.status:
        raise HTTPException(status_code=400, detail="No se puede modificar el stock de un producto inactivo")

    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad a restar debe ser mayor a 0")

    if producto.stock - cantidad < 0:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Solo hay {producto.stock} unidades disponibles")

    producto.stock -= cantidad
    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto
