# Problem Statement and Objectives

## Project Title

**Architecture Conformance Monitor**

## 1. Introduction

Modern software systems frequently use microservice and layered architectures to improve scalability, maintainability, deployment flexibility, and separation of concerns. Each service is expected to follow predefined architectural rules, such as permitted dependencies between API, service, repository, and model layers.

As software evolves, developers may unintentionally introduce dependencies that violate these rules. For example, an API layer may directly access a repository layer even though the approved architecture requires all requests to pass through the service layer. Such violations gradually weaken the intended architecture and create technical debt.

The Architecture Conformance Monitor is designed to continuously inspect Python microservices, identify architectural violations, preserve scan results, and provide actionable evidence through a web dashboard and automated CI checks.

## 2. Background

Architectural decisions are normally documented using design documents, diagrams, coding guidelines, and development conventions. However, these documents do not automatically verify whether the implementation continues to follow the approved design.

During regular development, architectural drift may occur because of:

- Frequent code changes
- Increasing system complexity
- Multiple developers working on different services
- Lack of automated architectural validation
- Direct dependencies added for short-term convenience
- Inconsistent understanding of architectural boundaries
- Pressure to deliver features quickly

Traditional unit and integration tests validate functional behaviour but generally do not detect violations of architectural structure. Code review can identify some violations, but manual inspection becomes difficult and inconsistent as the codebase grows.

Therefore, a continuous and automated mechanism is required to compare the implemented source code with declared architectural rules.

## 3. Problem Statement

Software architecture is usually defined during the design phase, but the source code may gradually deviate from that architecture as the system evolves. This architectural drift introduces hidden technical debt, increases coupling, weakens service and layer boundaries, and makes the system more difficult to test, maintain, and extend.

Existing functional testing processes do not automatically detect whether Python microservices follow their declared dependency rules. Manual code review is time-consuming, depends on reviewer experience, and may not consistently identify every architectural violation.

The problem addressed by this project is the absence of an automated system that can:

1. Scan Python microservice source code.
2. Identify internal architectural dependencies.
3. Compare detected dependencies with predefined architecture rules.
4. Detect forbidden layer relationships.
5. present precise evidence for each violation.
6. Preserve historical scan results for auditing and trend analysis.
7. Block non-conformant changes through continuous integration.

## 4. Proposed Solution

The proposed Architecture Conformance Monitor is a full-stack software platform that performs continuous architectural validation.

The system statically analyses Python source files using the Python Abstract Syntax Tree. It detects imports between recognised application layers and evaluates those dependencies against architecture rules declared in a YAML configuration file.

Each scan generates a structured report containing:

- Services scanned
- Files inspected
- Internal dependencies detected
- Architectural violations found
- Blocking status
- Source file and line number
- Source and target layers
- Imported target module
- Evidence and severity information

Scan results and violation evidence are stored in PostgreSQL. A FastAPI backend exposes the information through REST endpoints, while a React and TypeScript dashboard displays the latest conformance status, findings trend, scan history, and detailed violation evidence.

The scanner also runs within GitHub Actions so architectural rules are checked automatically whenever code is pushed or a pull request is created.

## 5. Aim

The primary aim of this project is to develop an automated Architecture Conformance Monitor that detects architectural drift in Python microservices, records technical-debt evidence, and supports continuous enforcement of approved architecture rules.

## 6. Objectives

The project has the following objectives:

1. **Define machine-readable architecture rules**

   Represent service boundaries, architectural layers, permitted dependencies, forbidden dependencies, and validation constraints in a YAML rules file.

2. **Statically analyse Python microservices**

   Parse Python source files using the Abstract Syntax Tree without executing application code.

3. **Discover internal layer dependencies**

   Detect imports between recognised layers such as API, services, repositories, models, and schemas.

4. **Detect architecture violations**

   Compare discovered dependencies with declared rules and identify forbidden relationships.

5. **Generate actionable evidence**

   Report the affected service, source file, line number, source layer, target layer, imported module, violation type, severity, and stable violation identifier.

6. **Persist scan history**

   Store scan summaries and individual violation records in PostgreSQL for later retrieval and auditing.

7. **Provide a REST API**

   Expose health, scan execution, latest scan, scan history, and individual scan-detail endpoints through FastAPI.

8. **Provide a monitoring dashboard**

   Display metrics, conformance status, historical trends, scan records, and expandable violation evidence through a React and TypeScript interface.

9. **Support containerised execution**

   Package the backend, frontend, PostgreSQL database, and sample microservices using Docker and Docker Compose.

10. **Automate quality and conformance checks**

    Use GitHub Actions to run linting, automated tests, the architecture scan, and the frontend production build.

11. **Validate the solution using automated tests**

    Test rule loading, source scanning, violation evaluation, persistence, API behaviour, and end-to-end scan execution.

12. **Reduce architectural technical debt**

    Detect structural violations early so they can be corrected before they become expensive maintenance problems.

