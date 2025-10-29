from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Producto, ProductoCreate, Categoria

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