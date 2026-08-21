# Test Plan and Test-Case Report

## Architecture Conformance Monitor

| Document Information | Details |
|---|---|
| Project | Architecture Conformance Monitor |
| Document Type | Test Plan and Test-Case Report |
| Version | 1.0 |
| Prepared By | Project Team |
| Academic Subject | Software Engineering |
| Test Environment | Python 3.12, React, PostgreSQL, Docker Compose |
| Repository | `axion-5025/architecture-conformance-monitor` |
| Status | Completed |

---

## 1. Introduction

The Architecture Conformance Monitor is a software engineering platform that scans Python microservices, identifies architectural dependencies, evaluates them against predefined architecture rules, detects violations, stores scan results, and presents the results through a web dashboard.

This document defines the testing strategy, test environment, test cases, expected results, actual results, and acceptance criteria used to verify the system.

Testing covers the following system components:

- Architecture rule loader
- Python static dependency scanner
- Architecture rule evaluator
- Command-line interface
- REST API
- PostgreSQL persistence layer
- React dashboard
- Docker deployment
- GitHub Actions continuous integration workflow
- Conformant and non-conformant architecture scenarios

---

## 2. Purpose

The purpose of this test plan is to verify that the Architecture Conformance Monitor:

1. Loads and validates architecture rules correctly.
2. Scans Python microservices accurately.
3. Detects internal architectural dependencies.
4. Ignores external library dependencies.
5. Detects forbidden layer relationships.
6. reports conformant and blocked architecture states.
7. Stores scan history and violation evidence.
8. Exposes scan functionality through REST APIs.
9. Displays scan results correctly on the dashboard.
10. runs consistently in local, Docker, and CI environments.

---

## 3. Testing Objectives

The primary testing objectives are:

- Verify all functional requirements defined in the SRS.
- Validate the correctness of dependency detection.
- Confirm that architecture violations are reported with evidence.
- Verify that scan results are persisted correctly.
- Confirm that API endpoints return valid responses and status codes.
- Validate the frontend production build.
- Verify integration between the frontend, backend, and database.
- Confirm that containers start and pass their health checks.
- Ensure automated quality checks run successfully in GitHub Actions.
- Prevent regressions when the implementation changes.

---

## 4. Scope of Testing

### 4.1 Features Included

The following features are included in testing:

- YAML architecture-rule loading
- Rule-schema validation
- Service-reference validation
- Shared-database ownership validation
- Unknown-field rejection
- Python source-file discovery
- Abstract Syntax Tree parsing
- Local import detection
- External import filtering
- Layer identification
- Forbidden dependency evaluation
- Violation evidence generation
- JSON report generation
- CLI exit-code behavior
- REST API health check
- Scan creation API
- Latest scan API
- Scan-history API
- Individual scan-detail API
- PostgreSQL scan persistence
- Violation-record persistence
- Dashboard metrics
- Conformance-status presentation
- Findings trend chart
- Scan-history table
- Persisted evidence panel
- Docker Compose deployment
- GitHub Actions CI workflow

### 4.2 Features Excluded

The following features are outside the present MVP testing scope:

- Authentication and role-based access control
- Multi-tenant architecture
- Java, JavaScript, Go, or C# source scanning
- Kubernetes deployment
- Distributed tracing validation
- Load testing with thousands of repositories
- Automatic repair of architecture violations
- Remote Git repository scanning
- Email or messaging notifications

---

## 5. Test Strategy

The project uses multiple levels of testing.

### 5.1 Unit Testing

Unit tests verify individual modules in isolation.

Modules covered include:

- Rule models and rule loader
- Python scanner
- Layer evaluator
- Debt-tracker repository
- CLI operations

### 5.2 Integration Testing

Integration tests verify communication between components.

Examples include:

- REST API and database integration
- Scanner and rule evaluator integration
- API and report-generation integration
- Dashboard and REST API integration
- Docker services and PostgreSQL integration

### 5.3 System Testing

System tests verify the complete application workflow:

1. Start the application.
2. Run an architecture scan.
3. Inspect service source files.
4. Evaluate dependencies.
5. Generate the report.
6. Store scan results.
7. Return the result through the API.
8. Display the result in the dashboard.

