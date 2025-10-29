from db import SessionDep
from fastapi import APIRouter, HTTPException
from models import Categoria, CategoriaBase
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Categoria, status_code=201)
async def create_categoria(nueva_categoria: CategoriaBase, session: SessionDep):
    query = select(Categoria).where(Categoria.nombre == nueva_categoria.nombre)
    existente = session.exec(query).first()

    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre.")

    categoria = Categoria.model_validate(nueva_categoria)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.get("/", response_model=list[Categoria])
async def listar_categorias_activas(session: SessionDep):
    query = select(Categoria).where(Categoria.status == True)
    categorias = session.exec(query).all()
    return categorias

@router.get("/{categoria_id}", response_model=Categoria)
async def obtener_categoria_con_productos(categoria_id: int, session: SessionDep):
    query = select(Categoria).where(Categoria.id == categoria_id)
    categoria = session.exec(query).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    _ = categoria.productos

    return categoria

@router.put("/{categoria_id}", response_model=Categoria)
async def actualizar_categoria(categoria_id: int, datos: CategoriaBase, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    if datos.nombre:
        query = select(Categoria).where(
            Categoria.nombre == datos.nombre,
            Categoria.id != categoria_id
        )
        existente = session.exec(query).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre.")

    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(categoria, key, value)

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.patch("/{categoria_id}/desactivar", response_model=Categoria)
async def desactivar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    if not categoria.status:
        raise HTTPException(status_code=400, detail="La categoría ya está inactiva.")

    categoria.status = False
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.patch("/categorias/{categoria_id}/activar")
def activar_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    categoria.status = True
    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return {"message": "Categoría activada correctamente"}
