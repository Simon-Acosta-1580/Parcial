from db import SessionDep
from fastapi import APIRouter, HTTPException
from models import Categoria, CategoriaBase

router = APIRouter()

@router.post("/", response_model=Categoria, status_code=201)
async def create_categoria(nueva_categoria: CategoriaBase, session: SessionDep):
    categoria = Categoria.model_validate(nueva_categoria)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
