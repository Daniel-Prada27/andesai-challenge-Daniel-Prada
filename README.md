# Mini API Restaurante

## Descripción breve
Este proyecto es una **API REST desarrollada con FastAPI** para gestionar los productos y órdenes de un restaurante. 
Permite realizar operaciones CRUD sobre los **items** (productos del inventario) y procesar **órdenes de compra**, además de consultar un **indicador de rendimiento (KPI)**.

La información se persiste en archivos `.csv`, lo que facilita su visualización y portabilidad sin depender de una base de datos externa.

---

## Stack y librerías utilizadas

**Lenguaje:**  
- Python 3.12.3

**Framework principal:**  
- [FastAPI](https://fastapi.tiangolo.com/) – para crear la API REST.

**Dependencias principales:**  
- `pandas` – para manejar los archivos CSV.  
- `python-dotenv` – para cargar las variables de entorno desde `.env`.  
- `uvicorn` – servidor ASGI para ejecutar la aplicación.  

**Infraestructura:**  
- Docker – para empaquetar y ejecutar el servicio de forma portable.

---

## Instrucciones para ejecutar el contenedor

### 1. Clonar el repositorio
```bash
git clone https://github.com/Daniel-Prada27/andesai-challenge-Daniel-Prada.git
cd andesai-challenge-Daniel-Prada 
```

### 2️. Crear la imagen Docker
```bash
docker build -t mini-api-restaurante .
```

### 3️. Ejecutar el contenedor
```bash
docker run -p 8000:8000 mini-api-restaurante
```

El servidor quedará disponible en:
```
http://localhost:8000
```

---

## Ejemplos de requests con `curl`

### Crear un nuevo ítem
```bash
curl -X POST "http://localhost:8000/items" -H "Content-Type: application/json" -d '{"sku": "010", "name": "Maracuyá", "stock": 20, "unit_cost": 200.0}'
```

### Listar ítems
```bash
curl "http://localhost:8000/items"
```

### Crear una orden
```bash
curl -X POST "http://localhost:8000/orders" -H "Content-Type: application/json" -d '{
  "order_id": "001",
  "items": [
    {"sku": "001", "qty": 2},
    {"sku": "005", "qty": 1}
  ]
}'
```

### Listar órdenes
```bash
curl "http://localhost:8000/orders"
```

### Actualizar items
```bash
curl -X PUT http://localhost:8000/items/005 \
-H "Content-Type: application/json" \
-d '{
  "sku": "005",
  "name": "Pescado",
  "stock": 75,
  "unit_cost": 60.0
}'
```

### Eliminar items
```bash
curl -X DELETE http://localhost:8000/items/010
```

### Consultar KPI
```bash
curl "http://localhost:8000/kpi/stock-coverage"
```
```bash
curl "http://localhost:8000/kpi/stock-coverage?days=10"
```
Por defecto, `days=7`

---

## Limitaciones o posibles mejoras
- Actualmente los datos se guardan en archivos CSV; podría integrarse una base de datos (PostgreSQL o SQLite) para mayor escalabilidad.
- No hay autenticación implementada; se podría añadir JWT o API Keys.
- No hay validación avanzada de errores o logs estructurados.
- La API no incluye tests automatizados, lo cual sería recomendable agregar.
- No se realiza paginación, sería bueno agregarla para reducir la carga en el servidor y la red.
- Hace falta establecer los codigos de estado HTTP adecuados para cada respuesta.
- Las respuestas no incluyen links a recursos relacionados, los cuales faciliten al cliente navegar por la api.
- Todas las operaciones se realizan de manera sincrónica; para escalar la api, habría que realizar una implementación asincrónica.

---

## Autor
Desarrollado por **Daniel Prada** – Proyecto Mini API Restaurante (2025)
