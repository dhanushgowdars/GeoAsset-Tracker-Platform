# 🌍 GeoAsset Tracker Platform

> **Enterprise-grade Geospatial Asset Management REST API built with FastAPI, PostgreSQL & PostGIS**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![PostGIS](https://img.shields.io/badge/PostGIS-Geospatial-brightgreen)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![Pytest](https://img.shields.io/badge/Pytest-Tested-yellow)
![License](https://img.shields.io/badge/License-MIT-orange)
![Backend](https://img.shields.io/badge/Backend-Complete-success)
![Frontend](https://img.shields.io/badge/Frontend-In%20Progress-lightgrey)

GeoAsset Tracker Platform is a production-style backend application that enables organizations to register, manage, and track physical assets — such as vehicles, drones, IoT sensors, and field equipment — using real-time geospatial data.

It provides secure JWT-based authentication, role-based authorization, RESTful APIs, geospatial search powered by PostGIS, Dockerized deployment, and integration testing with Pytest — all built on a layered architecture (API → Service → Repository → Database) for clean, scalable, maintainable code.

**Current status:** the backend is fully implemented and tested. A dashboard frontend is planned next — see [Planned Frontend](#planned-frontend-roadmap).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
  - [Architecture Diagram](#architecture-diagram)
  - [Request Lifecycle](#request-lifecycle)
- [Authentication Flow](#authentication-flow)
- [Geospatial Capabilities](#geospatial-capabilities)
- [Database Design](#database-design)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
  - [Running the Application](#running-the-application)
- [Testing](#testing)
- [Planned Frontend (Roadmap)](#planned-frontend-roadmap)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [Author](#author)
- [License](#license)

---

## Overview

This project was built to demonstrate production-style backend engineering using FastAPI and geospatial technologies — scalable architecture, secure authentication, clean code organization, and efficient spatial queries, the kind of concepts used in real-world fleet management, logistics, and asset-tracking systems.

| | |
|---|---|
| **Backend Framework** | FastAPI |
| **Language** | Python 3.11+ |
| **Database** | PostgreSQL + PostGIS |
| **Authentication** | JWT |
| **Testing** | Pytest |
| **Architecture** | Layered (API → Service → Repository → DB) |
| **Containerization** | Docker + Docker Compose |
| **Frontend** | Planned (see roadmap below) |

---

## Features

### 🔐 Authentication & Security
- JWT-based authentication
- Secure password hashing
- Role-based authorization (RBAC)
- Protected REST endpoints

### 📦 Asset Management
- Register new assets
- Update asset information
- Delete assets
- Retrieve asset details

### 🌍 Geospatial Features
- Find nearby assets within a radius
- Locate the nearest asset to a point
- Calculate distance between assets
- Bounding box search
- Geofence search using polygons (PostGIS)

### 🗄️ Database
- PostgreSQL
- PostGIS spatial extension
- SQLAlchemy ORM
- Alembic database migrations

### 🏗️ Backend Engineering
- FastAPI
- Layered architecture
- Repository pattern
- Service layer
- Pydantic validation
- Dependency injection

### 🐳 DevOps
- Docker
- Docker Compose
- Environment-based configuration

### 🧪 Testing
- Pytest integration tests
- Authentication tests
- CRUD tests
- Geospatial API tests

---

## Live Demo

🚧 **Coming soon** — a dashboard frontend is in progress. This section will be updated with a live link and screenshots once it's deployed. In the meantime, the full API is explorable via the interactive Swagger docs (see [Running the Application](#running-the-application)).

---

## Tech Stack

| Category | Technology |
|---|---|
| Backend Framework | FastAPI |
| Language | Python 3.11+ |
| Database | PostgreSQL |
| Spatial Extension | PostGIS |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT (JSON Web Tokens), Passlib |
| Migrations | Alembic |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| API Docs | Swagger UI, ReDoc |
| Version Control | Git, GitHub |

---

## System Architecture

### Architecture Diagram

```mermaid
flowchart TD
    A["Client (Swagger UI / Postman / Future Frontend)"] --> B[FastAPI REST API]
    B --> C[JWT Authentication Middleware]
    C --> D[API Layer - Routers]
    D --> E[Service Layer - Business Logic]
    E --> F[Repository Layer - Data Access]
    F --> G[SQLAlchemy ORM]
    G --> H[(PostgreSQL + PostGIS)]
    H --> G
    G --> F
    F --> E
    E --> D
    D --> A
```

The project follows a layered architecture that separates responsibilities into API, Service, Repository, and Database layers:

- **API Layer** — handles HTTP requests and responses.
- **Service Layer** — contains business logic.
- **Repository Layer** — manages database interactions.
- **Database Layer** — stores relational and geospatial data using PostgreSQL and PostGIS.

This separation improves maintainability, scalability, and testability.

### Request Lifecycle

```mermaid
flowchart LR
    Client --> Router
    Router --> Auth[Authentication]
    Auth --> Service
    Service --> Repository
    Repository --> DB[(PostgreSQL + PostGIS)]
    DB --> Repository
    Repository --> Service
    Service --> Router
    Router --> Client
```

---

## Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant FastAPI
    participant Database

    User->>FastAPI: Login Request
    FastAPI->>Database: Verify Credentials
    Database-->>FastAPI: User Found
    FastAPI-->>User: JWT Access Token

    User->>FastAPI: Protected API Request + JWT
    FastAPI->>FastAPI: Validate Token
    FastAPI-->>User: Requested Resource
```

---

## Geospatial Capabilities

The application leverages PostgreSQL with the PostGIS extension to perform efficient spatial operations.

```mermaid
flowchart TD
    A[Client Request] --> B[Nearby / Nearest / Geofence Search]
    B --> C[FastAPI]
    C --> D[Service Layer]
    D --> E[Repository]
    E --> F[PostGIS Spatial Query]
    F --> G[Matching Assets]
    G --> A
```

Supported operations:

- Nearby asset search (radius-based)
- Nearest asset lookup
- Distance calculation between two assets
- Bounding box queries
- Polygon-based geofence search

Spatial indexes on the geometry column keep these location-based queries fast even as the asset table grows.

---

## Database Design

The application uses PostgreSQL with the PostGIS extension to store and query geospatial information efficiently.

```mermaid
erDiagram
    USERS ||--o{ ASSETS : owns

    USERS {
        int id
        string username
        string email
        string password_hash
        string role
    }

    ASSETS {
        int id
        string name
        string description
        geometry location
        datetime created_at
    }
```

- **Users** — id, username, email, password hash, role
- **Assets** — id, name, description, latitude/longitude, geographic point (PostGIS geometry), created_at

---

## Project Structure

```text
GeoAsset-Tracker-Platform/
│
├── alembic/                  # Database migrations
├── app/
│   ├── api/                  # API routes
│   ├── config/                # Application settings
│   ├── database/               # Database configuration
│   ├── models/                # SQLAlchemy models
│   ├── repositories/           # Database access layer
│   ├── schemas/                # Pydantic request/response models
│   ├── services/               # Business logic
│   ├── utils/                  # Helper functions
│   └── main.py                 # FastAPI application entrypoint
│
├── tests/                    # Integration tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## API Endpoints

> ℹ️ Paths below follow standard REST conventions based on the modules implemented — verify these against your actual route definitions and update as needed. Full, always-accurate documentation (with request/response schemas) is generated automatically at `/docs`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Authenticate and receive a JWT |
| GET | `/api/v1/assets` | List all assets |
| POST | `/api/v1/assets` | Create a new asset |
| GET | `/api/v1/assets/{id}` | Retrieve a single asset |
| PUT | `/api/v1/assets/{id}` | Update an asset |
| DELETE | `/api/v1/assets/{id}` | Delete an asset |
| GET | `/api/v1/assets/nearby` | Find assets within a radius |
| GET | `/api/v1/assets/nearest` | Find the nearest asset to a point |
| GET | `/api/v1/assets/distance` | Calculate distance between two assets |
| GET | `/api/v1/assets/bbox` | Search assets within a bounding box |
| POST | `/api/v1/assets/geofence` | Search assets within a polygon |
| GET | `/health` | Application health check |

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ with the PostGIS extension available
- Docker & Docker Compose (recommended, optional if running locally)
- Git

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/dhanushgowdars/GeoAsset-Tracker-Platform.git
cd GeoAsset-Tracker-Platform
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://geouser:yourpassword@localhost:5432/geoasset_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

POSTGRES_USER=geouser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=geoasset_db
```

> Replace the values according to your local environment.

**Enable PostGIS and run migrations** (if not running via Docker, which handles this automatically):

```bash
psql -U geouser -d geoasset_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
alembic upgrade head
```

### Docker Setup

Build and start the application:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

Stop containers:

```bash
docker compose down
```

The PostgreSQL database is automatically initialized with the PostGIS extension. If your entrypoint doesn't run migrations automatically, apply them manually:

```bash
docker compose exec app alembic upgrade head
```

### Running the Application

```bash
uvicorn app.main:app --reload
```

| Resource | URL |
|---|---|
| Application | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## Testing

```mermaid
flowchart TD
    Pytest --> Authentication
    Pytest --> CRUD
    Pytest --> Authorization
    Pytest --> Geospatial
    Pytest --> Health
```

Run all integration tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

The project includes tests for:

- Authentication
- Authorization
- CRUD operations
- Geospatial APIs
- Health endpoint

---

## Planned Frontend (Roadmap)

The backend is complete; the next phase is a small but focused **fleet management dashboard** that visibly demonstrates each backend capability rather than just CRUD.

| Feature | Demonstrates |
|---|---|
| Login / logout with session persistence | JWT authentication |
| Dashboard summary cards (total, online, offline assets) | Aggregation over the assets API |
| Asset table with create / edit / delete | Full CRUD |
| Interactive map with asset markers | Geospatial data rendering |
| Drag-to-update asset position | PUT endpoint + live map sync |
| Nearby search (lat/lng + radius) | PostGIS radius queries |
| Click-to-find-nearest | PostGIS nearest-neighbor query |
| Distance calculator between two assets | PostGIS distance queries |
| "Search visible area" on map pan/zoom | Bounding box queries |
| Draw-a-polygon geofence search | PostGIS polygon queries |
| Role-based UI (admin vs. standard user) | RBAC in practice |
| Friendly handling of invalid login / expired token / 404s | Mature error handling |

**Planned stack:** React frontend (Vercel) → FastAPI backend (Render/Railway) → PostgreSQL + PostGIS, so the whole system can be demoed live end-to-end during interviews.

```mermaid
flowchart LR
    User --> React
    React --> FastAPI
    FastAPI --> PostgreSQL
    PostgreSQL --> PostGIS
```

This section will be replaced with real screenshots, a live demo link, and updated architecture diagrams once the frontend is built.

---

## Future Improvements

Planned enhancements beyond the current scope:

- Cloud deployment (backend + database)
- API rate limiting
- Refresh tokens
- Audit logging
- Caching with Redis
- CI/CD pipeline
- Kubernetes deployment

> **Note:** Redis, CI/CD, and Kubernetes were intentionally left out of the current build to keep the backend focused and aligned with its original scope. They're listed here as possible future enhancements, not planned requirements.

---

## Learning Outcomes

Through this project, hands-on experience was gained with:

- Designing scalable REST APIs
- FastAPI application development
- Layered backend architecture
- Repository pattern
- Service layer design
- JWT authentication
- PostgreSQL
- PostGIS spatial queries
- SQLAlchemy ORM
- Alembic migrations
- Docker containerization
- Pytest integration testing
- Git & GitHub workflows

---

## Author

**Dhanush R S**

Backend Developer | Python | FastAPI | PostgreSQL | PostGIS

- GitHub: [github.com/dhanushgowdars](https://github.com/dhanushgowdars)
- LinkedIn: [linkedin.com/in/your-linkedin](https://linkedin.com/in/your-linkedin)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
