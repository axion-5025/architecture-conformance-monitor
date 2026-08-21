# Sequence Diagrams

## Architecture Conformance Monitor

**Document Type:** UML Sequence Diagram Specification  
**Project:** Architecture Conformance Monitor  
**Version:** 1.0

---

## 1. Purpose

This document describes the time-ordered interactions between users, frontend components, backend services, the architecture scanning engine, and the PostgreSQL database.

The diagrams cover the following major workflows:

1. Loading the monitoring dashboard
2. Running an architecture conformance scan
3. Viewing scan history and violation evidence
4. Executing automated conformance checks through GitHub Actions

---

## 2. System Participants

| Participant | Responsibility |
|---|---|
| Developer | Uses the dashboard and initiates scans |
| React Dashboard | Displays metrics, scan status, trends, history, and evidence |
| FastAPI Backend | Exposes REST endpoints and coordinates scan operations |
| Scan Runner | Executes the end-to-end architecture scan |
| Rule Loader | Loads and validates the YAML architecture baseline |
| Python Scanner | Statically analyzes Python source files |
| Layer Evaluator | Detects prohibited architectural dependencies |
| Scan Repository | Persists and retrieves scan records |
| PostgreSQL | Stores scan summaries and violation evidence |
| GitHub Actions | Executes automated quality and conformance checks |

---

## 3. Dashboard Loading Sequence

### 3.1 Description

When the developer opens the dashboard, the React application requests the latest scan and the scan-history list.

The backend retrieves these records from PostgreSQL and returns them to the dashboard. If no scan exists, the dashboard displays its empty state.

### 3.2 Sequence Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant Repository as Scan Repository
    participant DB as PostgreSQL

    Developer->>Dashboard: Open dashboard
    Dashboard->>API: GET /api/v1/scans/latest
    API->>Repository: get_latest_scan(session)
    Repository->>DB: SELECT latest scan
    DB-->>Repository: Scan record or empty result
    Repository-->>API: Latest scan or None

    alt Latest scan exists
        API-->>Dashboard: 200 ScanResponse
    else No scan exists
        API-->>Dashboard: 404 No scan available
        Dashboard->>Dashboard: Display empty scan state
    end

    Dashboard->>API: GET /api/v1/scans/history
    API->>Repository: list_scans(session)
    Repository->>DB: SELECT scans ordered by date
    DB-->>Repository: Scan records
    Repository-->>API: Scan history list
    API-->>Dashboard: 200 ScanHistoryItem[]
    Dashboard->>Dashboard: Render metrics and history
    Dashboard-->>Developer: Display architecture overview
```

### 3.3 Result

The dashboard displays:

- Latest architecture status
- Services scanned
- Files scanned
- Dependencies detected
- Violations detected
- Findings trend
- Historical scan records

---

## 4. Architecture Scan Execution Sequence

### 4.1 Description

The developer selects **Run scan** from the dashboard.

The backend invokes the scan runner, which loads the YAML rules, scans each registered Python microservice, evaluates dependencies, generates a report, and saves the result in PostgreSQL.

### 4.2 Scan Request and Coordination

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant Runner as Scan Runner
    participant Repository as Scan Repository

    Developer->>Dashboard: Click Run scan
    Dashboard->>Dashboard: Show scanning state
    Dashboard->>API: POST /api/v1/scans
    API->>Runner: run_scan(rules_path, output_path)
    Runner->>Runner: Load rules and scan services
    Runner->>Runner: Evaluate dependencies
    Runner->>Runner: Generate JSON report
    Runner-->>API: Report and blocking status
    API->>Repository: save_scan_report(report, blocking)
    Repository-->>API: Persisted ScanRecord
    API-->>Dashboard: 200 ScanResponse
    Dashboard->>Dashboard: Reload latest scan and history
    Dashboard-->>Developer: Display updated result
```

### 4.3 Internal Scan Processing

```mermaid
sequenceDiagram
    participant Runner as Scan Runner
    participant Loader as Rule Loader
    participant Scanner as Python Scanner
    participant Evaluator as Layer Evaluator
    participant Report as Report Generator

    Runner->>Loader: load_rules(baseline.yml)
    Loader->>Loader: Parse YAML document
    Loader->>Loader: Validate rule model
    Loader-->>Runner: ArchitectureRules

    loop For every configured service
        Runner->>Scanner: scan_service(name, source_path)
        Scanner->>Scanner: Discover Python files

        loop For every Python file
            Scanner->>Scanner: Parse file using AST
            Scanner->>Scanner: Extract local imports
            Scanner->>Scanner: Create dependency evidence
        end

        Scanner-->>Runner: ServiceScanResult
        Runner->>Evaluator: evaluate_layer_dependencies(rules, result)
        Evaluator->>Evaluator: Compare imports with allowed layers
        Evaluator-->>Runner: ArchitectureViolation[]
    end

    Runner->>Report: Build conformance report
    Report->>Report: Calculate summary and blocking status
    Report-->>Runner: JSON-compatible report
```

