# Software Requirements Specification

## Architecture Conformance Monitor

| Document Information | Details |
|---|---|
| Project | Architecture Conformance Monitor |
| Document type | Software Requirements Specification |
| Version | 1.0 |
| Status | MVP Baseline |
| Prepared for | Software Engineering Project |
| Primary technology | Python, FastAPI, React, TypeScript and PostgreSQL |

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification defines the functional and non-functional requirements of the Architecture Conformance Monitor.

The system continuously evaluates Python microservices against predefined architectural rules. It identifies forbidden dependencies, produces evidence for violations, stores scan history, presents results through a web dashboard, and executes automated conformance checks through continuous integration.

This document establishes a shared understanding among developers, software architects, project managers, quality engineers, DevOps engineers, and academic evaluators.

### 1.2 Intended Audience

This document is intended for:

- Software developers
- Software architects
- Technical leads
- Quality assurance engineers
- DevOps engineers
- Project managers
- Academic supervisors
- Project evaluators
- Future maintainers

### 1.3 Product Scope

The Architecture Conformance Monitor is a full-stack platform that:

- Loads architecture rules from YAML.
- Scans configured Python microservices.
- Parses Python files using the Abstract Syntax Tree.
- Detects dependencies between application layers.
- Evaluates dependencies against permitted and forbidden rules.
- Generates structured conformance reports.
- Determines whether violations should block a release.
- Stores scan summaries and violation evidence in PostgreSQL.
- Exposes scan operations through a FastAPI REST API.
- Displays current and historical results through a React dashboard.
- Runs linting, tests, architecture scanning, and frontend builds through GitHub Actions.
- Supports local containerised execution through Docker Compose.

### 1.4 Project Aim

The aim is to automate the detection, recording, and communication of architectural drift in Python microservices so that structural technical debt can be identified before it becomes expensive to correct.

### 1.5 Definitions and Abbreviations

| Term | Definition |
|---|---|
| API | Application Programming Interface |
| AST | Abstract Syntax Tree |
| CI | Continuous Integration |
| CORS | Cross-Origin Resource Sharing |
| CRUD | Create, Read, Update and Delete |
| JSON | JavaScript Object Notation |
| MVP | Minimum Viable Product |
| REST | Representational State Transfer |
| SRS | Software Requirements Specification |
| UI | User Interface |
| YAML | YAML Ain't Markup Language |
| Architecture conformance | Degree to which implementation follows declared architecture rules |
| Architecture drift | Gradual deviation of source code from the intended architecture |
| Blocking violation | Violation that prevents architectural approval or release |
| Dependency evidence | Information proving that one layer imports another |
| Layer | Logical source-code grouping such as API, services or repositories |
| Scan | One complete execution of architectural analysis |
| Technical debt | Future maintenance cost created by unsuitable design or implementation decisions |
| Violation | Detected dependency that breaks a declared architecture rule |

### 1.6 References

The SRS is based on:

- Project problem statement and objectives
- Implemented Architecture Conformance Monitor MVP
- Architecture rules in `architecture-rules/baseline.yml`
- FastAPI REST interface
- React and TypeScript dashboard
- PostgreSQL persistence model
- Docker Compose deployment configuration
- GitHub Actions quality workflow
- Automated project test suite

### 1.7 Document Conventions

Requirements use the following identifiers:

| Prefix | Requirement category |
|---|---|
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| DR | Data Requirement |
| IR | Interface Requirement |
| BR | Business Rule |
| AC | Acceptance Criterion |
| UC | Use Case |

The priority levels are:

| Priority | Meaning |
|---|---|
| Must | Required for the MVP to operate |
| Should | Important but not essential for basic operation |
| Could | Desirable future enhancement |

---

## 2. Overall Description

### 2.1 Product Perspective

The Architecture Conformance Monitor is an independent platform that analyses the source code of configured Python microservices.

It is composed of the following major subsystems:

1. Architecture rule loader
2. Python static dependency scanner
3. Rule evaluation engine
4. Conformance report generator
5. Technical-debt persistence layer
6. FastAPI backend
7. React dashboard
8. PostgreSQL database
9. Docker Compose environment
10. GitHub Actions CI workflow

The application does not execute scanned source files. It analyses their syntax and imports statically.

### 2.2 Problem Context

Architecture is generally defined during software design, but implementation can gradually deviate from that design. Functional tests do not normally identify structural violations such as an API layer directly importing a repository layer.

Manual review is inconsistent and becomes increasingly difficult as a system grows. The platform addresses this problem by converting architecture rules into automated and repeatable checks.

### 2.3 Product Functions

The product provides the following primary functions:

- Define architecture rules in YAML.
- Validate architecture-rule configuration.
- Identify configured services.
- Find Python source files.
- Parse Python imports.
- Classify source and target layers.
- Ignore external dependencies.
- Detect forbidden layer relationships.
- Generate stable violation evidence.
- Calculate scan summary metrics.
- Determine blocking status.
- Save scan results.
- Retrieve the latest scan.
- Retrieve scan history.
- Retrieve complete evidence for a selected scan.
- Display results through a dashboard.
- Automate conformance checks in CI.
- Run the complete platform using containers.

