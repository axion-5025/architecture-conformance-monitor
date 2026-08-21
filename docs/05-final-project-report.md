# Final Project Report

## Architecture Conformance Monitor

### Continuous Architecture Conformance and Technical Debt Monitoring for Python Microservices

---

## Project Information

| Field | Details |
|---|---|
| Project title | Architecture Conformance Monitor |
| Project type | Software Engineering Academic Project |
| Domain | Software Architecture and Technical Debt Management |
| Student name | Krishna |
| Register number | [Enter Register Number] |
| Department | [Enter Department Name] |
| Institution | [Enter Institution Name] |
| Academic year | [Enter Academic Year] |
| Project guide | [Enter Guide Name] |
| Repository | https://github.com/axion-5025/architecture-conformance-monitor |
| Document version | 1.0 |
| Date | [Enter Submission Date] |

---

# Certificate

This is to certify that the project titled **“Architecture Conformance Monitor”** is a genuine work carried out by **Krishna**, under the guidance and supervision of **[Guide Name]**, in partial fulfilment of the requirements for the Software Engineering subject during the academic year **[Academic Year]**.

The project work presented in this report has been completed according to the prescribed academic requirements.

| Role | Name and Signature |
|---|---|
| Student | Krishna |
| Project guide | [Guide Name] |
| Head of department | [HOD Name] |
| External examiner | [Examiner Name] |

---

# Declaration

I hereby declare that the project titled **“Architecture Conformance Monitor”** is my original work completed as part of the Software Engineering subject.

The project has not been submitted previously, either fully or partially, for the award of any other degree, diploma, or academic qualification. All references and external resources used during the project have been appropriately acknowledged.

**Student:** Krishna  
**Place:** [Enter Place]  
**Date:** [Enter Date]  
**Signature:** ____________________

---

# Acknowledgement

I express my sincere gratitude to **[Guide Name]**, who provided valuable guidance, technical suggestions, and continuous encouragement throughout the development of this project.

I thank the faculty members of **[Department Name]** and **[Institution Name]** for providing the opportunity and necessary resources to complete this Software Engineering project.

I also acknowledge the open-source communities behind Python, FastAPI, React, TypeScript, PostgreSQL, Docker, Ruff, Pytest, SQLAlchemy, and GitHub Actions. These technologies played an important role in implementing and validating the project.

Finally, I thank my classmates, friends, and family members for their encouragement and support.

---

# Abstract

Modern software applications increasingly use microservice architectures to achieve modularity, independent deployment, scalability, and maintainability. However, as microservices evolve, developers may unintentionally introduce dependencies that violate the intended architectural design. These violations gradually weaken service boundaries and contribute to architectural technical debt.

Manual architecture reviews are useful but difficult to perform continuously. They are time-consuming, depend on reviewer expertise, and may detect violations only after they have already become part of the codebase. Traditional code-quality tools primarily focus on syntax, formatting, and general programming defects. They do not necessarily verify whether source-code dependencies comply with application-specific architectural rules.

The **Architecture Conformance Monitor** was developed to address this problem. It performs static analysis of Python microservices, extracts internal layer dependencies, evaluates them against declarative YAML architecture rules, and reports violations with detailed evidence. Scan results and violation records are stored in PostgreSQL, exposed through a FastAPI REST API, and presented through a React and TypeScript dashboard.

The dashboard displays the latest conformance status, services and files scanned, dependencies discovered, violations detected, historical scan results, trends, and stored evidence for individual violations. The complete system is containerized using Docker Compose. GitHub Actions automatically executes linting, automated tests, architecture scans, and frontend production builds.

The implemented MVP demonstrates that architectural rules can be treated as executable and continuously verifiable software artifacts. The system helps development teams identify architectural drift earlier, preserve an auditable scan history, and prevent blocking violations from progressing unnoticed.

**Keywords:** software architecture, architecture conformance, technical debt, microservices, static analysis, FastAPI, React, PostgreSQL, Docker, CI/CD.

---

# Table of Contents

1. Introduction  
2. Problem Definition  
3. Project Objectives  
4. Scope and Limitations  
5. Literature and Existing-System Study  
6. Proposed System  
7. Requirements Analysis  
8. System Design  
9. Technology Stack  
10. System Implementation  
11. Database Design  
12. API Design  
13. User Interface  
14. Testing and Quality Assurance  
15. Deployment and Continuous Integration  
16. Results and Discussion  
17. Project Management and Software Engineering Practices  
18. Security and Reliability Considerations  
19. Challenges and Solutions  
20. Future Enhancements  
21. Conclusion  
22. References  
23. Appendices  

