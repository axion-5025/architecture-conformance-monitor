# Deployment Diagram

## Architecture Conformance Monitor

### Document Information

| Field | Description |
|---|---|
| Project | Architecture Conformance Monitor |
| Diagram | Deployment Diagram |
| Version | 1.0 |
| Deployment model | Docker Compose–based containerized deployment |
| Frontend | React and TypeScript served through Nginx |
| Backend | Python FastAPI and Uvicorn |
| Database | PostgreSQL |
| CI/CD | GitHub Actions |

---

## 1. Purpose

The deployment diagram describes how the software components of the Architecture Conformance Monitor are deployed across runtime nodes.

It shows:

- The user’s web browser
- The Docker host machine
- The React dashboard container
- The FastAPI conformance platform container
- The PostgreSQL database container
- The sample Python microservice containers
- Persistent database storage
- GitHub and GitHub Actions
- Network ports and communication protocols

The deployment model allows the complete project to run consistently on development machines, demonstration systems, and supported cloud servers.

---

## 2. Deployment Overview

The system is packaged using Docker containers and coordinated using Docker Compose.

The deployment contains the following runtime services:

| Service | Technology | Host port | Container port | Purpose |
|---|---|---:|---:|---|
| Dashboard | React, TypeScript, Nginx | 8080 | 80 | Serves the web interface |
| Conformance API | FastAPI, Uvicorn | 8000 | 8000 | Executes scans and provides REST APIs |
| Order service | FastAPI, Uvicorn | 8001 | 8000 | Sample Python microservice |
| Payment service | FastAPI, Uvicorn | 8002 | 8000 | Sample Python microservice |
| Inventory service | FastAPI, Uvicorn | 8003 | 8000 | Sample Python microservice |
| PostgreSQL | PostgreSQL 18 Alpine | 5432 | 5432 | Stores scan history and violation evidence |

All containers communicate through the private Docker Compose network.

---

## 3. Deployment Diagram

```mermaid
flowchart TB
    developer["Developer / Administrator"]
    browser["Web Browser"]

    subgraph github["GitHub Cloud"]
        repository["GitHub Repository"]
        actions["GitHub Actions Runner"]
    end

    subgraph host["Docker Host"]
        compose["Docker Compose"]

        subgraph network["Private Docker Network"]
            dashboard["Dashboard Container<br/>React + Nginx<br/>Port 80"]
            api["Conformance API Container<br/>FastAPI + Uvicorn<br/>Port 8000"]
            postgres["PostgreSQL Container<br/>Port 5432"]

            subgraph services["Sample Microservice Containers"]
                order["Order Service<br/>Port 8000"]
                payment["Payment Service<br/>Port 8000"]
                inventory["Inventory Service<br/>Port 8000"]
            end
        end

        volume[("PostgreSQL Volume")]
        source["Mounted Application Source<br/>Rules and Python Services"]
    end

    developer -->|"Push source code"| repository
    repository -->|"Trigger workflow"| actions
    actions -->|"Lint, test, build and scan"| repository

    developer --> browser
    browser -->|"HTTP :8080"| dashboard
    dashboard -->|"REST API /api/v1/*"| api

    compose -.->|"Creates and manages"| dashboard
    compose -.->|"Creates and manages"| api
    compose -.->|"Creates and manages"| postgres
    compose -.->|"Creates and manages"| services

    api -->|"SQL over TCP :5432"| postgres
    postgres -->|"Persist records"| volume

    api -->|"Read rules and source files"| source
    source --> order
    source --> payment
    source --> inventory
```

---

## 4. Deployment Nodes

### 4.1 Developer Workstation

The developer workstation is used to:

- Write and modify source code
- Configure architecture rules
- Run Python tests
- Build the React dashboard
- Start Docker Compose
- Inspect scan results
- Commit and push changes to GitHub

The supported development environment includes:

- Python 3.12
- Node.js and npm
- Docker Desktop
- Docker Compose
- Git
- Visual Studio Code

---

### 4.2 Client Browser

The user accesses the Architecture Guard dashboard through a standard web browser.

Development URL:

```text
http://localhost:5173
```

Containerized production URL:

```text
http://localhost:8080
```

The browser is responsible for:

- Rendering the React dashboard
- Displaying scan metrics
- Showing conformance status
- Displaying scan history
- Displaying violation evidence
- Sending scan requests to the backend API

The browser does not directly access PostgreSQL or the sample microservices.

---

### 4.3 Docker Host

The Docker host may be:

- A Windows development computer using Docker Desktop
- A Linux server
- A virtual machine
- A supported cloud compute instance