### 5.4 Regression Testing

The automated test suite runs after implementation changes to ensure that previously working features continue to function correctly.

### 5.5 Static Analysis

Ruff is used to verify:

- Import ordering
- Formatting consistency
- Common Python defects
- Code-quality rules
- Selected security and correctness rules

### 5.6 Build Testing

The React and TypeScript frontend is compiled using:

```powershell
npm run build
```

This verifies:

- TypeScript correctness
- Module resolution
- Component compilation
- Production asset generation

### 5.7 Deployment Testing

Docker Compose is used to verify:

- Image construction
- Container creation
- Container networking
- Port mapping
- PostgreSQL connectivity
- Health checks
- Service startup dependencies

### 5.8 CI Testing

GitHub Actions automatically performs:

- Python dependency installation
- Ruff validation
- Automated tests
- Architecture conformance scan
- Dashboard dependency installation
- Dashboard production build
- Report display

---

## 6. Test Environment

### 6.1 Hardware Environment

| Resource | Minimum Requirement |
|---|---|
| Processor | Dual-core 64-bit processor |
| Memory | 4 GB RAM |
| Storage | 2 GB free space |
| Network | Required for dependency installation and GitHub operations |

### 6.2 Software Environment

| Software | Version/Configuration |
|---|---|
| Operating System | Windows 11 / Ubuntu Linux |
| Python | 3.12 |
| Node.js | 24 or compatible |
| npm | 11 or compatible |
| FastAPI | Python REST framework |
| React | Frontend framework |
| TypeScript | Frontend language |
| PostgreSQL | 18 Alpine container |
| Docker | Docker Desktop/Engine |
| Docker Compose | Compose v2 |
| pytest | Python test framework |
| Ruff | Python static-analysis tool |
| Git | Source-control system |
| GitHub Actions | CI environment |
| Browser | Current Chrome, Edge, or Firefox |

### 6.3 Application Ports

| Component | Port |
|---|---:|
| Production dashboard | 8080 |
| Development dashboard | 5173 |
| Conformance API | 8000 |
| Order service | 8001 |
| Payment service | 8002 |
| Inventory service | 8003 |
| PostgreSQL | 5432 |

---

## 7. Test Data

The test environment uses three sample Python microservices:

- `order-service`
- `payment-service`
- `inventory-service`

The architecture-rule file is:

```text
architecture-rules/baseline.yml
```

A conformant test scenario contains no forbidden dependencies.

A blocked scenario may contain an API-layer import similar to:

```python
from app.repositories.orders import OrderRepository
```

If the baseline rules prohibit the `api` layer from accessing the `repositories` layer directly, this dependency must generate a violation.

---

## 8. Entry Criteria

Testing can begin when:

- The project source code is available.
- Required dependencies are installed.
- The Python virtual environment is active.
- The architecture-rule file exists.
- The sample services are available.
- Docker is installed for container tests.
- The PostgreSQL configuration is available.
- Frontend dependencies are installed.

---

## 9. Exit Criteria

Testing is considered complete when:

- All critical functional test cases pass.
- Ruff reports no remaining errors.
- The pytest suite passes.
- The dashboard production build succeeds.
- All Docker containers become healthy.
- The REST API returns valid responses.
- Both conformant and blocked scans are verified.
- Persisted violation evidence is displayed correctly.
- The GitHub Actions workflow succeeds.
- No unresolved critical or high-severity defect remains.

---

## 10. Test Suspension and Resumption Criteria

Testing must be suspended if:

- The architecture-rule file cannot be loaded.
- The database is unavailable.
- Required dependencies cannot be installed.
- The application cannot start.
- Docker images cannot be built.
- Test data is corrupted.
- A critical defect prevents further testing.

Testing may resume after:

- The blocking defect is corrected.
- The test environment is restored.
- Required services are healthy.
- Test data is reset or recreated.

---

