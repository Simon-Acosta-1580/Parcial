from sqlmodel import SQLModel, Field, Relationship

class CategoriaBase(SQLModel):
    nombre: str | None = Field(description="Nombre de la categoria")
    descripcion: str | None = Field(description="Descripcion de la categoria")

class ProductoBase(SQLModel):
    nombre: str | None = Field(description="Nombre de la producto")
    precio: float | None = Field(description="Precio de la producto")
    stock: float | None = Field(description="Stock de la producto")
    descripcion: str | None = Field(description="Descripcion de la producto")

class Categorias(CategoriaBase, Table= True):
    id: int | None = Field(default = None, primary_key=True)
    productos: list["Producto"] = Relationship(back_populates="categoria")

class Producto(ProductoBase, Table= True):
    id: int | None = Field(default = None, primary_key=True)
    categoria: Categorias = Relationship(back_populates="productos")