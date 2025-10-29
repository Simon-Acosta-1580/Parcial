from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class CategoriaBase(SQLModel):
    nombre: str = Field(index=True, description="Nombre de la categoría", unique=True)
    descripcion: Optional[str] = Field(default=None, description="Descripción de la categoría")
    status: bool = Field(default=True, description="Activo o inactivo")


class ProductoBase(SQLModel):
    nombre: str = Field(index=True, description="Nombre del producto")
    precio: float = Field(default=0, description="Precio del producto")
    stock: int = Field(default=0, ge=0, description="Cantidad en stock (no negativos)")
    descripcion: Optional[str] = Field(default=None, description="Descripción del producto")
    status: bool = Field(default=True, description="Activo o inactivo")
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="categoria")


class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categoria: Optional[Categoria] = Relationship(back_populates="productos")


class CategoriaCreate(CategoriaBase):
    pass


class ProductoCreate(ProductoBase):
    categoria_id: int = Field(foreign_key="categoria.id")