## 11. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Developer | Implements features and resolves defects |
| Tester | Executes test cases and records outcomes |
| Project Manager | Reviews progress and acceptance criteria |
| Repository Maintainer | Reviews commits and CI results |
| End User/Evaluator | Verifies dashboard behavior and usability |

---

## 12. Functional Test Cases

### TC-RULE-001: Load a valid baseline rule file

| Field | Details |
|---|---|
| Test Case ID | TC-RULE-001 |
| Module | Rule Engine |
| Objective | Verify that a valid YAML architecture-rule file loads successfully |
| Preconditions | `architecture-rules/baseline.yml` exists |
| Test Steps | Load the baseline file using the rule loader |
| Expected Result | Application name, language, services, and rules are parsed |
| Actual Result | Valid baseline loaded successfully |
| Status | Passed |
| Automation | `test_loads_valid_baseline` |

### TC-RULE-002: Reject an unknown service reference

| Field | Details |
|---|---|
| Test Case ID | TC-RULE-002 |
| Module | Rule Engine |
| Objective | Ensure rules cannot reference undeclared services |
| Preconditions | Test YAML references an unknown service |
| Test Steps | Attempt to load the invalid rule file |
| Expected Result | Validation error is raised |
| Actual Result | Unknown service reference rejected |
| Status | Passed |
| Automation | `test_rejects_unknown_service_reference` |

### TC-RULE-003: Reject shared database ownership

| Field | Details |
|---|---|
| Test Case ID | TC-RULE-003 |
| Module | Rule Engine |
| Objective | Ensure conflicting database ownership is rejected |
| Preconditions | Two services claim invalid shared ownership |
| Test Steps | Load the invalid architecture-rule configuration |
| Expected Result | Validation error is raised |
| Actual Result | Invalid ownership rejected |
| Status | Passed |
| Automation | `test_rejects_shared_database_ownership` |

### TC-RULE-004: Reject unknown fields

| Field | Details |
|---|---|
| Test Case ID | TC-RULE-004 |
| Module | Rule Engine |
| Objective | Verify strict architecture-rule validation |
| Preconditions | YAML contains an unsupported field |
| Test Steps | Load the invalid YAML file |
| Expected Result | Unknown field is rejected |
| Actual Result | Strict validation rejected the field |
| Status | Passed |
| Automation | `test_rejects_unknown_fields` |

---

### TC-SCAN-001: Detect local layer dependencies

| Field | Details |
|---|---|
| Test Case ID | TC-SCAN-001 |
| Module | Python Scanner |
| Objective | Detect dependencies between internal application layers |
| Preconditions | Python file imports local service and repository modules |
| Test Steps | Scan the service directory |
| Expected Result | Dependencies identify source and target layers |
| Actual Result | Local dependencies detected correctly |
| Status | Passed |
| Automation | `test_detects_local_layer_dependencies` |

### TC-SCAN-002: Ignore external dependencies

| Field | Details |
|---|---|
| Test Case ID | TC-SCAN-002 |
| Module | Python Scanner |
| Objective | Ensure third-party and standard-library imports are not treated as architecture dependencies |
| Preconditions | Source file imports `json`, `httpx`, and `pathlib` |
| Test Steps | Scan the source file |
| Expected Result | No internal dependency is generated |
| Actual Result | External imports ignored |
| Status | Passed |
| Automation | `test_ignores_external_dependencies` |

### TC-SCAN-003: Reject invalid Python source

| Field | Details |
|---|---|
| Test Case ID | TC-SCAN-003 |
| Module | Python Scanner |
| Objective | Verify behavior when Python syntax is invalid |
| Preconditions | Source file contains invalid Python syntax |
| Test Steps | Attempt to scan the service |
| Expected Result | A meaningful `SyntaxError` is raised |
| Actual Result | Invalid Python rejected |
| Status | Passed |
| Automation | `test_rejects_invalid_python` |

---

### TC-EVAL-001: Detect a forbidden layer dependency

| Field | Details |
|---|---|
| Test Case ID | TC-EVAL-001 |
| Module | Rule Evaluator |
| Objective | Verify detection of a dependency prohibited by the baseline |
| Preconditions | API layer directly imports repository layer |
| Test Steps | Scan dependency and evaluate architecture rules |
| Expected Result | A high-severity layer violation is produced |
| Actual Result | Violation detected with source and target evidence |
| Status | Passed |
| Automation | `test_detects_forbidden_layer_dependency` |

