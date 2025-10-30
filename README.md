
<h1> Parcial corte 2 desarrollo de software — Sistema de Gestión de Categorías y Productos</h1>

<h2>Descripción General</h2>
<p>Este proyecto implementa una interfaz de programacion de aplicaciones desarrollada con <strong>FastAPI</strong> y <strong>SQLModel</strong>, con el proposito de generar <strong>categorías</strong> y <strong>productos</strong> dentro de un contexto empresarial o comercial.</p>
<p>Incluye relaciones entre modelos, persistencia de datos, validaciones lógicas y generación automática de la base de datos.</p>

<hr>

<h2>Tecnologías Utilizadas</h2>
<ul>
<li>Python 3.11+</li>
<li>FastAPI — Framework backend principal</li>
<li>SQLModel — ORM que combina lo mejor de Pydantic y SQLAlchemy</li>
<li>Uvicorn — Servidor ASGI</li>
<li>SQLite / PostgreSQL / MySQL — Motores configurables</li>
</ul>

<hr>

<h2>Estructura del Proyecto</h2>
<pre>
ProyectoIntegrador/
├── main.py
├── db.py
├── models.py
├── categoria.py
├── producto.py
└── README.md
</pre>

<hr>

<h2>⚙️ Configuración del Entorno</h2>
<ol>
<li>Clonar el repositorio:<br><code>git clone https://github.com/Simon-Acosta-1580/Parcial.git</code></li>
<li>Crear entorno virtual:<br><code>python -m venv .venv</code></li>
<li>Activar entorno virtual:<br><code>.venv\Scripts\activate</code> (Windows) <br><code>.venv\bin\activate</code>(mac)</li>
<li>Instalar dependencias:<br><code>pip install -r requirements.txt</code></li>
<li>Ejecutar servidor:<br><code>fastapi dev</code></li>
</ol>

<p>Interfaz interactiva disponible en: <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a></p>

<hr>

<h2>Endpoints Principales</h2>

<h3>Categorías</h3>
<table>
<tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
<tr><td>POST</td><td>/categorias/</td><td>Crear nueva categoría</td></tr>
<tr><td>GET</td><td>/categorias/</td><td>Listar categorías activas</td></tr>
<tr><td>GET</td><td>/categorias/{id}</td><td>Obtener categoría por ID (con productos)</td></tr>
<tr><td>PATCH</td><td>/categorias/{id}/desactivar</td><td>Desactivar categoría y productos</td></tr>
<tr><td>PATCH</td><td>/categorias/{id}/activar</td><td>Reactivar categoría y productos</td></tr>
</table>

<h3>Productos</h3>
<table>
<tr><th>Método</th><th>Endpoint</th><th>Descripción</th></tr>
<tr><td>POST</td><td>/productos/</td><td>Crear nuevo producto</td></tr>
<tr><td>GET</td><td>/productos/</td><td>Listar productos activos</td></tr>
<tr><td>PATCH</td><td>/productos/{id}/restar_stock/{cantidad}</td><td>Restar stock del producto</td></tr>
</table>

<hr>

<h2>Lógica de Negocio Implementada</h2>
<ul>
<li>No se permiten nombres duplicados</li>
<li>Stock no negativo</li>
<li>Desactivar una categoría desactiva sus productos</li>
<li>Reactivar categoría reactiva productos</li>
<li>Soporte de búsqueda por nombre</li>
</ul>

<hr>
