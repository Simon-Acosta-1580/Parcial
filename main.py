from fastapi import FastAPI
import Categorias
import Productos
from db import create_tables

app = FastAPI(lifespan=create_tables, title="Tienda API")
app.include_router(Categorias.router, tags=["Categorias"], prefix="/categorias")
app.include_router(Productos.router, tags=["Productos"], prefix="/products")


