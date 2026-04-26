# Trazabilidad del Proyecto — secure-fastapi-api

**Fecha de corte:** 21 de abril de 2026  
**Repositorio:** [YagoGomez83/secure-fastapi-api](https://github.com/YagoGomez83/secure-fastapi-api)  
**Rama activa:** `main`

---

## ¿Qué es este proyecto?

Una API REST construida con **FastAPI** que sigue una arquitectura en capas limpia. Está diseñada con buenas prácticas de seguridad, soporte para Docker y una estructura lista para extender con nueva funcionalidad.

---

## Stack tecnológico usado

| Capa | Tecnología |
|---|---|
| Framework | FastAPI 0.136 + Uvicorn |
| Validación | Pydantic v2 + pydantic-settings |
| Base de datos | SQLAlchemy 2.0 · PostgreSQL (psycopg2) · SQLite async (aiosqlite) |
| Seguridad | bcrypt · Argon2 · Passlib · Bandit |
| Testing | Pytest · pytest-asyncio · pytest-cov |
| Contenedores | Docker · Docker Compose |

---

## Estructura de carpetas

```
secure-fastapi-api/
├── app/
│   ├── main.py                     # Punto de entrada de la aplicación
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── user.py         # Endpoints de usuarios
│   ├── core/
│   │   ├── config.py               # Configuración via pydantic-settings
│   │   ├── logging.py              # (placeholder — pendiente implementar)
│   │   └── security.py             # (placeholder — pendiente implementar)
│   ├── models/
│   │   └── user.py                 # (placeholder — modelo SQLAlchemy pendiente)
│   ├── schemas/
│   │   └── user.py                 # (placeholder — schemas Pydantic pendientes)
│   ├── repositories/
│   │   └── user_repository.py      # (placeholder — acceso a datos pendiente)
│   └── services/
│       └── user_service.py         # (placeholder — lógica de negocio pendiente)
├── tests/
│   └── test_users.py               # Tests básicos (health + users)
├── docs/
│   └── trazabilidad/
│       └── resumen_proyecto.md     # Este archivo
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Lo que está implementado y funcionando

### 1. Punto de entrada — `app/main.py`
- Crea la instancia de FastAPI con título y modo debug desde config.
- Define el endpoint `GET /health` que devuelve `{ "status": "ok", "env": "dev" }`.
- Registra el router de usuarios bajo el prefijo `/api/v1`.

### 2. Configuración — `app/core/config.py`
- Usa `pydantic-settings` para cargar variables de entorno desde un archivo `.env`.
- Variables disponibles: `APP_NAME`, `APP_ENV`, `APP_PORT`, `DEBUG`.
- Expone un objeto singleton `settings` que se importa en toda la app.

### 3. Endpoints de usuario — `app/api/v1/endpoints/user.py`
- `GET /api/v1/users` → devuelve una lista hardcodeada de 2 usuarios (datos mock).
- `GET /api/v1/users/{user_id}` → valida que el ID sea positivo; si no, lanza `HTTPException 400`.

### 4. Dockerfile
- Imagen base: `python:3.12-slim`.
- Crea un usuario no-root (`appuser`) para ejecutar la app — buena práctica de seguridad.
- Copia `requirements.txt` antes del código para aprovechar el caché de capas de Docker.
- Expone el puerto 8000.

### 5. Docker Compose — `docker-compose.yml`
- Levanta el servicio `api` con el puerto `8001:8000`.
- Carga variables desde `.env`.
- Política de restart: `unless-stopped`.

### 6. Tests — `tests/test_users.py`
- `test_health()` → verifica que `GET /health` devuelva HTTP 200.
- `test_users()` → verifica que `GET /api/v1/users` devuelva HTTP 200.
- Usa `TestClient` de FastAPI (basado en httpx).

---

## Lo que está estructurado pero pendiente de implementar

Estos archivos existen pero están vacíos. Representan las capas de la arquitectura que aún no tienen código:

| Archivo | Propósito futuro |
|---|---|
| `app/core/security.py` | Hashing de contraseñas con bcrypt/Argon2, generación de tokens JWT |
| `app/core/logging.py` | Configuración centralizada de logs |
| `app/models/user.py` | Modelo SQLAlchemy para la tabla `users` en la base de datos |
| `app/schemas/user.py` | Schemas Pydantic para validar requests y serializar responses |
| `app/repositories/user_repository.py` | Queries a la base de datos (CRUD de usuarios) |
| `app/services/user_service.py` | Lógica de negocio (ej: crear usuario, verificar contraseña) |

---

## Flujo de datos (arquitectura en capas)

```
Request HTTP
    ↓
[Endpoint]  app/api/v1/endpoints/user.py
    ↓
[Service]   app/services/user_service.py     ← lógica de negocio
    ↓
[Repository] app/repositories/user_repository.py  ← acceso a datos
    ↓
[Model]     app/models/user.py               ← tabla en DB (SQLAlchemy)
    ↓
[Database]  PostgreSQL / SQLite
```

Actualmente los endpoints responden directamente con datos mock, sin pasar por las capas inferiores.

---

## Dependencias clave en `requirements.txt`

| Paquete | Para qué sirve |
|---|---|
| `fastapi` | Framework principal |
| `uvicorn` | Servidor ASGI para correr FastAPI |
| `pydantic` / `pydantic-settings` | Validación y configuración |
| `sqlalchemy` | ORM para base de datos |
| `psycopg2-binary` | Driver PostgreSQL |
| `aiosqlite` | Driver SQLite async (para tests/dev) |
| `bcrypt` | Hashing de contraseñas |
| `argon2-cffi` | Hashing moderno de contraseñas |
| `passlib` | Abstracción para algoritmos de hashing |
| `bandit` | Análisis estático de seguridad en código Python |
| `pytest` / `pytest-cov` | Testing y cobertura |

---

## Comandos útiles

```bash
# Correr la app localmente
uvicorn app.main:app --reload

# Correr con Docker
docker-compose up --build

# Ejecutar tests
pytest

# Tests con cobertura
pytest --cov=app --cov-report=term-missing

# Análisis de seguridad estática
bandit -r app/
```

---

## Próximos pasos sugeridos

1. Implementar `app/models/user.py` con SQLAlchemy (tabla `users` con id, username, email, hashed_password).
2. Implementar `app/schemas/user.py` con Pydantic (schemas `UserCreate`, `UserResponse`).
3. Implementar `app/repositories/user_repository.py` (CRUD real contra la DB).
4. Implementar `app/services/user_service.py` (crear usuario, hashear contraseña).
5. Implementar `app/core/security.py` (hash con Argon2/bcrypt, JWT tokens).
6. Conectar los endpoints a las capas reales en lugar de datos mock.
7. Añadir autenticación (OAuth2 + JWT) a los endpoints protegidos.
8. Expandir los tests para cubrir las nuevas capas.
