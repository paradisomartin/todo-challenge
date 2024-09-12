# API de Lista de Tareas

Este proyecto proporciona una API RESTful para gestionar tareas y etiquetas en una aplicación de lista de tareas.

## Características

- Autenticación de usuario usando JWT
- Operaciones CRUD para tareas
- Operaciones CRUD para etiquetas
- Filtrado, búsqueda y ordenación de tareas

## Endpoints de la API

### Tareas

- `GET /api/tasks/`: Listar todas las tareas del usuario autenticado
- `POST /api/tasks/`: Crear una nueva tarea
- `GET /api/tasks/{id}/`: Obtener una tarea específica
- `PUT /api/tasks/{id}/`: Actualizar una tarea específica
- `DELETE /api/tasks/{id}/`: Eliminar una tarea específica

## Filtrado y Búsqueda de Tareas

Las tareas pueden ser filtradas, buscadas y ordenadas usando los siguientes parámetros en la URL:

- Búsqueda por título o descripción: `?search=palabra_clave`
- Ordenar por fecha de creación: `?ordering=created_at` o `?ordering=-created_at` (descendente)
- Ordenar por título: `?ordering=title` o `?ordering=-title` (descendente)
- Filtrar por rango de fechas:
  - Desde: `?created_after=YYYY-MM-DD`
  - Hasta: `?created_before=YYYY-MM-DD`
- Filtrar por etiqueta: `?tags__title=nombre_etiqueta`

### Etiquetas

- `GET /api/tags/`: Listar todas las etiquetas del usuario autenticado
- `POST /api/tags/`: Crear una nueva etiqueta
- `GET /api/tags/{id}/`: Obtener una etiqueta específica
- `PUT /api/tags/{id}/`: Actualizar una etiqueta específica
- `DELETE /api/tags/{id}/`: Eliminar una etiqueta específica

## Configuración y Ejecución

### Requisitos Previos

- Docker
- Docker Compose

### Pasos para Ejecutar

1. Clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   cd <directorio-del-proyecto>
   ```

2. Copiar el archivo de entorno:
   ```
   cp .env.example .env
   ```

3. Editar el archivo `.env` con la configuración deseada.

4. Construir las imágenes de Docker:
   ```
   docker-compose build
   ```

5. Iniciar los servicios:
   ```
   docker-compose up -d
   ```

La API debería estar ahora en funcionamiento y accesible en `http://localhost:8000`.

## Gestión del Proyecto con Docker

Para facilitar la gestión del proyecto usando Docker, hemos creado un script de shell que simplifica la ejecución de comandos comunes de Django. Este script, `manage.sh`, se encuentra en la raíz del proyecto.

### Uso del Script de Gestión

Asegúrate de que el script tenga permisos de ejecución:

```bash
chmod +x manage.sh
```

Puedes usar el script de la siguiente manera:

- Crear migraciones:
  ```
  ./manage.sh makemigrations
  ```

- Aplicar migraciones:
  ```
  ./manage.sh migrate
  ```

- Crear un superusuario:
  ```
  ./manage.sh createsuperuser
  ```

- Ejecutar pruebas:
  ```
  ./manage.sh test
  ```

- Abrir el shell de Django:
  ```
  ./manage.sh shell
  ```

### Ejemplos de Uso

1. Para crear migraciones para una app específica:
   ```
   ./manage.sh makemigrations tasks
   ```

2. Para ejecutar pruebas de una app específica:
   ```
   ./manage.sh test tasks
   ```

3. Para aplicar una migración específica:
   ```
   ./manage.sh migrate tasks 0001
   ```

## Desarrollo

Para propósitos de desarrollo, establece `DEVELOPMENT=True` en tu archivo `.env` para habilitar CORS para el desarrollo frontend local.

## Pruebas

Ejecuta las pruebas usando:
```
docker-compose run backend python manage.py test
```