### 2.4 User Classes

#### 2.4.1 Software Architect

The software architect defines architectural rules, reviews violations, and determines whether implementation conforms to the intended design.

#### 2.4.2 Developer

The developer runs scans, examines evidence, corrects forbidden dependencies, and verifies that changes are conformant.

#### 2.4.3 Technical Lead

The technical lead reviews scan trends, release status, and accumulated technical debt.

#### 2.4.4 Quality Engineer

The quality engineer validates expected system behaviour and includes architectural conformance in the quality process.

#### 2.4.5 DevOps Engineer

The DevOps engineer operates containerised services and maintains CI enforcement.

#### 2.4.6 Project Manager

The project manager uses scan status and history as evidence of implementation quality and release readiness.

#### 2.4.7 Academic Evaluator

The academic evaluator reviews the software-engineering process, implementation, test evidence, and project documentation.

### 2.5 Operating Environment

The system is designed for the following environment:

| Component | Environment |
|---|---|
| Development operating system | Windows, Linux or macOS |
| Backend runtime | Python 3.12 |
| Backend framework | FastAPI |
| Frontend runtime | Modern web browser |
| Frontend framework | React with TypeScript |
| Database | PostgreSQL |
| Static analysis | Python AST |
| Configuration | YAML |
| Container runtime | Docker with Docker Compose |
| Frontend web server | Nginx |
| CI platform | GitHub Actions |
| Source control | Git and GitHub |

### 2.6 Design and Implementation Constraints

- Only Python services are analysed in the MVP.
- Services must follow a recognisable package structure.
- Internal architectural layers must be represented by directory or module names.
- Architecture rules must be provided in valid YAML.
- Static analysis observes declared imports but may not detect every runtime dependency.
- PostgreSQL is used for persistent production-style storage.
- The application must not execute scanned Python source code.
- The backend and dashboard must communicate using JSON REST endpoints.
- The complete application must run using Docker Compose.
- The source repository is maintained on GitHub.

### 2.7 Assumptions and Dependencies

- Python source paths exist and are readable.
- Configured services use valid Python syntax.
- Architecture rules correctly represent approved design decisions.
- Docker is available when running the complete containerised environment.
- PostgreSQL is reachable using the configured database URL.
- The frontend can reach the backend using the configured API address.
- GitHub Actions can install project dependencies.
- Users have permission to access the source repository and development environment.

### 2.8 Out-of-Scope Capabilities

The MVP does not provide:

- Authentication and role-based access control
- Multi-tenant project management
- Automatic source-code repair
- Runtime distributed-trace analysis
- Support for languages other than Python
- Automatic rule generation using machine learning
- Kubernetes deployment
- External notification integrations
- Advanced user administration
- Production secrets management
- Full source-control provider integration

---

## 3. System Architecture Overview

### 3.1 Logical Architecture

The system uses a layered and component-based structure:

- The dashboard provides the user interface.
- The REST API coordinates scan and query operations.
- The scanner detects dependencies.
- The rule engine evaluates dependencies.
- The report generator constructs structured results.
- The debt tracker persists scan history and evidence.
- PostgreSQL stores persistent records.
- GitHub Actions executes automated validation.

### 3.2 Major Components

| Component | Responsibility |
|---|---|
| Rule loader | Load and validate the YAML architecture baseline |
| Python scanner | Parse Python files and detect internal imports |
| Rule evaluator | Compare dependencies with allowed architecture rules |
| CLI | Execute a complete scan and generate a JSON report |
| Debt tracker | Persist scan records and violation evidence |
| REST API | Expose scanning and historical data |
| Dashboard | Present metrics, trends, history and evidence |
| PostgreSQL | Store scan and violation records |
| Docker Compose | Coordinate the application containers |
| GitHub Actions | Perform automated quality and conformance checks |

### 3.3 Sample Services

The MVP scans:

- `order-service`
- `payment-service`
- `inventory-service`

These services demonstrate how the platform evaluates multiple Python microservices.

---

## 4. Functional Requirements

### 4.1 Architecture Rule Management

#### FR-001: Load architecture rules

The system shall load architecture rules from a configured YAML file.

- Priority: Must
- Input: Path to the YAML rules file
- Output: Validated architecture-rule model

#### FR-002: Validate rule structure

The system shall validate the YAML structure before starting a scan.

Validation shall include:

- Required application information
- Rules version
- Declared language
- Configured services
- Layer definitions
- Permitted dependency definitions
- Forbidden dependency definitions

- Priority: Must

#### FR-003: Reject unknown fields

The system shall reject unsupported or unknown fields in the architecture-rule file.

- Priority: Must

#### FR-004: Reject unknown service references

The system shall reject rules that reference a service that has not been declared.

- Priority: Must

#### FR-005: Reject conflicting ownership

The system shall reject configuration that assigns prohibited shared ownership where exclusive ownership is required.

