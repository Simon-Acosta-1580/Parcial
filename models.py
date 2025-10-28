from sqlmodel import SQLModel, Field, Relationship

class CategoriaBase(SQLModel):
    nombre: str | None = Field(description="Nombre de la categoria")
    descripcion: str | None = Field(description="Descripcion de la categoria")

class ProductosBase(SQLModel):
    nombre: str | None = Field(description="Nombre de la producto")
    precio: float | None = Field(description="Precio de la producto")
    stock: float | None = Field(description="Stock de la producto")
    descripcion: str | None = Field(description="Descripcion de la producto")