---

### TC-CLI-001: Generate a blocking report

| Field | Details |
|---|---|
| Test Case ID | TC-CLI-001 |
| Module | Command-Line Interface |
| Objective | Verify that the CLI reports blocking architecture violations |
| Preconditions | At least one blocking violation exists |
| Test Steps | Run `python -m conformance_platform.cli` |
| Expected Result | JSON report is generated and blocking status is returned |
| Actual Result | Blocking report generated successfully |
| Status | Passed |
| Automation | `test_run_scan_reports_blocking_violation` |

### TC-CLI-002: Return failure exit code for blocking violations

| Field | Details |
|---|---|
| Test Case ID | TC-CLI-002 |
| Module | Command-Line Interface |
| Objective | Verify release-gate behavior |
| Preconditions | Blocking violation exists |
| Test Steps | Execute the CLI and inspect its exit code |
| Expected Result | Exit code is `1` |
| Actual Result | CLI returned the expected code |
| Status | Passed |
| Automation | `test_cli_returns_one_for_blocking_violation` |

---

### TC-DB-001: Save a scan and its violation

| Field | Details |
|---|---|
| Test Case ID | TC-DB-001 |
| Module | Debt Tracker |
| Objective | Verify persistence of a scan and violation evidence |
| Preconditions | Database tables exist |
| Test Steps | Save a report containing one violation |
| Expected Result | Scan and child violation records are stored |
| Actual Result | Scan and violation saved |
| Status | Passed |
| Automation | `test_saves_scan_and_violation` |

### TC-DB-002: Return the latest scan first

| Field | Details |
|---|---|
| Test Case ID | TC-DB-002 |
| Module | Debt Tracker |
| Objective | Verify scan ordering |
| Preconditions | Multiple scans exist |
| Test Steps | Request the latest scan and scan list |
| Expected Result | Most recently generated scan is returned first |
| Actual Result | Latest scan returned correctly |
| Status | Passed |
| Automation | `test_returns_latest_scan_first` |

### TC-DB-003: Retrieve scan details by ID

| Field | Details |
|---|---|
| Test Case ID | TC-DB-003 |
| Module | Debt Tracker |
| Objective | Verify retrieval of persisted scan evidence |
| Preconditions | Scan containing a violation exists |
| Test Steps | Request the scan by its identifier |
| Expected Result | Scan and associated violations are returned |
| Actual Result | Persisted scan evidence returned |
| Status | Passed |
| Automation | `test_returns_scan_by_id_with_violations` |

### TC-DB-004: Return no result for unknown scan ID

| Field | Details |
|---|---|
| Test Case ID | TC-DB-004 |
| Module | Debt Tracker |
| Objective | Verify behavior for a nonexistent scan |
| Preconditions | Requested identifier does not exist |
| Test Steps | Request the unknown scan identifier |
| Expected Result | Repository returns `None` |
| Actual Result | Unknown scan was not returned |
| Status | Passed |
| Automation | `test_returns_none_when_scan_id_does_not_exist` |

### TC-DB-005: Limit scan-history results

| Field | Details |
|---|---|
| Test Case ID | TC-DB-005 |
| Module | Debt Tracker |
| Objective | Verify history result limiting |
| Preconditions | Multiple scan records exist |
| Test Steps | Request history with a result limit |
| Expected Result | Returned list does not exceed the specified limit |
| Actual Result | History limit applied |
| Status | Passed |
| Automation | `test_limits_scan_history_results` |

---

### TC-API-001: Verify API health

| Field | Details |
|---|---|
| Test Case ID | TC-API-001 |
| Module | REST API |
| Endpoint | `GET /health` |
| Objective | Verify that the API is available |
| Expected Result | HTTP 200 with service, version, and healthy status |
| Actual Result | Health response returned |
| Status | Passed |
| Automation | `test_health_endpoint` |

### TC-API-002: Create, retrieve, and list a scan