### 4.4 Alternative Outcomes

```mermaid
sequenceDiagram
    participant Runner as Scan Runner
    participant Scanner as Python Scanner
    participant Evaluator as Layer Evaluator
    participant API as FastAPI Backend
    participant Dashboard as React Dashboard

    Runner->>Scanner: Scan registered services
    Scanner-->>Runner: Dependency evidence
    Runner->>Evaluator: Evaluate evidence

    alt No blocking violation
        Evaluator-->>Runner: Empty blocking-violation list
        Runner-->>API: blocking = false
        API-->>Dashboard: Conformant scan response
        Dashboard->>Dashboard: Show green Conformant status
    else Blocking violation detected
        Evaluator-->>Runner: Blocking violations
        Runner-->>API: blocking = true
        API-->>Dashboard: Blocked scan response
        Dashboard->>Dashboard: Show red Release blocked status
    else Invalid Python source
        Scanner-->>Runner: SyntaxError with source-file evidence
        Runner-->>API: Scan failure
        API-->>Dashboard: Error response
        Dashboard->>Dashboard: Display scan failure message
    end
```

---

## 5. Scan Persistence Sequence

### 5.1 Description

Every completed scan is preserved as an auditable database record.

The scan summary is stored in `scan_records`, while individual violations are stored in `violation_records`.

### 5.2 Sequence Diagram

```mermaid
sequenceDiagram
    participant API as FastAPI Backend
    participant Repository as Scan Repository
    participant Scan as ScanRecord
    participant Violation as ViolationRecord
    participant DB as PostgreSQL

    API->>Repository: save_scan_report(report, blocking)
    Repository->>Scan: Create scan summary entity

    loop For every violation
        Repository->>Violation: Create violation entity
        Violation-->>Scan: Associate with scan record
    end

    Repository->>DB: INSERT scan record
    Repository->>DB: INSERT violation records
    Repository->>DB: COMMIT transaction
    DB-->>Repository: Persisted identifiers
    Repository->>DB: REFRESH scan record
    DB-->>Repository: Complete ScanRecord
    Repository-->>API: Saved scan
```

### 5.3 Transaction Behaviour

If persistence succeeds:

- The scan receives a unique identifier.
- All violation records reference the scan identifier.
- The transaction is committed.
- The API returns the persisted scan identifier.

If persistence fails:

- The transaction is not treated as successful.
- The API does not return a valid scan result.
- The dashboard displays an error state.

---

## 6. Scan History and Evidence Sequence

### 6.1 Description

The developer can select any historical scan from the audit-trail table.

The dashboard requests the complete persisted scan detail. The backend retrieves the scan record and its associated violations from PostgreSQL.

### 6.2 Sequence Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant Repository as Scan Repository
    participant DB as PostgreSQL

    Developer->>Dashboard: Select scan-history row
    Dashboard->>Dashboard: Show evidence loading state
    Dashboard->>API: GET /api/v1/scans/{scan_id}
    API->>Repository: get_scan_by_id(session, scan_id)
    Repository->>DB: SELECT scan with violations
    DB-->>Repository: Scan and violation records

    alt Scan exists
        Repository-->>API: Complete ScanRecord
        API-->>Dashboard: 200 ScanDetailResponse
        Dashboard->>Dashboard: Render evidence panel
        Dashboard-->>Developer: Display scan details
    else Scan does not exist
        Repository-->>API: None
        API-->>Dashboard: 404 Scan not found
        Dashboard-->>Developer: Display retrieval error
    end
```

### 6.3 Conformant Evidence Panel

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant DB as PostgreSQL

    Developer->>Dashboard: Select conformant scan
    Dashboard->>API: Request scan details
    API->>DB: Retrieve scan and violations
    DB-->>API: Scan with empty violation list
    API-->>Dashboard: Scan detail, blocking = false
    Dashboard->>Dashboard: Build conformant evidence view
    Dashboard-->>Developer: Show No violations recorded
```

### 6.4 Blocked Evidence Panel

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant DB as PostgreSQL

    Developer->>Dashboard: Select blocked scan
    Dashboard->>API: Request scan details
    API->>DB: Retrieve scan and violations
    DB-->>API: Scan with violation records
    API-->>Dashboard: Scan detail, blocking = true
    Dashboard->>Dashboard: Render violation cards
    Dashboard-->>Developer: Show source and dependency evidence
