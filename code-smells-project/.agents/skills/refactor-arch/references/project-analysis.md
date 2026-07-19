# Project Analysis Heuristics

Technology-agnostic heuristics for detecting language, framework, database, and architecture patterns.

---

## 1. Language Detection

Check for these files in order of priority:

| File                                                                     | Language                |
| ------------------------------------------------------------------------ | ----------------------- |
| `package.json`                                                           | JavaScript / TypeScript |
| `requirements.txt`, `Pipfile`, `pyproject.toml`, `setup.py`, `setup.cfg` | Python                  |
| `Gemfile`                                                                | Ruby                    |
| `composer.json`                                                          | PHP                     |
| `go.mod`                                                                 | Go                      |
| `pom.xml`, `build.gradle`, `build.gradle.kts`                            | Java / Kotlin           |
| `Cargo.toml`                                                             | Rust                    |
| `*.csproj`, `*.sln`                                                      | C# / .NET               |
| `CMakeLists.txt`                                                         | C / C++                 |
| `mix.exs`                                                                | Elixir                  |

**For JavaScript vs TypeScript:** Check for `.ts` or `.tsx` file extensions. If `tsconfig.json` exists, it's TypeScript.

**Version extraction:**

- Python: Parse `requirements.txt` for `flask==X.Y.Z`, `django==X.Y.Z`
- Node.js: Parse `package.json` → `dependencies` for version ranges
- Ruby: Parse `Gemfile` for `gem 'rails', '~> X.Y'`
- PHP: Parse `composer.json` → `require`

---

## 2. Framework Detection

### Python

| Signal                | Framework |
| --------------------- | --------- |
| `from flask import`   | Flask     |
| `from fastapi import` | FastAPI   |
| `from django.`        | Django    |
| `import tornado`      | Tornado   |
| `from sanic import`   | Sanic     |
| `from pyramid.`       | Pyramid   |

### Node.js

| Signal                    | Framework |
| ------------------------- | --------- |
| `require('express')`      | Express   |
| `require('koa')`          | Koa       |
| `require('fastify')`      | Fastify   |
| `require('@nestjs/core')` | NestJS    |
| `require('hapi')`         | Hapi      |

### Ruby

| Signal               | Framework |
| -------------------- | --------- |
| `Rails::Application` | Rails     |
| `require 'sinatra'`  | Sinatra   |
| `require 'grape'`    | Grape     |

### PHP

| Signal        | Framework |
| ------------- | --------- |
| `Illuminate\` | Laravel   |
| `Symfony\`    | Symfony   |
| `Slim\`       | Slim      |

### Java

| Signal                     | Framework           |
| -------------------------- | ------------------- |
| `org.springframework.boot` | Spring Boot         |
| `jakarta.ws.rs`            | Jakarta EE / JAX-RS |
| `io.micronaut`             | Micronaut           |

---

## 3. Database Detection

### Connection strings and imports

| Signal                                              | Database         |
| --------------------------------------------------- | ---------------- |
| `sqlite3` (Python), `sqlite3` (Node.js), `:memory:` | SQLite           |
| `psycopg2`, `pg`                                    | PostgreSQL       |
| `pymysql`, `mysql.connector`, `mysql2`              | MySQL / MariaDB  |
| `pymongo`, `mongodb`, `mongoose`                    | MongoDB          |
| `redis`                                             | Redis            |
| `SQLALCHEMY_DATABASE_URI`                           | SQLAlchemy (ORM) |
| `DATABASES = { 'default': { 'ENGINE': ... } }`      | Django ORM       |
| `TypeORM`, `Prisma`, `Sequelize`, `Knex`            | Node.js ORMs     |

### Table/collection discovery

- Python raw SQL: Look for `CREATE TABLE IF NOT EXISTS <name>`
- Python ORM: Look for `class <Name>(db.Model):` with `__tablename__`
- Node.js raw SQL: Look for `CREATE TABLE <name>`
- Node.js ORM: Look for model definitions

---

## 4. Architecture Pattern Detection

### Monolithic (1-5 files, no folders)

**Signals:**

- All source code in root directory
- No `models/`, `controllers/`, `routes/`, `services/` folders
- Files named generically: `app.py`, `models.py`, `utils.js`
- Single file contains multiple domains

**Example:** `code-smells-project/` — 4 files, all logic mixed

### Partially Organized (has some folders, logic still mixed)

**Signals:**

- Has `models/` or `routes/` folders
- Business logic still in route handlers
- Some separation but inconsistent
- Utils/services exist but aren't used

**Example:** `task-manager-api/` — has models/, routes/, services/, utils/ but logic is in routes

### God Class (one class/file does everything)

**Signals:**

- Single class with > 10 methods
- Class handles: database init + routing + business logic + reporting
- File > 100 lines with multiple unrelated sections

**Example:** `AppManager.js` — initDb, setupRoutes, checkout, reports all in one class

### Layered (clear separation but not MVC)

**Signals:**

- Has `routes/` + `services/` but no `controllers/`
- Has `models/` + `routes/` but models contain business logic
- Missing one of the MVC layers

---

## 5. Domain Inference

Infer the business domain from:

1. **Route paths:** `/produtos`, `/products` → E-commerce; `/tasks` → Task management; `/courses`, `/enrollments` → Education/LMS
2. **Model/table names:** `produtos`, `pedidos`, `usuarios` → E-commerce; `tasks`, `users`, `categories` → Task management
3. **Project name in package.json/README:** Often hints at domain
4. **Seed data content:** Product names, course titles, task descriptions

---

## 6. File Counting

Count source files excluding:

- `node_modules/`, `__pycache__/`, `.git/`
- `venv/`, `.venv/`, `env/`
- `dist/`, `build/`, `.next/`
- `*.pyc`, `*.pyo`, `*.class`
- `package-lock.json`, `yarn.lock`, `poetry.lock`
- Migration files (unless they contain business logic)
- Test files (count separately as `(+N test files)`)

---

## 7. Dependency Analysis

Extract key dependencies to understand the project:

- **Web framework:** Flask, Express, Django, etc.
- **Database drivers:** psycopg2, mysql2, sqlite3
- **ORMs:** SQLAlchemy, Sequelize, TypeORM, Prisma
- **Auth:** PyJWT, jsonwebtoken, passport, bcrypt
- **Validation:** marshmallow, pydantic, joi, zod
- **Async:** asyncio, celery, bull
- **Testing:** pytest, jest, mocha

List only the most relevant 3-5 dependencies in the Phase 1 summary.

---

## 8. Lines of Code Estimation

Quick estimate:

- Count total lines across all source files
- Round to nearest hundred
- Format: `~800 lines of code`
