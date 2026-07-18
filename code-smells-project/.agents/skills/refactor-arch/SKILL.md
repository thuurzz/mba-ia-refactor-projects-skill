---
name: refactor-arch
description: Analyze, audit, and refactor legacy projects to MVC architecture. Detects anti-patterns, code smells, security vulnerabilities, and deprecated APIs across any language/framework. Generates structured audit reports and performs automated refactoring with validation.
---

# Refactor-Arch: Automated Architectural Refactoring Skill

You are an expert software architect specializing in refactoring legacy codebases to the MVC (Model-View-Controller) pattern. You work with ANY programming language and framework. Your job is to execute 3 sequential phases.

---

## PHASE 1: PROJECT ANALYSIS

**Goal:** Understand the codebase without modifying anything.

### Step 1.1: Detect Stack

Read these files to determine the technology stack:

- `requirements.txt`, `Pipfile`, `pyproject.toml`, `setup.py` → Python
- `package.json` → Node.js/JavaScript/TypeScript
- `Gemfile` → Ruby
- `composer.json` → PHP
- `go.mod` → Go
- `pom.xml`, `build.gradle` → Java
- `Cargo.toml` → Rust
- `*.csproj` → C#/.NET

For the framework, look at:

- Python: `Flask` (from flask import...), `Django` (django), `FastAPI` (fastapi)
- Node.js: `Express` (require('express')), `Koa`, `Fastify`, `NestJS`
- Ruby: `Rails`, `Sinatra`
- PHP: `Laravel`, `Symfony`
- Java: `Spring Boot`, `Jakarta EE`

For the database, look at:

- `sqlite3`, `sqlite` → SQLite
- `psycopg2`, `pg` → PostgreSQL
- `pymysql`, `mysql2`, `mysql` → MySQL
- `pymongo`, `mongodb`, `mongoose` → MongoDB
- `SQLAlchemy`, `TypeORM`, `Prisma`, `Sequelize` → ORM usage

### Step 1.2: Map Architecture

Determine the current architecture pattern:

- **Monolithic:** All code in 1-5 files, no folder separation
- **Partially organized:** Has some folders (models/, routes/) but logic mixed
- **Layered:** Clear separation but not MVC (e.g., routes + services only)
- **MVC-like:** Already has models/views/controllers but with issues

Count source files (exclude `node_modules`, `__pycache__`, `.git`, `venv`, `dist`, `build`).

### Step 1.3: Identify Domain

Read route definitions, model names, and table names to infer the business domain:

- Products, orders, users → E-commerce
- Courses, enrollments, payments → LMS / Education
- Tasks, users, categories → Task Management / Project Management

### Step 1.4: Print Summary

Print EXACTLY this format:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <detected>
Framework:     <detected> <version>
Dependencies:  <key packages>
Domain:        <inferred domain>
Architecture:  <current pattern>
Source files:  <count> files analyzed
DB tables:     <list of tables/collections>
================================
```

---

## PHASE 2: ARCHITECTURE AUDIT

**Goal:** Cross-reference the codebase against the anti-patterns catalog and generate a report. **DO NOT modify any files.**

### Step 2.1: Load References

Read these reference files for detection knowledge:

- `references/anti-patterns-catalog.md` — What to look for
- `references/report-template.md` — How to format output

### Step 2.2: Scan for Anti-Patterns

For each anti-pattern in the catalog, scan ALL source files. For each finding, record:

- **Severity:** CRITICAL, HIGH, MEDIUM, or LOW
- **File:** Exact file path
- **Line(s):** Exact line number or range
- **Description:** What was found
- **Impact:** Why it matters
- **Recommendation:** How to fix it

### Step 2.3: Generate Report

Print the report following the template in `references/report-template.md`.

### Step 2.4: Pause for Confirmation

After printing the report, **STOP** and ask:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

**DO NOT proceed to Phase 3 until the user confirms with 'y' or 'yes'.**

---

## PHASE 3: REFACTORING

**Goal:** Restructure the project to MVC pattern, fix all findings, and validate.

### Step 3.1: Load References

Read these reference files for refactoring knowledge:

- `references/mvc-guidelines.md` — Target architecture rules
- `references/refactoring-playbook.md` — Transformation patterns

### Step 3.2: Plan the New Structure

Design the target MVC structure based on the project's language and framework:

**For Python/Flask:**

```
src/
├── config/
│   └── settings.py          # All configuration, env vars
├── models/
│   ├── __init__.py
│   └── <entity>_model.py    # Data access, ORM, queries
├── controllers/
│   ├── __init__.py
│   └── <entity>_controller.py  # Business logic, orchestration
├── routes/
│   ├── __init__.py
│   └── <entity>_routes.py   # Route definitions, request/response
├── middlewares/
│   ├── __init__.py
│   └── error_handler.py     # Centralized error handling
├── services/
│   ├── __init__.py
│   └── <service>.py         # Cross-cutting services
└── app.py                    # Composition root / entry point
```

**For Node.js/Express:**

```
src/
├── config/
│   └── index.js             # All configuration, env vars
├── models/
│   └── <entity>.model.js    # Data access, queries
├── controllers/
│   └── <entity>.controller.js  # Business logic
├── routes/
│   └── <entity>.routes.js   # Route definitions
├── middlewares/
│   └── errorHandler.js      # Centralized error handling
├── services/
│   └── <service>.js         # Cross-cutting services
└── app.js                    # Entry point
```

### Step 3.3: Execute Refactoring

Apply transformations from the playbook. For each finding from Phase 2:

1. **CRITICAL issues first** — Security and architecture
2. **HIGH issues second** — Design and coupling
3. **MEDIUM issues third** — Performance and duplication
4. **LOW issues last** — Code quality

Key transformations to apply:

- Extract configuration to config module (use environment variables)
- Separate models by domain entity
- Move business logic from routes to controllers
- Create centralized error handling middleware
- Fix SQL injection with parameterized queries
- Replace weak hashing with bcrypt/argon2
- Fix N+1 queries with JOINs or eager loading
- Remove dead code and unused imports
- Replace print() with proper logging

### Step 3.4: Validate

After refactoring, validate that the application still works:

1. **Boot test:** Start the application and verify it initializes without errors
2. **Endpoint test:** Test each original endpoint and verify it responds correctly
3. **Structure check:** Verify the new directory structure matches MVC

Print the validation results:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<directory tree>

## Changes Made
<summary of changes>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

---

## CRITICAL RULES

1. **NEVER modify files in Phase 1 or Phase 2** — only read and analyze
2. **ALWAYS pause after Phase 2** — wait for user confirmation before Phase 3
3. **ALWAYS validate after Phase 3** — boot the app and test endpoints
4. **Be technology-agnostic** — adapt patterns to the detected language/framework
5. **Preserve functionality** — the refactored app must behave identically to the original
6. **Use parameterized queries** — never concatenate user input into SQL
7. **Use environment variables** — never hardcode secrets or credentials
8. **Follow the reference files** — they contain the detailed knowledge for each phase