| Field | Details |
|---|---|
| Test Case ID | TC-API-002 |
| Module | REST API |
| Endpoints | `POST /api/v1/scans`, `GET /api/v1/scans/latest`, `GET /api/v1/scans/history` |
| Objective | Verify the primary API workflow |
| Preconditions | Rules and sample services exist |
| Test Steps | Create a scan, retrieve the latest scan, and retrieve history |
| Expected Result | Consistent persisted data is returned |
| Actual Result | Complete API workflow succeeded |
| Status | Passed |
| Automation | `test_creates_retrieves_and_lists_scan` |

### TC-API-003: Retrieve latest scan without report file

| Field | Details |
|---|---|
| Test Case ID | TC-API-003 |
| Module | REST API |
| Endpoint | `GET /api/v1/scans/latest` |
| Objective | Verify database-backed retrieval when the local report file is missing |
| Preconditions | Scan exists in the database but report file is unavailable |
| Expected Result | Latest stored scan is reconstructed and returned |
| Actual Result | Stored scan returned |
| Status | Passed |
| Automation | `test_latest_scan_uses_database_when_report_file_is_missing` |

### TC-API-004: Retrieve stored violation details

| Field | Details |
|---|---|
| Test Case ID | TC-API-004 |
| Module | REST API |
| Endpoint | `GET /api/v1/scans/{scan_id}` |
| Objective | Verify persisted evidence retrieval |
| Preconditions | Blocking scan with a violation exists |
| Expected Result | Response contains violation type, severity, source, layers, module, evidence type, and ID |
| Actual Result | Complete violation evidence returned |
| Status | Passed |
| Automation | `test_returns_stored_violation_details` |

### TC-API-005: Return 404 when no latest scan exists

| Field | Details |
|---|---|
| Test Case ID | TC-API-005 |
| Module | REST API |
| Endpoint | `GET /api/v1/scans/latest` |
| Objective | Verify missing-data handling |
| Preconditions | No scan exists |
| Expected Result | HTTP 404 with a meaningful error message |
| Actual Result | HTTP 404 returned |
| Status | Passed |
| Automation | `test_latest_scan_returns_404_when_missing` |

### TC-API-006: Return 404 for an unknown scan ID

| Field | Details |
|---|---|
| Test Case ID | TC-API-006 |
| Module | REST API |
| Endpoint | `GET /api/v1/scans/{scan_id}` |
| Objective | Verify invalid scan-detail requests |
| Preconditions | Requested scan does not exist |
| Expected Result | HTTP 404 |
| Actual Result | HTTP 404 returned |
| Status | Passed |
| Automation | `test_scan_detail_returns_404_when_missing` |

---

## 13. Frontend Test Cases

### TC-UI-001: Load dashboard data

| Field | Details |
|---|---|
| Test Case ID | TC-UI-001 |
| Module | React Dashboard |
| Objective | Verify retrieval and display of latest scan and history |
| Test Steps | Open dashboard while backend is running |
| Expected Result | Metrics and history load without an error |
| Actual Result | Dashboard loaded successfully |
| Status | Passed |
| Type | Manual integration test |

### TC-UI-002: Run architecture scan

| Field | Details |
|---|---|
| Test Case ID | TC-UI-002 |
| Module | React Dashboard |
| Objective | Verify scan execution from the user interface |
| Test Steps | Click **Run scan** |
| Expected Result | Button enters scanning state and dashboard refreshes |
| Actual Result | Scan created and dashboard updated |
| Status | Passed |
| Type | Manual system test |

### TC-UI-003: Display conformant scan

| Field | Details |
|---|---|
| Test Case ID | TC-UI-003 |
| Module | React Dashboard |
| Objective | Verify presentation of a scan with no violation |
| Preconditions | Source architecture is conformant |
| Test Steps | Run scan and inspect result |
| Expected Result | Green conformant status and zero violations appear |
| Actual Result | Conformant state displayed |
| Status | Passed |
| Type | Manual system test |

### TC-UI-004: Display blocked scan

