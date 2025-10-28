from db import SessionDep
from fastapi import APIRouter
from models import Categoria, CategoriaBase
from sqlmodel import select

router = APIRouter()

@router.post("/", response_model=Categoria, status_code=201)
async def create_categoria(nueva_categoria: CategoriaBase, session: SessionDep):
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