## 7. Project Scope

### 7.1 In Scope

The current project includes:

- Python microservice source-code scanning
- Python import analysis using the Abstract Syntax Tree
- YAML-based architecture rule definition
- Architectural-layer dependency detection
- Forbidden dependency detection
- Violation severity and blocking decisions
- JSON conformance-report generation
- PostgreSQL persistence
- Scan history and violation-evidence retrieval
- FastAPI REST services
- React and TypeScript monitoring dashboard
- Docker-based local deployment
- Nginx-based frontend serving
- GitHub Actions continuous integration
- Automated linting and testing
- Sample order, payment, and inventory services

### 7.2 Out of Scope

The current MVP does not include:

- Runtime dependency discovery from distributed traces
- Automatic source-code modification
- Automatic correction of architecture violations
- Source-language analysis other than Python
- Full enterprise authentication and role-based access control
- Multi-tenant project management
- Kubernetes production orchestration
- Machine-learning-based rule generation
- Integration with every external source-code provider

These capabilities may be considered for future development.

## 8. Stakeholders

| Stakeholder | Interest in the System |
|---|---|
| Software architects | Define rules and verify architectural conformance |
| Developers | Receive early and precise feedback about violations |
| Technical leads | Monitor architecture quality and technical debt |
| Quality engineers | Include structural quality in validation activities |
| DevOps engineers | Integrate conformance checks into CI pipelines |
| Project managers | Review project quality and release readiness |
| Academic evaluators | Assess software-engineering design and implementation |

## 9. Functional Summary

The system must be capable of:

- Loading and validating architecture rules.
- Scanning all configured Python services.
- Parsing Python source files safely.
- Detecting internal layer dependencies.
- Ignoring external library dependencies.
- Evaluating detected dependencies against declared rules.
- Generating structured scan and violation reports.
- Determining whether a scan should block a release.
- Saving scan reports and violations.
- Retrieving the latest scan.
- Retrieving scan history.
- Retrieving a specific scan and its evidence.
- Displaying scan information in the dashboard.
- Running automated checks through GitHub Actions.

## 10. Non-Functional Summary

The system should provide:

- **Accuracy:** Correctly identify configured architectural dependencies.
- **Reliability:** Produce repeatable results for the same source code and rules.
- **Performance:** Complete scans within a practical time for the sample system.
- **Usability:** Present results clearly to developers and reviewers.
- **Maintainability:** Separate scanning, rule evaluation, persistence, API, and user-interface responsibilities.
- **Portability:** Run consistently through Docker on supported environments.
- **Auditability:** Preserve scan summaries and detailed violation evidence.
- **Extensibility:** Allow additional rules, scanners, services, and evidence sources.
- **Security:** Avoid executing scanned Python source code during static analysis.

## 11. Constraints

The solution operates under the following constraints:

- The MVP analyses only Python source code.
- Services must use a recognisable project and layer structure.
- Architecture rules must be defined correctly in YAML.
- Static analysis can detect declared imports but not every runtime dependency.
- PostgreSQL is required for persistent scan history in the containerised environment.
- Docker is required to run the complete production-style stack locally.
- The frontend requires access to the backend REST API.

## 12. Assumptions

The project assumes that:

- The target services are written in Python.
- Internal layers are represented through package or directory names.
- Import statements provide sufficient evidence for MVP dependency analysis.
- Architectural rules are approved before scanning.
- Developers execute scans from the repository root.
- The configured source paths are available to the scanner.
- A violation marked as blocking must prevent architectural approval.

## 13. Success Criteria

The MVP is considered successful when:

- Architecture rules can be loaded and strictly validated.
- Three configured Python microservices can be scanned.
- Internal imports can be discovered with file and line evidence.
- Forbidden layer dependencies can be detected.
- A clean architecture produces a conformant result.
- A deliberately introduced violation produces a blocked result.
- Scan summaries and violations are persisted in PostgreSQL.
- Historical scan details can be retrieved through the REST API.
- The dashboard displays both conformant and blocked scans.
- The evidence panel displays stored violation details.
- Backend tests and linting pass.
- The frontend production build succeeds.
- GitHub Actions completes all configured quality checks successfully.
- The complete platform can run through Docker Compose.

## 14. Expected Outcome

The expected outcome is a working software-engineering platform that continuously compares implemented Python microservices with declared architecture rules.

The system gives developers early feedback, gives architects objective evidence of structural compliance, provides project teams with an auditable history of technical debt, and prevents blocking architectural violations from silently entering the codebase.

## 15. Conclusion

The Architecture Conformance Monitor addresses the gap between documented software architecture and implemented source code. By converting architecture rules into executable checks, the project makes architectural governance continuous, measurable, and repeatable.

The resulting platform demonstrates important software-engineering concepts including requirements analysis, layered design, static analysis, REST API development, database persistence, frontend development, automated testing, containerisation, and continuous integration.