| Field | Details |
|---|---|
| Test Case ID | TC-UI-004 |
| Module | React Dashboard |
| Objective | Verify presentation of a blocking violation |
| Preconditions | A forbidden layer dependency exists |
| Test Steps | Run scan and inspect dashboard |
| Expected Result | Red blocked status and violation count appear |
| Actual Result | Blocked state displayed |
| Status | Passed |
| Type | Manual system test |

### TC-UI-005: Display conformant evidence panel

| Field | Details |
|---|---|
| Test Case ID | TC-UI-005 |
| Module | Scan History |
| Objective | Verify evidence display for a conformant scan |
| Test Steps | Select a conformant scan from history |
| Expected Result | Panel displays scan metadata and “No violations recorded” |
| Actual Result | Conformant evidence panel displayed |
| Status | Passed |
| Type | Manual system test |

### TC-UI-006: Display blocked evidence panel

| Field | Details |
|---|---|
| Test Case ID | TC-UI-006 |
| Module | Scan History |
| Objective | Verify detailed violation evidence |
| Test Steps | Select a blocked scan from history |
| Expected Result | Panel displays severity, message, service, source file, dependency, target module, evidence type, and violation ID |
| Actual Result | Complete violation evidence displayed |
| Status | Passed |
| Type | Manual system test |

### TC-UI-007: Close evidence panel

| Field | Details |
|---|---|
| Test Case ID | TC-UI-007 |
| Module | Scan History |
| Objective | Verify evidence-panel interaction |
| Test Steps | Open a scan and click the close button |
| Expected Result | Evidence panel closes |
| Actual Result | Panel closed successfully |
| Status | Passed |
| Type | Manual UI test |

### TC-UI-008: Build production frontend

| Field | Details |
|---|---|
| Test Case ID | TC-UI-008 |
| Module | React Dashboard |
| Objective | Verify production compilation |
| Test Steps | Run `npm run build` |
| Expected Result | TypeScript and Vite build complete successfully |
| Actual Result | Production assets generated in `dist` |
| Status | Passed |
| Note | Bundle-size warning is non-blocking |

---

## 14. Docker and Deployment Test Cases

### TC-DEP-001: Validate Docker Compose configuration

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-001 |
| Objective | Verify Compose syntax and resolved configuration |
| Command | `docker compose config` |
| Expected Result | Valid configuration is printed without errors |
| Actual Result | Configuration validated |
| Status | Passed |

### TC-DEP-002: Build application images

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-002 |
| Objective | Verify all required images can be constructed |
| Command | `docker compose build` |
| Expected Result | Images build successfully |
| Actual Result | Images built |
| Status | Passed |

### TC-DEP-003: Start backend containers

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-003 |
| Objective | Verify backend deployment |
| Command | `docker compose up -d --build` |
| Expected Result | API, services, and database containers start |
| Actual Result | Containers started |
| Status | Passed |

### TC-DEP-004: Verify container health

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-004 |
| Objective | Verify runtime availability |
| Command | `docker compose ps` |
| Expected Result | Required containers show a healthy status |
| Actual Result | Containers reported healthy |
| Status | Passed |

### TC-DEP-005: Verify PostgreSQL readiness

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-005 |
| Objective | Verify database availability |
| Command | `docker compose exec postgres pg_isready -U architecture_user -d architecture_monitor` |
| Expected Result | PostgreSQL reports that it is accepting connections |
| Actual Result | Database accepted connections |
| Status | Passed |

### TC-DEP-006: Serve production dashboard container

| Field | Details |
|---|---|
| Test Case ID | TC-DEP-006 |
| Objective | Verify the dashboard production container |
| Test Steps | Start dashboard service and open its mapped URL |
| Expected Result | Nginx serves the compiled React dashboard |
| Actual Result | Dashboard served successfully |
| Status | Passed |

---

## 15. CI Test Cases

### TC-CI-001: Trigger workflow on main-branch push

| Field | Details |
|---|---|
| Test Case ID | TC-CI-001 |
| Objective | Verify automated CI execution |
| Test Steps | Push a commit to `main` |
| Expected Result | Architecture CI workflow starts |
| Actual Result | Workflow triggered |
| Status | Passed |