- Priority: Must

#### FR-006: Report rule errors

The system shall return a clear validation error when the architecture-rule file is invalid.

- Priority: Must

### 4.2 Source-Code Scanning

#### FR-007: Scan configured services

The system shall scan every service declared in the architecture baseline.

- Priority: Must

#### FR-008: Locate Python files

The scanner shall recursively locate Python files within each configured service source path.

- Priority: Must

#### FR-009: Parse Python files

The scanner shall parse Python source files using the Python Abstract Syntax Tree.

- Priority: Must

#### FR-010: Avoid source execution

The scanner shall not execute the Python source code being analysed.

- Priority: Must

#### FR-011: Count scanned files

The scanner shall count the number of Python files inspected for each service and for the complete scan.

- Priority: Must

#### FR-012: Detect import statements

The scanner shall detect both:

- `import module`
- `from module import object`

- Priority: Must

#### FR-013: Identify source layer

The scanner shall determine the source layer from the location of the importing file.

- Priority: Must

#### FR-014: Identify target layer

The scanner shall determine the target layer from the imported internal module.

- Priority: Must

#### FR-015: Ignore external dependencies

The scanner shall ignore standard-library and third-party dependencies that do not represent internal architectural layers.

- Priority: Must

#### FR-016: Record dependency evidence

For each internal dependency, the scanner shall record:

- Service name
- Source file
- Line number
- Source layer
- Target layer
- Target module
- Evidence type

- Priority: Must

#### FR-017: Reject invalid Python syntax

The scanner shall stop processing an invalid Python file and return an error identifying the affected file.

- Priority: Must

### 4.3 Conformance Evaluation

#### FR-018: Evaluate detected dependencies

The system shall compare every detected internal dependency with the declared architecture rules.

- Priority: Must

#### FR-019: Detect forbidden layer dependency

The system shall create a violation when a source layer imports a forbidden target layer.

- Priority: Must

#### FR-020: Allow permitted dependencies

The system shall not create a violation for dependencies permitted by the architecture rules.

- Priority: Must

#### FR-021: Generate violation identifier

The system shall generate a stable identifier for every detected violation.

- Priority: Must

#### FR-022: Assign violation type

Each violation shall include a violation type such as `layer_violation`.

- Priority: Must

#### FR-023: Assign severity

Each violation shall include its configured severity.

- Priority: Must

#### FR-024: Generate violation message

The system shall provide a human-readable message explaining the violated rule.

- Priority: Must

#### FR-025: Determine blocking status

The system shall mark a scan as blocking when at least one blocking architecture violation is detected.

- Priority: Must

#### FR-026: Produce conformant status

The system shall classify a scan as conformant when no blocking violation is detected.

- Priority: Must

### 4.4 Report Generation

#### FR-027: Generate scan report

The system shall generate a structured conformance report after completing a scan.

- Priority: Must

#### FR-028: Include report metadata

The report shall include:

- Generation timestamp
- Application name
- Architecture-rules version

- Priority: Must

#### FR-029: Include summary metrics

The report shall include:

- Services scanned
- Files scanned
- Dependencies found
- Violations found

- Priority: Must

#### FR-030: Include service results

The report shall include the scan result for each configured service.

- Priority: Must

#### FR-031: Include violations

The report shall include complete evidence for every violation.

- Priority: Must

#### FR-032: Write JSON report

The CLI shall write the conformance report to the configured JSON output path.

- Priority: Must

#### FR-033: Return process result

The CLI shall return:

- Exit code `0` when the scan contains no blocking violations.
- Exit code `1` when the scan contains blocking violations or cannot complete successfully.

- Priority: Must

### 4.5 Scan Persistence

#### FR-034: Save scan record

The system shall save a persistent database record for each scan initiated through the API.

- Priority: Must

#### FR-035: Save summary values

The scan record shall store:

- Generation time
- Application
- Rules version
- Services scanned
- Files scanned
- Dependencies found
- Violations found
- Blocking status

- Priority: Must

#### FR-036: Save violation evidence

The system shall store every violation associated with its scan record.

- Priority: Must

#### FR-037: Preserve scan-to-violation relationship

A violation record shall reference the scan that generated it.

- Priority: Must

#### FR-038: Delete dependent violations

If a scan record is deleted through a future persistence operation, its dependent violation records shall also be deleted.

- Priority: Should

#### FR-039: Retrieve latest scan

The system shall retrieve the most recent persisted scan.

- Priority: Must

#### FR-040: List scan history

The system shall return scan records ordered from newest to oldest.

- Priority: Must

#### FR-041: Limit history results

The persistence layer shall support limiting the number of scan-history results returned.

- Priority: Must

#### FR-042: Retrieve scan by identifier

The system shall retrieve a specific scan and its associated violations using the scan identifier.

- Priority: Must

#### FR-043: Handle unknown scan identifier

The system shall report that a scan does not exist when the supplied identifier cannot be found.

- Priority: Must

### 4.6 REST API

#### FR-044: Provide health endpoint