---

# 1. Introduction

## 1.1 Background

Software architecture defines the major structural decisions of a software system. These decisions include:

- division of responsibilities;
- service boundaries;
- permitted dependencies;
- prohibited dependencies;
- ownership of shared resources;
- communication patterns;
- deployment structure.

An architectural model may initially be well-designed, but the implemented code can gradually move away from that design. This process is known as **architectural drift** or **architectural erosion**.

For example, consider a layered Python service containing the following layers:

- API;
- services;
- repositories;
- models.

The intended architecture may require the API layer to communicate only with the service layer. A developer may later import a repository directly into an API module to complete a feature quickly. Although the application may still run, the dependency bypasses the service layer and violates the approved architecture.

If such violations accumulate, the system becomes harder to understand, modify, test, and maintain. This creates architectural technical debt.

## 1.2 Need for the Project

Architecture documentation alone cannot guarantee that source code follows the documented design. Continuous enforcement requires architecture rules to be converted into machine-readable constraints.

A practical conformance platform should be able to:

1. read declared architecture rules;
2. inspect the real source code;
3. discover internal dependencies;
4. compare dependencies with permitted relationships;
5. report violations;
6. preserve historical results;
7. provide evidence to developers;
8. run automatically during continuous integration.

The Architecture Conformance Monitor implements this workflow for Python microservices.

## 1.3 Project Overview

The implemented platform scans three sample Python microservices:

- order service;
- payment service;
- inventory service.

The platform processes the Python Abstract Syntax Tree of each source file to detect local imports. It maps source and target modules to architectural layers and evaluates the resulting dependencies using YAML-defined rules.

The platform is accessible through:

- a command-line interface;
- a REST API;
- a web dashboard;
- an automated GitHub Actions workflow.

---

# 2. Problem Definition

## 2.1 Problem Statement

Microservice applications are expected to follow defined architectural boundaries and dependency rules. During continuous development, developers may unintentionally introduce dependencies that violate these rules.

Manual architecture reviews cannot efficiently inspect every code change. General-purpose linters detect code-quality problems but do not validate project-specific architectural constraints. Consequently, architectural violations may remain undetected until they create significant technical debt.

A system is therefore required to continuously scan Python microservices, identify internal dependencies, validate those dependencies against declared architecture rules, report violations with actionable evidence, preserve historical results, and support automated enforcement in continuous integration.

## 2.2 Core Problem Being Solved

The project solves the absence of automated traceability between:

- the intended architecture stored as rules; and
- the actual architecture represented by source-code dependencies.

The system establishes this traceability by converting imports into dependency evidence and comparing that evidence against the approved architecture.

## 2.3 Effects of the Existing Problem

Uncontrolled architectural drift may cause:

- tight coupling between layers;
- reduced modularity;
- unclear responsibilities;
- difficult unit testing;
- complicated refactoring;
- increased regression risk;
- slower feature development;
- expensive technical-debt correction;
- inconsistent architecture across services;
- loss of confidence in architecture documentation.

---

# 3. Project Objectives

## 3.1 Primary Objective

To design and implement a platform that automatically detects architectural violations in Python microservices and preserves the results as auditable technical-debt records.

## 3.2 Specific Objectives

The specific objectives are:

1. To represent architecture constraints using a readable YAML configuration.
2. To validate configuration files before performing a scan.
3. To statically inspect Python source files without executing application logic.
4. To discover internal layer dependencies from Python import statements.
5. To ignore standard-library and third-party dependencies that are outside the defined application architecture.
6. To detect prohibited layer-to-layer dependencies.
7. To produce structured JSON conformance reports.
8. To classify scan results as conformant or blocked.
9. To store scan summaries and violation evidence in PostgreSQL.
10. To expose scan operations and historical information through a REST API.
11. To provide a dashboard for running scans and reviewing results.
12. To present historical trends and evidence for individual violations.
13. To containerize all major services using Docker.
14. To automate linting, testing, architecture validation, and frontend builds using GitHub Actions.
15. To verify the system using automated test cases.

## 3.3 Success Criteria

The project is considered successful when:

- valid architecture rules are loaded successfully;
- invalid or inconsistent rules are rejected;
- Python services are scanned correctly;
- prohibited dependencies are detected;
- external dependencies are ignored;
- invalid Python files produce meaningful errors;
- conformant and blocked scans are distinguished;
- scan and violation records are persisted;
- users can retrieve historical and individual scan details;
- evidence appears correctly in the dashboard;
- backend tests pass;
- frontend production builds successfully;
- containers become healthy;
- the GitHub Actions workflow passes.

---