### TC-CI-002: Run Python quality checks

| Field | Details |
|---|---|
| Test Case ID | TC-CI-002 |
| Objective | Verify automated Ruff and pytest execution |
| Expected Result | Ruff and all Python tests pass |
| Actual Result | Checks passed |
| Status | Passed |

### TC-CI-003: Validate architecture scan in CI

| Field | Details |
|---|---|
| Test Case ID | TC-CI-003 |
| Objective | Verify automated architecture enforcement |
| Expected Result | Conformance report is generated and displayed |
| Actual Result | Report generated |
| Status | Passed |

### TC-CI-004: Validate dashboard production build in CI

| Field | Details |
|---|---|
| Test Case ID | TC-CI-004 |
| Objective | Ensure frontend changes remain deployable |
| Expected Result | `npm ci` and `npm run build` complete successfully |
| Actual Result | Production build passed |
| Status | Passed |

---

## 16. Requirements Traceability Matrix

| Requirement ID | Requirement Summary | Test Cases |
|---|---|---|
| FR-01 | Load architecture rules | TC-RULE-001 |
| FR-02 | Validate rule schema | TC-RULE-002, TC-RULE-003, TC-RULE-004 |
| FR-03 | Scan registered Python services | TC-SCAN-001, TC-SCAN-003 |
| FR-04 | Detect internal dependencies | TC-SCAN-001 |
| FR-05 | Ignore external dependencies | TC-SCAN-002 |
| FR-06 | Evaluate layer rules | TC-EVAL-001 |
| FR-07 | Generate violation evidence | TC-EVAL-001, TC-API-004 |
| FR-08 | Generate JSON report | TC-CLI-001 |
| FR-09 | Provide CLI release gate | TC-CLI-002 |
| FR-10 | Create scan through API | TC-API-002 |
| FR-11 | Retrieve latest scan | TC-API-002, TC-API-003 |
| FR-12 | Retrieve scan history | TC-API-002 |
| FR-13 | Retrieve scan details | TC-API-004, TC-API-006 |
| FR-14 | Persist scan records | TC-DB-001, TC-DB-002 |
| FR-15 | Persist violations | TC-DB-001, TC-DB-003 |
| FR-16 | Display dashboard metrics | TC-UI-001 |
| FR-17 | Display conformance status | TC-UI-003, TC-UI-004 |
| FR-18 | Display findings trend | TC-UI-001 |
| FR-19 | Display persisted evidence | TC-UI-005, TC-UI-006 |
| FR-20 | Automate checks in CI | TC-CI-001 through TC-CI-004 |
| NFR-01 | Maintainability | TC-CI-002 |
| NFR-02 | Portability | TC-DEP-001 through TC-DEP-006 |
| NFR-03 | Reliability | TC-API-005, TC-API-006 |
| NFR-04 | Usability | TC-UI-001 through TC-UI-007 |
| NFR-05 | Data integrity | TC-DB-001 through TC-DB-005 |

---

## 17. Automated Test Execution

### 17.1 Activate the Python environment

```powershell
cd C:\architecture-conformance-monitor
.\venv\Scripts\Activate.ps1
```

### 17.2 Run static analysis

```powershell
python -m ruff check conformance_platform tests
```

Expected output:

```text
All checks passed!
```

### 17.3 Run the complete Python test suite

```powershell
python -m pytest -v
```

Verified result:

```text
21 passed
```

A Starlette test-client deprecation warning may be displayed. This warning originates from a dependency and does not represent a failing application test.

### 17.4 Build the frontend

```powershell
cd dashboard
npm ci
npm run build
```

Expected result:

```text
built successfully
```

The generated JavaScript chunk may exceed 500 KB. This is a performance warning and does not prevent production compilation.

### 17.5 Validate containers

```powershell
cd C:\architecture-conformance-monitor
docker compose config
docker compose up -d --build
docker compose ps
```

### 17.6 Check the API

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected response:

```text
service                     version status
-------                     ------- ------
conformance-platform-api    0.3.0   healthy
```

---

## 18. Test Execution Summary