The API shall provide `GET /health`.

It shall return:

- Service name
- API version
- Health status

- Priority: Must

#### FR-045: Create scan endpoint

The API shall provide `POST /api/v1/scans`.

The endpoint shall:

1. Run an architecture scan.
2. Generate a report.
3. Persist the report.
4. Return the scan identifier.
5. Return blocking status.
6. Return the complete report.

- Priority: Must

#### FR-046: Latest scan endpoint

The API shall provide `GET /api/v1/scans/latest`.

The endpoint shall return the most recent scan and its persisted report data.

- Priority: Must

#### FR-047: Empty latest-scan response

The latest-scan endpoint shall return HTTP `404` when no scan is available.

- Priority: Must

#### FR-048: Scan history endpoint

The API shall provide `GET /api/v1/scans/history`.

- Priority: Must

#### FR-049: Scan-detail endpoint

The API shall provide `GET /api/v1/scans/{scan_id}`.

The endpoint shall return:

- Scan metadata
- Scan summary
- Blocking status
- Complete persisted violation evidence

- Priority: Must

#### FR-050: Unknown scan-detail response

The scan-detail endpoint shall return HTTP `404` when the scan identifier does not exist.

- Priority: Must

#### FR-051: Return JSON responses

All REST endpoints shall return JSON-compatible responses.

- Priority: Must

#### FR-052: Validate response models

The API shall validate its responses using explicitly defined Pydantic models.

- Priority: Must

#### FR-053: Configure CORS

The API shall permit requests from configured dashboard origins.

- Priority: Must

### 4.7 Dashboard

#### FR-054: Display application identity

The dashboard shall display the product name “Architecture Guard”.

- Priority: Must

#### FR-055: Display scan metrics

The dashboard shall display:

- Services scanned
- Files scanned
- Dependencies found
- Violations found

- Priority: Must

#### FR-056: Display conformance status

The dashboard shall indicate whether the latest scan is:

- Conformant
- Release blocked
- Not yet available

- Priority: Must

#### FR-057: Display latest scan metadata

The dashboard shall display:

- Application name
- Rule-set version
- Scan identifier

- Priority: Must

#### FR-058: Run scan from dashboard

The user shall be able to start a scan by selecting the Run Scan button.

- Priority: Must

#### FR-059: Refresh dashboard

The user shall be able to reload scan information by selecting the Refresh button.

- Priority: Must

#### FR-060: Display progress state

The dashboard shall disable conflicting actions and display progress while loading or scanning.

- Priority: Must

#### FR-061: Display request errors

The dashboard shall display an error message when an API operation fails.

- Priority: Must

#### FR-062: Display findings trend

The dashboard shall graph historical dependency and violation counts.

- Priority: Must

#### FR-063: Display scan history

The dashboard shall display persisted scans in newest-first order.

- Priority: Must

#### FR-064: Display scan status badge

Each scan-history row shall indicate Conformant or Blocked status.

- Priority: Must

#### FR-065: Select historical scan

The user shall be able to select a scan-history row to view its evidence.

- Priority: Must

#### FR-066: Highlight selected scan

The dashboard shall visually identify the selected history row.

- Priority: Should

#### FR-067: Display conformant evidence state

For a conformant scan, the evidence panel shall state that no violations were recorded.

- Priority: Must

#### FR-068: Display blocked-scan evidence

For a blocked scan, the evidence panel shall display every stored violation.

- Priority: Must

#### FR-069: Display detailed violation fields

The evidence panel shall display:

- Violation type
- Severity
- Message
- Service
- Source file and line
- Source and target layers
- Target module
- Evidence type
- Violation identifier

- Priority: Must

#### FR-070: Close evidence panel

The user shall be able to close the selected scan-evidence panel.

- Priority: Should

#### FR-071: Support responsive layout

The dashboard shall remain usable on desktop, tablet, and mobile screen sizes.

- Priority: Should

### 4.8 Containerisation

#### FR-072: Containerise backend

The FastAPI backend shall be buildable as a Docker image.

- Priority: Must

#### FR-073: Containerise dashboard

The React dashboard shall use a multi-stage production Docker build.

- Priority: Must

#### FR-074: Serve dashboard through Nginx

The dashboard production container shall serve the compiled static application through Nginx.

- Priority: Must

#### FR-075: Proxy API requests

Nginx shall proxy dashboard API requests to the conformance API within the Docker network.

- Priority: Must

#### FR-076: Containerise sample services

The order, payment, and inventory services shall be buildable as Docker containers.

- Priority: Must

#### FR-077: Provide PostgreSQL service

Docker Compose shall provide PostgreSQL with persistent storage.

- Priority: Must

#### FR-078: Provide service health checks

Docker Compose shall define health checks for PostgreSQL and HTTP services.

- Priority: Must

#### FR-079: Control startup dependency

The conformance API shall wait for PostgreSQL to become healthy before starting.

- Priority: Must

#### FR-080: Start complete stack

A single Docker Compose command shall start the database, API, dashboard, and sample services.

- Priority: Must

