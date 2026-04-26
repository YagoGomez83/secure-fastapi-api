# Secure FastAPI DevSecOps API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![CI/CD](https://github.com/YagoGomez83/secure-fastapi-api/actions/workflows/ci.yml/badge.svg)
![Security](https://img.shields.io/badge/Security-SAST%20%7C%20SCA-red)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Una API REST construida con **FastAPI** diseñada desde cero con mentalidad **DevSecOps**. Este proyecto no solo expone endpoints, sino que demuestra la implementación de arquitectura limpia, seguridad por diseño, observabilidad y un pipeline de integración continua robusto listo para producción.

---

## Enfoque DevSecOps (Por qué este proyecto destaca)

Este repositorio es una prueba de concepto de habilidades reales en ingeniería de seguridad y backend:

- **Autenticación Robusta:** Implementación de JWT (Stateless) y contraseñas hasheadas con **Argon2id** (resistente a memoria), mitigando ataques de tiempo (User Enumeration).
- **Observabilidad Nivel Producción:** Logging estructurado en **JSON** y trazabilidad de peticiones mediante **Correlation IDs** usando `contextvars` (listo para ELK Stack/Splunk).
- **Seguridad en CI/CD:** Pipeline de GitHub Actions que incluye análisis estático (SAST con Bandit), análisis de composición (SCA con Safety) y escaneo de contenedores (Trivy).
- **Contenedores Seguros (Hardening):** Ejecución como usuario no-root (`appuser`), optimización de caché y gestión segura de variables de entorno.
- **Arquitectura Limpia:** Separación estricta de responsabilidades (Endpoints → Services → Repositories → Models) usando Inyección de Dependencias.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Framework Core | FastAPI 0.136 + Uvicorn |
| Validación & Config | Pydantic v2 + pydantic-settings |
| ORM & Base de Datos | SQLAlchemy 2.0 · PostgreSQL (psycopg2) · SQLite (Desarrollo) |
| Seguridad (Auth) | Argon2 (argon2-cffi) · JWT (python-jose) |
| Observabilidad | JSON Logging + UUID Correlation IDs (`contextvars`) |
| Testing | Pytest · httpx (TestClient) · pytest-cov |
| CI/CD Pipeline | GitHub Actions · Bandit (SAST) · Safety (SCA) · Trivy |

---

## Arquitectura de Carpetas

```text
secure-fastapi-api/
├── .github/workflows/         # Pipeline CI/CD (SAST, SCA, Docker Build)
├── app/
│   ├── api/v1/endpoints/
│   │   ├── auth.py            # Login, Registro, Refresh
│   │   └── user.py            # Endpoints de recursos
│   ├── core/
│   │   ├── config.py          # Gestión de secretos (.env)
│   │   ├── logging.py         # Formateador JSON y ContextVars
│   │   └── security.py        # Hashing (Argon2) y JWT
│   ├── models/                # Entidades SQLAlchemy
│   ├── repositories/          # Acceso a base de datos
│   ├── schemas/               # Validaciones Pydantic
│   └── services/              # Lógica de negocio core
├── tests/                     # Suite de pruebas Pytest
├── Dockerfile                 # Construcción segura en capas (Non-root)
└── docker-compose.yml         # Orquestación local
```

---

## Empezando (Getting Started)

### Requisitos Previos

- Python 3.12+
- Docker & Docker Compose (Recomendado)

### Despliegue con Docker (La forma rápida y segura)

```bash
docker-compose up --build
```

*La API estará disponible en `http://localhost:8001`*

### Instalación Local (Para Desarrollo)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/YagoGomez83/secure-fastapi-api.git
   cd secure-fastapi-api
   ```

2. Crear entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar el entorno (Nunca subas el `.env` real):
   ```bash
   cp .env.example .env
   ```

4. Ejecutar el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Referencia de la API

La documentación interactiva se autogenera gracias a OpenAPI:

- **Swagger UI:** `http://localhost:8000/docs` (o puerto 8001 en Docker)
- **ReDoc:** `http://localhost:8000/redoc`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Estado de la API y entorno |
| `POST` | `/api/v1/auth/register` | Registro de usuario |
| `POST` | `/api/v1/auth/login` | Login y obtención de JWT |
| `GET` | `/api/v1/users` | Listar todos los usuarios |
| `GET` | `/api/v1/users/{user_id}` | Obtener usuario por ID |

---

## Pruebas y Cobertura

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## Seguridad

- Contraseñas hasheadas con **Argon2id** (resistente a ataques de memoria)
- Autenticación stateless con **JWT**
- Análisis estático con **Bandit** (SAST) en cada push
- Análisis de dependencias con **Safety** (SCA)
- Escaneo de vulnerabilidades en contenedor con **Trivy**
- Imagen Docker ejecutada como **usuario no-root**
- Toda la configuración cargada desde variables de entorno — sin secretos hardcodeados
- Validación de entrada con **Pydantic v2** en todos los request bodies

---

## Licencia

MIT © [YagoGomez83](https://github.com/YagoGomez83)