Docker Compose creates and manages the project containers and their private network.

Responsibilities of the Docker host include:

- Building container images
- Starting and stopping containers
- Mapping host ports to container ports
- Providing container networking
- Managing health checks
- Managing persistent volumes

---

### 4.4 Dashboard Container

The dashboard is built using React and TypeScript.

A multi-stage Docker build is used:

1. Node.js installs dependencies.
2. Vite produces the optimized frontend bundle.
3. Nginx serves the generated static files.

Deployment details:

| Property | Value |
|---|---|
| Container | Dashboard |
| Build file | `dashboard/Dockerfile` |
| Web server | Nginx |
| Configuration | `dashboard/nginx.conf` |
| Internal port | 80 |
| Host port | 8080 |
| Protocol | HTTP |

The Nginx server also supports single-page application routing by returning `index.html` for frontend routes.

The dashboard sends API requests to the conformance platform through the configured API endpoint.

---

### 4.5 Conformance API Container

The conformance API is the central backend deployment unit.

Deployment details:

| Property | Value |
|---|---|
| Container | Conformance API |
| Framework | FastAPI |
| Application server | Uvicorn |
| Build file | `docker/platform.Dockerfile` |
| Internal port | 8000 |
| Host port | 8000 |
| Health endpoint | `/health` |

The API container provides endpoints such as:

```text
GET  /health
POST /api/v1/scans
GET  /api/v1/scans/latest
GET  /api/v1/scans/history
GET  /api/v1/scans/{scan_id}
```

Its responsibilities include:

- Loading architecture rules
- Scanning the Python microservices
- Evaluating detected dependencies
- Generating conformance reports
- Determining whether a scan is blocking
- Saving scan records
- Saving violation evidence
- Returning results to the dashboard

---

### 4.6 PostgreSQL Container

PostgreSQL stores the persisted technical-debt and conformance history.

Deployment details:

| Property | Value |
|---|---|
| Image | `postgres:18-alpine` |
| Internal port | 5432 |
| Host port | 5432 |
| Database | `architecture_monitor` |
| Default user | `architecture_user` |
| Persistent volume | `postgres-data` |

The API connects to PostgreSQL using a SQLAlchemy database URL similar to:

```text
postgresql+psycopg://architecture_user:architecture_password@postgres:5432/architecture_monitor
```

The hostname is `postgres` because containers communicate using Docker Compose service names.

The database stores:

- Scan identifiers
- Scan timestamps
- Application names
- Rules versions
- Summary metrics
- Blocking status
- Architecture violation details
- Source and dependency evidence

---

### 4.7 PostgreSQL Persistent Volume

The named Docker volume is:

```text
postgres-data
```

It stores PostgreSQL data outside the writable container layer.

This ensures that scan history remains available when containers are:

- Restarted
- Recreated
- Rebuilt
- Temporarily stopped

Running the following command removes containers but preserves the named volume:

```powershell
docker compose down
```

Running the following command also removes the stored database volume:

```powershell
docker compose down -v
```

The `-v` option must therefore be used carefully.

---

### 4.8 Sample Microservice Containers

The project includes three Python sample microservices.

| Service | Host port | Container port |
|---|---:|---:|
| Order service | 8001 | 8000 |
| Payment service | 8002 | 8000 |
| Inventory service | 8003 | 8000 |

Each service:

- Uses Python
- Runs through Uvicorn
- Provides a `/health` endpoint
- Represents a service examined by the conformance scanner
- Is built using `docker/service.Dockerfile`

These services demonstrate how architecture rules can be applied to a microservice-based application.

The scanner primarily inspects their Python source code statically. It does not require runtime API calls to discover local layer imports.

---

## 5. Port Mapping Diagram

```mermaid
flowchart LR
    browser["Browser"]

    subgraph host["Docker Host Ports"]
        p8080["8080"]
        p8000["8000"]
        p8001["8001"]
        p8002["8002"]
        p8003["8003"]
        p5432["5432"]
    end

    subgraph containers["Container Ports"]
        dashboard["Dashboard :80"]
        api["Conformance API :8000"]
        order["Order :8000"]
        payment["Payment :8000"]
        inventory["Inventory :8000"]
        database["PostgreSQL :5432"]
    end

    browser --> p8080
    p8080 --> dashboard
    p8000 --> api
    p8001 --> order
    p8002 --> payment
    p8003 --> inventory
    p5432 --> database
```

---

## 6. Internal Communication