### 4.9 Continuous Integration

#### FR-081: Trigger CI on main branch changes

CI shall run on pushes and pull requests targeting the `main` branch.

- Priority: Must

#### FR-082: Install backend dependencies

CI shall install the Python dependencies declared in `requirements.txt`.

- Priority: Must

#### FR-083: Run Ruff

CI shall run Ruff against the conformance platform and tests.

- Priority: Must

#### FR-084: Run backend tests

CI shall execute the complete Python test suite.

- Priority: Must

#### FR-085: Run architecture scan

CI shall execute the architecture conformance CLI.

- Priority: Must

#### FR-086: Display conformance report

CI shall display the generated JSON report even when an earlier scan step reports failure.

- Priority: Must

#### FR-087: Install frontend dependencies

CI shall install dashboard dependencies using the committed lock file.

- Priority: Must

#### FR-088: Build dashboard

CI shall run the dashboard production build.

- Priority: Must

#### FR-089: Cancel obsolete workflow

CI shall cancel an in-progress workflow when a newer workflow starts for the same Git reference.

- Priority: Should

---

## 5. External Interface Requirements

### 5.1 User Interface Requirements

#### IR-001

The dashboard shall use a clear, professional interface suitable for technical users.

#### IR-002

Primary metrics and scan status shall be visible without opening a secondary page.

#### IR-003

Interactive controls shall provide visible disabled and loading states.

#### IR-004

Status shall not be communicated using colour alone; labels and icons shall also be used.

#### IR-005

The scan-history table shall support horizontal scrolling on smaller displays.

#### IR-006

Selected history rows shall provide visual feedback.

#### IR-007

Violation evidence shall use readable labels and group related information.