# 4. Scope and Limitations

## 4.1 In Scope

The MVP includes:

- Python microservice scanning;
- static import analysis using the Python AST;
- detection of dependencies between known layers;
- YAML-based architectural rules;
- strict validation of the rule model;
- forbidden layer-dependency detection;
- command-line scan execution;
- JSON report generation;
- REST endpoints for scans and health status;
- PostgreSQL persistence;
- latest-scan retrieval;
- scan-history retrieval;
- individual scan-detail retrieval;
- stored violation evidence;
- React and TypeScript dashboard;
- conformance metrics;
- findings trend visualization;
- expandable evidence panels;
- Docker Compose orchestration;
- health checks;
- automated backend testing;
- frontend production-build validation;
- GitHub Actions integration.

## 4.2 Out of Scope

The current MVP does not include:

- automatic correction of violations;
- Java, JavaScript, C#, or other language scanners;
- runtime dependency detection;
- distributed trace analysis;
- authentication and authorization;
- organization-level multi-tenancy;
- direct GitHub repository cloning through the UI;
- pull-request comments;
- email or chat notifications;
- user-defined rule editing through the dashboard;
- advanced graph visualization;
- Kubernetes deployment;
- predictive technical-debt analytics;
- production-grade OpenTelemetry and Jaeger integration.

These features may be considered for future development.

## 4.3 Assumptions

The system assumes that:

- scanned services are written in Python;
- application packages follow recognizable layer names;
- architecture rules are available in YAML format;
- the configured service paths exist;
- the PostgreSQL service is available for persistent operation;
- Docker is available for complete local deployment;
- users have permission to scan the target source code.

## 4.4 Constraints

The project is constrained by:

- academic project timelines;
- MVP-level implementation scope;
- static-analysis limitations;
- dependency detection based primarily on imports;
- one application rule set at a time;
- local Docker-based deployment;
- absence of production identity management.

---

# 5. Existing-System Study

## 5.1 Manual Architecture Reviews

In many projects, architecture is reviewed manually through:

- design meetings;
- code reviews;
- architecture documents;
- senior developer inspection;
- periodic audits.

Manual review supports contextual reasoning but has several weaknesses:

- it is time-consuming;
- it is not applied consistently;
- reviewers may miss hidden dependencies;
- results are difficult to reproduce;
- historical evidence is rarely preserved;
- validation may happen late in development.

## 5.2 General Code-Quality Tools

Linters and static-analysis tools commonly identify:

- formatting errors;
- unused imports;
- suspicious syntax;
- type problems;
- complexity issues;
- insecure patterns.

However, they do not automatically understand application-specific architecture rules such as:

> The API layer shall not directly import the repository layer.

## 5.3 Architecture Documentation

Architecture diagrams describe the intended structure, but diagrams do not continuously inspect source code. Documentation may become outdated when implementation decisions change.

## 5.4 Limitations of the Existing Approach

| Existing approach | Limitation |
|---|---|
| Manual review | Expensive and inconsistent |
| Static documentation | Does not enforce implementation |
| General linter | Lacks project-specific architecture rules |
| One-time audit | Does not provide continuous monitoring |
| Build-only validation | May not preserve detailed evidence |
| Informal technical-debt list | Difficult to trace to code |

---

# 6. Proposed System

## 6.1 System Description

The proposed system is a continuous architecture-conformance platform for Python microservices.

It performs the following operations:

1. Loads the architecture baseline.
2. Validates the rule structure.
3. Iterates through configured services.
4. Locates Python source files.
5. Parses each file using the Python AST.
6. Extracts local import dependencies.
7. Determines source and target layers.
8. Evaluates dependencies against forbidden relationships.
9. Creates structured violations.
10. Generates a JSON report.
11. Saves scan and violation records.
12. Exposes the information through REST endpoints.
13. Presents the results on a web dashboard.
14. Repeats validation automatically in CI.

## 6.2 Advantages

The proposed system provides:

- early violation detection;
- repeatable rule evaluation;
- architecture-as-code;
- source-level evidence;
- persistent audit history;
- visual status reporting;
- CI integration;
- clear release-blocking decisions;
- reduced dependence on manual inspection;
- improved maintainability.

## 6.3 High-Level Workflow

```mermaid
flowchart TD
    A["Load YAML rules"] --> B["Validate rule model"]
    B --> C["Scan Python services"]
    C --> D["Extract local dependencies"]
    D --> E["Evaluate architecture rules"]
    E --> F["Generate JSON report"]
    F --> G["Persist scan and violations"]
    G --> H["Expose REST API"]
    H --> I["Display dashboard evidence"]


    