```

### 6.5 Evidence Displayed

For a blocked scan, the dashboard displays:

- Violation type
- Severity
- Service name
- Human-readable message
- Source file
- Line number
- Source layer
- Target layer
- Target module
- Evidence type
- Unique violation identifier

---

## 7. GitHub Actions CI Sequence

### 7.1 Description

Every push or pull request targeting the `main` branch starts the Architecture CI workflow.

The workflow validates backend quality, automated tests, dashboard compilation, and architecture conformance.

### 7.2 Sequence Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant GitHub as GitHub Repository
    participant Actions as GitHub Actions
    participant Quality as Quality Checks
    participant Scanner as Conformance CLI

    Developer->>GitHub: Push commit or open pull request
    GitHub->>Actions: Trigger Architecture CI
    Actions->>Actions: Check out repository
    Actions->>Actions: Set up Python and Node.js
    Actions->>Quality: Run Ruff
    Quality-->>Actions: Lint result
    Actions->>Quality: Run Pytest
    Quality-->>Actions: Test result
    Actions->>Quality: Build React dashboard
    Quality-->>Actions: Production-build result
    Actions->>Scanner: Run architecture scan
    Scanner-->>Actions: Report and process exit code

    alt Every check succeeds
        Actions-->>GitHub: Mark workflow successful
        GitHub-->>Developer: Green CI status
    else Any check fails
        Actions-->>GitHub: Mark workflow failed
        GitHub-->>Developer: Failed CI status and logs
    end
```

### 7.3 CI Quality Gates

| Gate | Command | Failure Condition |
|---|---|---|
| Python linting | `python -m ruff check conformance_platform tests` | Style or quality violation |
| Backend testing | `python -m pytest -v` | One or more failed tests |
| Dashboard build | `npm run build` | TypeScript or Vite build error |
| Architecture scan | `python -m conformance_platform.cli` | Blocking architecture violation |

---

## 8. Health Monitoring Sequence

### 8.1 Description

Docker Compose periodically checks whether the backend and sample services are operational.

### 8.2 Sequence Diagram

```mermaid
sequenceDiagram
    participant Docker as Docker Compose
    participant API as Conformance API
    participant Order as Order Service
    participant Other as Other Services

    loop At configured health-check interval
        Docker->>API: GET /health
        API-->>Docker: 200 healthy
        Docker->>Order: GET /health
        Order-->>Docker: 200 healthy
        Docker->>Other: GET /health
        Other-->>Docker: 200 healthy
    end

    alt Service responds successfully
        Docker->>Docker: Mark container healthy
    else Retries are exhausted
        Docker->>Docker: Mark container unhealthy
    end
```

---

## 9. End-to-End Interaction Summary

```mermaid
sequenceDiagram
    actor Developer
    participant Dashboard as React Dashboard
    participant API as FastAPI Backend
    participant Engine as Scan Engine
    participant DB as PostgreSQL

    Developer->>Dashboard: Run architecture scan
    Dashboard->>API: POST scan request
    API->>Engine: Execute conformance analysis
    Engine-->>API: Report and violations
    API->>DB: Persist audit evidence
    DB-->>API: Saved scan identifier
    API-->>Dashboard: Scan response
    Dashboard-->>Developer: Status, metrics, and evidence
```

---

## 10. Preconditions and Postconditions

### 10.1 Run-Scan Use Case

**Preconditions**

- FastAPI backend is running.
- PostgreSQL is available.
- Architecture baseline file exists.
- Registered service directories are accessible.
- Python source files are available for analysis.

**Postconditions**

- Source files have been statically scanned.
- Dependency evidence has been evaluated.
- A conformance report has been generated.
- Scan summary and violations have been persisted.
- Updated results are available through the dashboard and REST API.

### 10.2 View-Scan-Evidence Use Case

**Preconditions**

- At least one scan exists in the database.
- The selected scan identifier is valid.
- The backend is accessible from the dashboard.

**Postconditions**

- Persisted scan metadata is displayed.
- Violation evidence is shown when present.
- A conformant confirmation is shown when no violations exist.

---

## 11. Error and Exception Scenarios

| Scenario | System Response |
|---|---|
| No latest scan exists | API returns `404`; dashboard displays the empty state |
| Requested scan ID does not exist | API returns `404`; dashboard displays an error |
| Invalid Python file is scanned | Scanner raises a syntax-related scan error |
| YAML baseline is invalid | Rule loader rejects the rule file |
| Database is unavailable | Persistence or retrieval operation fails |
| Backend is unavailable | Dashboard displays a request-failure message |
| Blocking dependency is found | Scan is stored and marked as blocked |
| Dashboard build fails in CI | GitHub Actions marks the workflow as failed |

---

## 12. Traceability to Requirements

| Sequence | Related Functional Requirements |
|---|---|
| Dashboard loading | FR-09, FR-10, FR-11 |
| Architecture scan execution | FR-01, FR-02, FR-03, FR-04, FR-05 |
| Scan persistence | FR-06, FR-07 |
| Scan history and evidence | FR-08, FR-09, FR-10 |
| GitHub Actions CI | FR-12, FR-13 |
| Health monitoring | FR-14 |

---

## 13. Conclusion

The sequence diagrams demonstrate how the Architecture Conformance Monitor coordinates frontend requests, REST API operations, static source-code analysis, rule evaluation, database persistence, audit-evidence retrieval, and continuous integration.

These interactions ensure that architectural violations are detected early, stored permanently, presented with actionable evidence, and enforced automatically during development and delivery.