### 5.2 REST Interface Requirements

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/api/v1/scans` | Execute and persist a scan |
| GET | `/api/v1/scans/latest` | Retrieve latest scan |
| GET | `/api/v1/scans/history` | Retrieve scan history |
| GET | `/api/v1/scans/{scan_id}` | Retrieve persisted scan evidence |

### 5.3 Software Interfaces

| Interface | Purpose |
|---|---|
| YAML parser | Read architecture rules |
| Python AST | Parse source files |
| SQLAlchemy | Database object-relational mapping |
| PostgreSQL | Persistent scan storage |
| FastAPI | REST API |
| Pydantic | Data validation |
| React | Dashboard interface |
| Recharts | Findings trend visualisation |
| Nginx | Frontend hosting and API proxy |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | Continuous integration |

### 5.4 Communication Interfaces

- The dashboard and API shall communicate over HTTP.
- The API shall exchange JSON data.
- The API and PostgreSQL shall communicate through the configured database connection.
- Docker services shall communicate using the internal Compose network.
- Browser requests to `/api/` shall be proxied by Nginx to the backend in the production container environment.

### 5.5 Hardware Interfaces

The MVP has no specialised hardware requirements. It runs on a general-purpose computer capable of running Python, Node.js, Docker, and a modern web browser.

---

## 6. Data Requirements

### 6.1 Scan Record

#### DR-001

Each scan shall have a unique integer identifier.

#### DR-002

Each scan record shall contain:

| Field | Type | Required |
|---|---|---|
| ID | Integer | Yes |
| Generated time | Date and time | Yes |
| Application | String | Yes |
| Rules version | String | Yes |
| Services scanned | Integer | Yes |
| Files scanned | Integer | Yes |
| Dependencies found | Integer | Yes |
| Violations found | Integer | Yes |
| Blocking | Boolean | Yes |

### 6.2 Violation Record

#### DR-003

Each violation shall have a unique database identifier.

#### DR-004

Each violation shall reference one scan record.

#### DR-005

Each violation record shall contain:

| Field | Type | Required |
|---|---|---|
| Database ID | Integer | Yes |
| Scan ID | Integer | Yes |
| Violation ID | String | Yes |
| Violation type | String | Yes |
| Severity | String | Yes |
| Service name | String | Yes |
| Message | Text | Yes |
| Source file | Text | Yes |
| Line | Integer | Yes |
| Source layer | String | Yes |
| Target layer | String | Yes |
| Target module | Text | Yes |
| Evidence type | String | Yes |

### 6.3 Data Integrity

#### DR-006

All scan summary values shall be non-negative integers.

#### DR-007

A violation shall not exist without an associated scan.

#### DR-008

Deleting a scan shall delete its associated violations.

#### DR-009

Required scan and violation fields shall not accept null values.

#### DR-010

Scan history shall be ordered by generation time from newest to oldest.

### 6.4 Data Retention

The MVP retains all persisted scan and violation records unless the PostgreSQL volume or records are explicitly removed.

### 6.5 Report Storage

The CLI shall generate a JSON file for immediate scan output. Historical evidence used by the API shall be obtained from persisted database records so it remains available even when a report file is missing.

---

## 7. Business Rules

### BR-001

Only dependencies between recognised internal layers shall be evaluated as architecture dependencies.

### BR-002

External packages shall not be treated as internal layer dependencies.

### BR-003

A dependency prohibited by the architecture baseline shall create a violation.

### BR-004

A violation with blocking severity shall cause the scan to be classified as blocked.

### BR-005

A scan with no blocking violations shall be classified as conformant.

### BR-006

The API shall persist every successfully completed API-triggered scan.

### BR-007

A scan record and its evidence shall be treated as an auditable historical result.

### BR-008

The latest scan shall be determined using the persisted generation timestamp.

### BR-009

The dashboard shall not modify historical scan evidence.

### BR-010

The CI workflow shall fail when a blocking architecture violation is detected.

---

## 8. Non-Functional Requirements

### 8.1 Performance

#### NFR-001

The system should complete a scan of the three sample microservices within five seconds under normal local development conditions.

#### NFR-002

A dashboard API request should normally receive a response within two seconds, excluding scan execution time.

#### NFR-003

The dashboard should render the latest scan and history without noticeable delay for the MVP data volume.

### 8.2 Reliability

#### NFR-004

The same source code and rule configuration shall produce the same conformance result.

#### NFR-005

A failed scan shall not be stored as a successful result.

#### NFR-006

Database transactions shall be committed only after the scan record and its violations are prepared successfully.

#### NFR-007

The platform shall expose health checks for operational verification.

### 8.3 Security

#### NFR-008

The scanner shall use static analysis and shall not execute scanned source code.

#### NFR-009

Database credentials shall be supplied through environment variables in deployed environments.

#### NFR-010

Secrets shall not be committed to source control.

#### NFR-011

CORS shall be limited to configured frontend origins.

#### NFR-012

The API shall validate request parameters and response data.

#### NFR-013

The production dashboard shall communicate with the backend using the configured proxy rather than exposing implementation details in the interface.

### 8.4 Maintainability

#### NFR-014

Rule loading, scanning, evaluation, persistence, API, and dashboard responsibilities shall remain separated.

#### NFR-015

Python code shall pass the configured Ruff checks.

#### NFR-016

Backend behaviour shall be covered by automated tests.

#### NFR-017

TypeScript shall compile without errors before producing the frontend build.

#### NFR-018

Source code shall use meaningful module, function, and data-model names.

### 8.5 Portability

#### NFR-019

The complete application shall run using Docker Compose on a supported Docker host.

#### NFR-020

Development commands shall support Windows PowerShell and standard CI Linux environments.

#### NFR-021

The dashboard shall work in current major web browsers.

### 8.6 Usability

#### NFR-022

Users shall be able to identify the latest architectural status from the main dashboard.

#### NFR-023

Blocked and conformant scans shall be visually distinguishable.

#### NFR-024

Violation evidence shall identify what rule failed and where it failed.

#### NFR-025

The interface shall avoid unnecessary implementation-specific text.

#### NFR-026

The dashboard shall provide responsive layouts for smaller screens.

### 8.7 Scalability

#### NFR-027

The persistence model shall support multiple scan records and multiple violations per scan.

#### NFR-028

The scanner design should permit additional services and architectural layers.

#### NFR-029

Scan-history queries shall support a result limit.

### 8.8 Auditability

#### NFR-030

Each persisted scan shall contain a generation timestamp.

#### NFR-031

Each violation shall be traceable to a source file and line number.

#### NFR-032

Historical scan evidence shall remain retrievable independently of the latest report file.

### 8.9 Testability

#### NFR-033

Core components shall expose deterministic functions that can be tested independently.

#### NFR-034

Database tests shall support an isolated in-memory SQLite database.

#### NFR-035

API tests shall support dependency overriding for isolated test sessions.

#### NFR-036

The project shall include both conformant and blocked scan test scenarios.

---

## 9. Use-Case Model

### 9.1 Actor Summary

| Actor | Responsibilities |
|---|---|
| Developer | Run scans and correct violations |
| Software architect | Define rules and review conformance |
| Technical lead | Review history and release status |
| DevOps engineer | Operate deployment and CI |
| CI system | Automatically validate changes |

### 9.2 Use-Case Summary

| ID | Use case | Primary actor |
|---|---|---|
| UC-01 | Run architecture scan | Developer |
| UC-02 | Review latest conformance status | Developer |
| UC-03 | Review scan history | Technical lead |
| UC-04 | Inspect scan evidence | Software architect |
| UC-05 | Validate architecture rules | Software architect |
| UC-06 | Execute CI checks | CI system |
| UC-07 | Start containerised platform | DevOps engineer |
| UC-08 | Verify service health | DevOps engineer |

---

## 10. Detailed Use Cases

### UC-01: Run Architecture Scan

| Item | Description |
|---|---|
| Primary actor | Developer |
| Goal | Analyse configured services and record a new conformance result |
| Trigger | User selects Run Scan or executes the CLI |
| Preconditions | Rules exist, source paths exist and dependencies are available |
| Postconditions | Report is generated; API scans are persisted |
| Priority | Must |

#### Main Flow

1. The actor starts a scan.
2. The system loads the YAML architecture rules.
3. The system validates the rule configuration.
4. The system scans every configured service.
5. The system parses Python files.
6. The system discovers internal dependencies.
7. The system evaluates the dependencies.
8. The system generates violation evidence.
9. The system calculates summary values.
10. The system determines blocking status.
11. The system generates the report.
12. The API stores the scan and violations.
13. The dashboard displays the new result.

#### Alternative Flows

- If the rule file is invalid, the system reports a validation error.
- If a Python file has invalid syntax, the system reports the affected file.
- If PostgreSQL is unavailable, the API returns a failure and does not report successful persistence.
- If a blocking violation exists, the scan is marked Blocked.

### UC-02: Review Latest Conformance Status

| Item | Description |
|---|---|
| Primary actor | Developer |
| Goal | Determine whether the latest architecture is conformant |
| Preconditions | Dashboard and API are available |
| Postconditions | Latest scan information is displayed |
| Priority | Must |

#### Main Flow

1. The actor opens the dashboard.
2. The dashboard requests the latest scan.
3. The API retrieves the latest persisted scan.
4. The dashboard displays summary metrics.
5. The dashboard displays Conformant or Release Blocked status.

#### Alternative Flow

If no scan exists, the dashboard displays No Scan Available.

### UC-03: Review Scan History

| Item | Description |
|---|---|
| Primary actor | Technical lead |
| Goal | Review previous architectural results |
| Preconditions | At least one scan has been persisted |
| Postconditions | Historical scans are displayed newest first |
| Priority | Must |

#### Main Flow

1. The actor opens the dashboard.
2. The dashboard requests scan history.
3. The API retrieves persisted scans.
4. The dashboard displays scan dates, metrics, and statuses.

### UC-04: Inspect Scan Evidence

| Item | Description |
|---|---|
| Primary actor | Software architect |
| Goal | Understand why a scan passed or failed |
| Preconditions | A history row exists |
| Postconditions | The evidence panel displays the selected scan |
| Priority | Must |

#### Main Flow

1. The actor selects a scan-history row.
2. The dashboard requests the selected scan.
3. The API retrieves the scan and related violations.
4. The dashboard highlights the selected row.
5. The dashboard displays scan metadata.
6. For a blocked scan, the dashboard displays violation evidence.
7. For a conformant scan, the dashboard confirms no violations were recorded.

#### Alternative Flow

If the selected scan no longer exists, the dashboard displays an error.

### UC-05: Validate Architecture Rules

| Item | Description |
|---|---|
| Primary actor | Software architect |
| Goal | Confirm that the rule baseline is structurally valid |
| Preconditions | A YAML rules file exists |
| Postconditions | Valid rules are loaded or validation errors are returned |
| Priority | Must |

### UC-06: Execute CI Checks

| Item | Description |
|---|---|
| Primary actor | CI system |
| Goal | Validate source quality, behaviour, architecture and frontend build |
| Trigger | Push or pull request against `main` |
| Postconditions | Workflow passes or blocks the change |
| Priority | Must |

#### Main Flow

1. CI checks out the repository.
2. CI configures Python.
3. CI installs backend dependencies.
4. CI runs Ruff.
5. CI runs backend tests.
6. CI runs the conformance scan.
7. CI displays the report.
8. CI configures Node.js.
9. CI installs frontend dependencies.
10. CI builds the production dashboard.
11. CI reports the final workflow status.

### UC-07: Start Containerised Platform

| Item | Description |
|---|---|
| Primary actor | DevOps engineer |
| Goal | Start all platform components |
| Preconditions | Docker is installed and required ports are available |
| Postconditions | All configured containers are running |
| Priority | Must |

### UC-08: Verify Service Health

| Item | Description |
|---|---|
| Primary actor | DevOps engineer |
| Goal | Confirm that the API and supporting services are operational |
| Preconditions | Containers have started |
| Postconditions | Service health status is known |
| Priority | Must |

---

## 11. Error Handling Requirements

### ER-001

Invalid YAML shall produce a clear validation message.

### ER-002

Invalid Python syntax shall identify the affected source file.

### ER-003

An unavailable database shall produce an API failure rather than a false success.

### ER-004

An unknown scan identifier shall return HTTP `404`.

### ER-005

Absence of all scans shall return HTTP `404` from the latest-scan endpoint.

### ER-006

Frontend API failures shall be displayed without destroying previously rendered layout.

### ER-007

A failed frontend request shall not create fabricated scan data.

### ER-008

CI shall expose generated report output for diagnosis when possible.

---

## 12. Acceptance Criteria

### AC-001: Valid rule loading

Given a valid architecture baseline, when rules are loaded, then strict validation succeeds.

### AC-002: Invalid rule rejection

Given an invalid or unknown rule field, when rules are loaded, then validation fails with a meaningful error.

### AC-003: Dependency detection

Given an API module importing an internal service module, when the service is scanned, then the dependency is recorded with source and target layers.

### AC-004: External dependency filtering

Given a file importing a third-party library, when it is scanned, then no internal architectural dependency is created for that import.

### AC-005: Violation detection

Given a forbidden API-to-repository import, when the scan runs, then one layer violation is generated.

### AC-006: Evidence generation

Given a detected violation, the result shall contain the service, source file, line, layers, target module, severity, type, evidence type, and violation identifier.

### AC-007: Conformant scan

Given no forbidden dependencies, when the scan completes, then the scan is not blocking.

### AC-008: Blocked scan

Given a blocking violation, when the scan completes, then blocking is true and the CLI returns exit code `1`.

### AC-009: Persistence

Given a completed API scan, when persistence succeeds, then its summary and violations can be retrieved later.

### AC-010: Latest scan retrieval

Given multiple persisted scans, when the latest scan is requested, then the newest scan is returned.

### AC-011: Scan-detail retrieval

Given a valid scan identifier, when scan details are requested, then the scan and all associated violations are returned.

### AC-012: Missing scan handling

Given an unknown scan identifier, when details are requested, then HTTP `404` is returned.

### AC-013: Dashboard summary

Given a persisted scan, when the dashboard loads, then its summary metrics and conformance status are displayed.

### AC-014: Conformant evidence panel

Given a conformant history record, when the row is selected, then the panel states that no violations were recorded.

### AC-015: Blocked evidence panel

Given a blocked history record, when the row is selected, then complete violation evidence is displayed.

### AC-016: Containerised operation

Given Docker is available and ports are free, when Docker Compose starts, then PostgreSQL, the API, dashboard, and sample services become available.

### AC-017: Continuous integration

Given a conformant commit, when the GitHub Actions workflow runs, then linting, tests, architecture validation, and dashboard build pass.

### AC-018: CI blocking

Given a blocking violation, when the GitHub Actions workflow runs the scanner, then the workflow fails.

---

## 13. Requirements Traceability Matrix

| Objective | Related requirements | Verification |
|---|---|---|
| Machine-readable rules | FR-001–FR-006 | Rule-loader tests |
| Python static analysis | FR-007–FR-017 | Scanner tests |
| Detect violations | FR-018–FR-026 | Evaluator tests |
| Generate reports | FR-027–FR-033 | CLI tests |
| Persist history | FR-034–FR-043 | Repository tests |
| Provide REST API | FR-044–FR-053 | API tests |
| Provide dashboard | FR-054–FR-071 | Build and manual UI verification |
| Containerised execution | FR-072–FR-080 | Docker Compose verification |
| Automated validation | FR-081–FR-089 | GitHub Actions |
| Security and quality | NFR-008–NFR-018 | Review, Ruff and tests |
| Auditability | NFR-030–NFR-032 | Evidence retrieval tests |

---

## 14. Verification Strategy

| Requirement category | Verification method |
|---|---|
| Rule validation | Automated unit tests |
| Static scanning | Automated unit tests |
| Rule evaluation | Automated unit tests |
| CLI behaviour | Automated integration tests |
| Database persistence | Repository tests |
| REST API | FastAPI TestClient tests |
| Dashboard behaviour | Manual functional verification |
| Frontend compilation | TypeScript and Vite production build |
| Container services | Docker Compose health checks |
| CI process | GitHub Actions workflow |
| User interface | Desktop and responsive visual review |

---

## 15. MVP Completion Criteria

The MVP is complete when:

- Architecture rules are loaded and validated.
- Python services are scanned statically.
- Internal layer dependencies are identified.
- Forbidden dependencies produce violations.
- Conformant and blocked outcomes are supported.
- Reports contain actionable evidence.
- Scan results are stored in PostgreSQL.
- REST endpoints expose current and historical results.
- The dashboard presents metrics, trends, history, and evidence.
- The platform runs with Docker Compose.
- Automated tests pass.
- Ruff passes.
- The frontend production build succeeds.
- GitHub Actions reports successful validation for conformant code.

---

## 16. Future Enhancements

Possible future enhancements include:

- Runtime conformance analysis using OpenTelemetry traces
- Jaeger integration for distributed dependency evidence
- Java, JavaScript, and TypeScript scanners
- Authentication and role-based access control
- Multiple projects and rule sets
- GitHub pull-request annotations
- Email, Slack, or Microsoft Teams notifications
- Architecture dependency visualisation
- Technical-debt scoring
- Violation assignment and remediation workflow
- Configurable data-retention policies
- Kubernetes deployment
- Exportable PDF compliance reports
- Rule-authoring interface
- Comparison between any two scans

---

## 17. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Student/Developer |  |  |  |
| Project Guide |  |  |  |
| Project Manager |  |  |  |
| Evaluator |  |  |  |

---

## 18. Conclusion

This SRS defines the MVP requirements of the Architecture Conformance Monitor. It provides a formal foundation for system design, implementation, testing, diagrams, reporting, demonstration, and academic evaluation.

The requirements connect the original problem—architectural drift and hidden technical debt—to measurable system behaviour. Every major requirement can be verified using automated testing, CI results, API responses, database records, dashboard behaviour, or container health checks.