| Source | Destination | Protocol | Purpose |
|---|---|---|---|
| Browser | Dashboard | HTTP | Load the web application |
| Dashboard | Conformance API | HTTP/JSON | Run scans and retrieve results |
| Conformance API | PostgreSQL | PostgreSQL protocol | Store and retrieve scan evidence |
| Conformance API | Architecture rules | File access | Load the declared baseline |
| Conformance API | Service source code | File access | Perform static dependency scanning |
| Docker Engine | Containers | Docker API | Manage runtime lifecycle |
| GitHub Actions | Repository source | GitHub workflow | Test and validate submitted code |

---

## 7. External Communication

The primary external communication paths are:

### User to dashboard

```text
Browser → http://localhost:8080
```

### Dashboard to backend

```text
Dashboard → http://localhost:8000/api/v1/*
```

When the dashboard and API run in the same Compose network, Nginx may proxy `/api/` requests directly to:

```text
http://conformance-api:8000
```

This avoids exposing internal Docker service names to the browser.

### Developer to GitHub

```text
Developer workstation → GitHub repository
```

Git pushes trigger the Architecture CI workflow.

---

## 8. Docker Compose Deployment Sequence

```mermaid
sequenceDiagram
    actor Developer
    participant Compose as Docker Compose
    participant DB as PostgreSQL
    participant API as Conformance API
    participant UI as Dashboard

    Developer->>Compose: docker compose up -d --build
    Compose->>DB: Create and start database
    loop Health check
        Compose->>DB: pg_isready
        DB-->>Compose: Ready
    end
    Compose->>API: Start after database is healthy
    loop Health check
        Compose->>API: GET /health
        API-->>Compose: 200 healthy
    end
    Compose->>UI: Start Nginx dashboard
    Compose-->>Developer: Deployment started
```

---

## 9. Container Health Checks

### PostgreSQL

PostgreSQL readiness is verified using:

```text
pg_isready
```

The API is started only after PostgreSQL becomes healthy.

### Conformance API

The API health check calls:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "service": "conformance-platform-api",
  "version": "0.3.0",
  "status": "healthy"
}
```

### Sample services

Each sample service exposes its own `/health` endpoint.

The health checks allow Docker Compose to report whether each container is:

- Starting
- Healthy
- Unhealthy
- Restarting
- Stopped

---

## 10. CI Deployment and Validation Environment

GitHub Actions provides an isolated Linux-based validation environment for every push or pull request to the `main` branch.

```mermaid
flowchart TB
    push["Git Push or Pull Request"]
    runner["Ubuntu GitHub Actions Runner"]
    quality["Ruff and Pytest"]
    frontend["Dashboard Production Build"]
    scan["Architecture Conformance Scan"]
    result["Pass or Fail"]

    push --> runner
    runner --> quality
    quality --> frontend
    frontend --> scan
    scan --> result
```

The workflow performs:

1. Repository checkout
2. Python environment setup
3. Python dependency installation
4. Ruff static quality checks
5. Pytest automated testing
6. Node.js environment setup
7. Dashboard dependency installation
8. Dashboard production build
9. Architecture conformance scan
10. Conformance report display

This ensures that a change is validated before it is accepted as a release-ready implementation.

---

## 11. Deployment Configuration

The principal deployment files are:

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines all containers, networks, ports, volumes and dependencies |
| `docker/platform.Dockerfile` | Builds the conformance API image |
| `docker/service.Dockerfile` | Builds the sample microservice images |
| `dashboard/Dockerfile` | Builds and serves the React dashboard |
| `dashboard/nginx.conf` | Configures Nginx and frontend routing |
| `.env.example` | Documents configurable environment variables |
| `requirements.txt` | Defines Python dependencies |
| `dashboard/package.json` | Defines dashboard dependencies and scripts |
| `.github/workflows/architecture-ci.yml` | Defines automated validation |

---

## 12. Environment Variables

| Variable | Purpose | Default development value |
|---|---|---|
| `POSTGRES_DB` | PostgreSQL database name | `architecture_monitor` |
| `POSTGRES_USER` | PostgreSQL username | `architecture_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `architecture_password` |
| `POSTGRES_PORT` | Published PostgreSQL port | `5432` |
| `DATABASE_URL` | API database connection string | PostgreSQL Compose URL |
| `VITE_API_BASE_URL` | Frontend API address | `http://localhost:8000` |

Production passwords must not use the development defaults.

They should be supplied using:

- Protected environment variables
- Deployment-platform secrets
- Docker secrets
- A managed secret-storage solution

---

## 13. Local Development Deployment

The backend infrastructure can be started with:

```powershell
cd C:\architecture-conformance-monitor
docker compose up -d --build
docker compose ps
```

The development dashboard can be started separately with:

```powershell
cd C:\architecture-conformance-monitor\dashboard
npm install
npm run dev
```

Development access points:

| Component | URL |
|---|---|
| Dashboard | `http://localhost:5173` |
| Conformance API | `http://localhost:8000` |
| API documentation | `http://localhost:8000/docs` |
| Order service documentation | `http://localhost:8001/docs` |
| Payment service documentation | `http://localhost:8002/docs` |
| Inventory service documentation | `http://localhost:8003/docs` |

---

## 14. Complete Containerized Deployment

The complete production-style local deployment can be started using:

```powershell
cd C:\architecture-conformance-monitor
docker compose up -d --build
docker compose ps
```

The dashboard is then available at:

```text
http://localhost:8080
```

Useful operational commands:

```powershell
docker compose logs --tail 100
docker compose logs --tail 100 conformance-api
docker compose restart conformance-api
docker compose down
```

---

## 15. Cloud Deployment Possibilities

The containerized architecture can be deployed to:

- Amazon Web Services
- Microsoft Azure
- Google Cloud Platform
- DigitalOcean
- Render
- Railway
- A Linux virtual private server
- An on-premises Docker server

A basic cloud deployment may use:

| Project component | Cloud deployment option |
|---|---|
| Dashboard | Static hosting, Nginx container or CDN |
| Conformance API | Docker container service |
| PostgreSQL | Managed PostgreSQL database |
| Source repository | GitHub |
| CI/CD | GitHub Actions |
| Container images | Container registry |
| Secrets | Cloud secret manager |

---

## 16. Recommended Production Deployment

For a production deployment:

- Serve the dashboard over HTTPS.
- Place the API behind a reverse proxy or API gateway.
- Use a managed PostgreSQL database.
- Store credentials in a secret manager.
- Do not expose PostgreSQL publicly.
- Restrict CORS to approved frontend domains.
- Enable application logs and monitoring.
- Configure automated backups.
- Run containers using non-root users.
- Apply CPU and memory limits.
- Scan container images for vulnerabilities.
- Use immutable versioned container tags.

---

## 17. Security Considerations

### Network security

Only required ports should be published.

PostgreSQL should normally remain accessible only inside the private deployment network.

### Credential security

Database credentials must not be committed to GitHub.

### API security

A future production version should support:

- Authentication
- Role-based authorization
- Rate limiting
- Request validation
- HTTPS
- Audit logging

### Container security

Container images should:

- Use trusted base images
- Run with minimum privileges
- Exclude development files
- Be rebuilt when security updates are released
- Be checked for known vulnerabilities

---

## 18. Availability and Recovery

The deployment supports basic availability through:

- Container health checks
- Persistent PostgreSQL storage
- Repeatable Docker image builds
- Automated CI verification
- Service restart capabilities

Recovery can be performed by:

1. Restoring PostgreSQL data from backup.
2. Pulling the application source from GitHub.
3. Restoring environment variables.
4. Rebuilding the Docker images.
5. Starting the Compose deployment.
6. Verifying all container health checks.

---

## 19. Deployment Constraints

The current MVP has the following deployment constraints:

- It targets Python source-code analysis.
- It uses one PostgreSQL database instance.
- Docker Compose is the primary orchestration method.
- Authentication and role-based access control are not included.
- Horizontal scaling is not configured.
- Distributed tracing infrastructure is planned but not required for the current MVP.
- The demonstration microservices are deployed on the same Docker host.

These constraints are acceptable for the academic MVP and can be extended in future phases.

---

## 20. Deployment Verification Checklist

The deployment is considered successful when:

- Docker Compose configuration is valid.
- All required images build successfully.
- PostgreSQL becomes healthy.
- The conformance API becomes healthy.
- All three sample services become healthy.
- The dashboard loads successfully.
- The dashboard can run a scan.
- Scan history is persisted.
- Violation evidence can be expanded.
- Data remains available after container recreation.
- GitHub Actions completes successfully.

Commands used for verification:

```powershell
docker compose config
docker compose up -d --build
docker compose ps
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod -Method Post http://localhost:8000/api/v1/scans
Invoke-WebRequest http://localhost:8080
git status
```

---

## 21. Conclusion

The Architecture Conformance Monitor uses a portable container-based deployment architecture.

The React dashboard, FastAPI backend, PostgreSQL database and sample Python microservices are isolated into separate deployment units while remaining connected through a controlled Docker network.

Persistent storage preserves historical scan evidence, health checks verify runtime readiness, and GitHub Actions validates each source-code change.

This deployment design provides a reproducible foundation for local development, academic demonstration, continuous integration and future cloud deployment.