| Test Category | Result |
|---|---|
| Architecture-rule tests | Passed |
| Python scanner tests | Passed |
| Rule evaluator tests | Passed |
| CLI tests | Passed |
| Persistence tests | Passed |
| REST API tests | Passed |
| Automated Python tests | 21 passed |
| Static analysis | Passed |
| Frontend production build | Passed |
| Conformant UI scenario | Passed |
| Blocked UI scenario | Passed |
| Evidence-panel verification | Passed |
| Docker deployment | Passed |
| GitHub Actions workflow | Passed |

---

## 19. Defect Summary

| Defect | Cause | Resolution | Status |
|---|---|---|---|
| Virtual environment activation failed | Incomplete or locked environment | Recreated and activated environment | Closed |
| GitHub repository not found | Remote repository was not created or URL was incorrect | Created repository and corrected remote URL | Closed |
| Empty Compose file | Compose content had not been saved | Added valid service definitions | Closed |
| Docker port 8080 conflict | Another container already used the port | Identified conflicting container and adjusted runtime state | Closed |
| Ruff import-order errors | Imports were not normalized | Applied Ruff fixes | Closed |
| Ruff `B008` errors | FastAPI `Depends` used directly in defaults | Introduced an `Annotated` session dependency | Closed |
| API test mismatch | API contract changed after persistence improvements | Updated tests to current behavior | Closed |
| Missing Python dependency | Virtual environment was inactive | Activated the correct environment | Closed |
| Dashboard initially showed zero values | Backend was unavailable or scan was not loaded | Started containers and refreshed dashboard | Closed |
| Bundle-size warning | Recharts and frontend dependencies increased bundle size | Accepted for MVP; future code splitting recommended | Open, non-blocking |
| Test-client deprecation warning | Dependency-level Starlette/FastAPI behavior | Recorded for future dependency upgrade | Open, non-blocking |

---

## 20. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Scanner misses dynamic imports | Medium | Medium | Document static-analysis limitation |
| Invalid YAML blocks scans | Low | High | Strict validation and automated rule tests |
| Database unavailable | Low | High | Health checks and startup dependency |
| Port conflicts | Medium | Medium | Configurable port mappings |
| Large frontend bundle | Medium | Low | Future dynamic imports and code splitting |
| Incorrect architecture rules | Medium | High | Review and version rule files |
| Unsupported programming language | High outside MVP | Medium | Python-only scope is documented |
| Corrupt scan data | Low | High | SQLAlchemy transactions and database constraints |

---

## 21. Acceptance Criteria

The project is accepted when:

1. A valid architecture baseline loads successfully.
2. Invalid architecture rules are rejected.
3. Python services are scanned.
4. Internal dependencies are identified.
5. Forbidden dependencies generate violations.
6. Conformant scans contain no blocking violations.
7. Blocking scans contain actionable evidence.
8. Scan history is stored in PostgreSQL.
9. REST API endpoints return expected results.
10. Dashboard metrics reflect the latest scan.
11. Users can inspect conformant and blocked scan evidence.
12. Python quality and automated tests pass.
13. The React production build completes.
14. Docker services start and become healthy.
15. GitHub Actions completes successfully.

All critical acceptance criteria were satisfied during MVP verification.

---

## 22. Final Test Conclusion

The Architecture Conformance Monitor was tested at unit, integration, system, deployment, and continuous-integration levels.

The verified system can:

- Scan three sample Python microservices.
- Detect internal architectural dependencies.
- Evaluate dependencies against a declared baseline.
- Distinguish conformant and blocked architectures.
- Produce actionable violation evidence.
- Persist scan history and violation records.
- Expose scan operations through REST endpoints.
- Display scan metrics, trends, history, and evidence.
- Run using Docker Compose.
- Execute automated quality checks through GitHub Actions.

The automated Python suite completed with **21 passing tests**. Static analysis passed, the frontend production build succeeded, Docker services became healthy, and GitHub Actions completed successfully.

Therefore, the Architecture Conformance Monitor MVP satisfies its defined testing and acceptance criteria and is suitable for academic demonstration and evaluation.