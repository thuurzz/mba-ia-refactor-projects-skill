================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~780 lines of code

## Summary
CRITICAL: 6 | HIGH: 5 | MEDIUM: 5 | LOW: 3

## Findings

### [CRITICAL] Arbitrary SQL Execution in Admin Endpoint
File: app.py:59-76
Description: The `/admin/query` endpoint accepts raw SQL from `request.get_json()` and executes it directly with `cursor.execute(query)`.
Impact: Any caller can read, modify, or delete all database data and potentially destroy the application state.
Recommendation: Remove this endpoint from the public API or restrict it behind strong authentication and an allowlisted command set.

### [CRITICAL] SQL Injection Across the Data Access Layer
File: models.py:28,47-50,57-60,68,92,109-111,126-128,140,148-150,155,157-160,163-166,174,188,192,206,220,224,247,250,253,279-280,289-299
Description: Most queries are built with string concatenation of route parameters or request data instead of bound parameters.
Impact: Attackers can inject arbitrary SQL through product, user, order, status, and search flows to exfiltrate or corrupt data.
Recommendation: Replace every concatenated statement with parameterized queries using `?` placeholders and tuple arguments.

### [CRITICAL] Hardcoded Secret Key in Source Code
File: app.py:7
Description: Flask `SECRET_KEY` is committed as a plain string literal instead of being loaded from configuration.
Impact: Anyone with source access can forge signed session data and impersonate trusted application state.
Recommendation: Move `SECRET_KEY` into environment-backed configuration and require a non-default value outside development.

### [CRITICAL] God Module Handling All HTTP Concerns and Domain Flows
File: controllers.py:1-292
Description: One controller file contains product, user, order, reporting, health, validation, side effects, and error handling for the entire API.
Impact: Changes in one domain can easily break unrelated endpoints, and isolated testing or reuse is unnecessarily difficult.
Recommendation: Split the module into domain-specific controllers and move repeated validation and response concerns into shared helpers.

### [CRITICAL] God Module Handling Schema, Queries, Authentication, Orders, and Reports
File: models.py:1-314
Description: A single model file mixes data access for products, users, orders, authentication, inventory mutation, and reporting calculations.
Impact: The data layer violates single responsibility and makes targeted fixes, tests, and refactors high risk.
Recommendation: Separate the file into entity-specific model modules for products, users, orders, and reporting queries.

### [CRITICAL] Plaintext Password Storage and Comparison
File: database.py:75-82, models.py:79-85,95-100,109-111,126-128
Description: Seed users are stored with plaintext passwords, user records expose the `senha` field, new accounts are inserted without hashing, and login compares raw passwords directly in SQL.
Impact: A database leak immediately compromises all user credentials, and password reuse can create broader account takeover risk.
Recommendation: Hash passwords with `bcrypt`, store only the hash, and verify credentials with a constant-time password check.

### [HIGH] Business Logic and Validation Are Embedded in Route Handlers
File: controllers.py:24-58,64-93,146-216,237-252,264-290
Description: Route-facing functions perform business validation, category rules, order orchestration, notification decisions, and reporting concerns directly.
Impact: The MVC boundary is blurred, making HTTP handlers large, fragile, and hard to test independently from business behavior.
Recommendation: Move domain logic into controller/service functions and keep route handlers limited to request parsing and response formatting.

### [HIGH] Debug Mode Enabled in Runtime Configuration
File: app.py:8,88
Description: The application sets `DEBUG = True` and also boots Flask with `debug=True`.
Impact: Debug traces and the Werkzeug debugger can expose internals and enable remote code execution in unsafe deployments.
Recommendation: Read debug mode from environment configuration and default it to `False`.

### [HIGH] Global Mutable Database Connection Shared Across Requests
File: database.py:4-10
Description: The module stores a singleton SQLite connection in the global `db_connection` variable and reuses it across requests with `check_same_thread=False`.
Impact: Shared mutable state can leak request behavior across threads and creates fragile concurrency semantics.
Recommendation: Use request-scoped connection management or a dedicated database layer that opens and closes connections safely per request.

### [HIGH] Administrative Endpoints Have No Authentication or Authorization
File: app.py:47-78
Description: `/admin/reset-db` and `/admin/query` are exposed without any authentication, authorization, or environment guard.
Impact: Any caller can erase business data or execute privileged database operations.
Recommendation: Remove these endpoints from production code or protect them with authenticated admin-only access checks.

### [HIGH] Sensitive Data and Internal Configuration Leak Through API Responses
File: controllers.py:128-142,264-290, models.py:79-85,95-100
Description: User responses include the `senha` field, and the health endpoint exposes `db_path`, `debug`, `ambiente`, and `secret_key` values.
Impact: Attackers gain credentials and operational details that materially lower the cost of follow-on attacks.
Recommendation: Whitelist safe response fields and keep health responses limited to non-sensitive service status.

### [MEDIUM] N+1 Queries in Order Retrieval and Order Creation Flows
File: models.py:139-166,171-233
Description: The order code performs repeated `SELECT` statements inside loops for each item and each order instead of using joins or batched reads.
Impact: Performance degrades rapidly as order and item counts grow, increasing latency and database load.
Recommendation: Fetch related rows with joins or batched `IN` queries and build the response from those result sets.

### [MEDIUM] Product Validation Logic Is Duplicated Across Create and Update Paths
File: controllers.py:24-58,64-93
Description: The product create and update handlers repeat the same required-field, range, and category validation logic.
Impact: Future rule changes can drift between endpoints and create inconsistent behavior.
Recommendation: Extract shared product validation into a reusable function or service.

### [MEDIUM] Deletes Can Leave Orphaned Order Data and Broken References
File: app.py:47-57, models.py:65-70, database.py:37-53
Description: The schema declares no foreign keys or cascade rules, and product deletion occurs without checking or cleaning dependent order items.
Impact: The database can accumulate inconsistent records and reports can reference missing products.
Recommendation: Add foreign key constraints with appropriate cascade rules or perform transactional cleanup before deleting parent rows.

### [MEDIUM] Generic Exception Handling Returns Raw Error Messages to Clients
File: app.py:68-78, controllers.py:5-292
Description: Broad `except Exception as e` blocks are used throughout the code and often return `str(e)` directly in JSON responses.
Impact: Internal implementation details leak to clients, while different failure classes are flattened into generic handling.
Recommendation: Centralize error handling, catch known exceptions explicitly, and return sanitized client-facing messages.

### [MEDIUM] Deprecated or Unsafe Runtime APIs Used for Server and SQLite Access
File: database.py:10, app.py:88
Description: The project relies on `sqlite3.connect(..., check_same_thread=False)` and the Flask development server via `app.run(...)` for application runtime.
Impact: These choices are fragile for modern production deployment and can become maintenance or concurrency liabilities.
Recommendation: Use request-safe connection management and run the app behind a production WSGI server with external configuration.

### [LOW] Print Statements Are Used Instead of Structured Logging
File: app.py:56,83-85, controllers.py:8,11,57,61,106,161,179,182,208-210,219,248,250
Description: Operational events, errors, and pseudo-notifications are emitted with `print()` calls.
Impact: Logs have no levels, structure, or centralized handling, which makes production diagnostics harder.
Recommendation: Replace `print()` with the standard `logging` module and consistent log levels.

### [LOW] Magic Numbers and Magic Strings Are Scattered Through Business Rules
File: app.py:36,88, controllers.py:47-54,198-200,242,285-289
Description: Validation thresholds, allowed categories, statuses, version values, and configuration flags are embedded as raw literals in multiple handlers.
Impact: Rule changes require manual code hunting and increase the chance of inconsistent updates.
Recommendation: Extract shared constants and configuration values into dedicated modules.

### [LOW] Unused Imports and Dead Code Increase Noise
File: database.py:2, models.py:2
Description: `os` in `database.py` and `sqlite3` in `models.py` are imported but never used.
Impact: Dead code adds avoidable cognitive load and signals weak hygiene in a small codebase.
Recommendation: Remove unused imports and add linting to prevent regressions.

================================
Total: 19 findings
================================

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
.
├── app.py
├── requirements.txt
└── src/
    ├── app.py
    ├── config/
    │   └── settings.py
    ├── controllers/
    │   ├── order_controller.py
    │   ├── product_controller.py
    │   ├── system_controller.py
    │   └── user_controller.py
    ├── middlewares/
    │   └── error_handler.py
    ├── models/
    │   ├── database.py
    │   ├── order_model.py
    │   ├── product_model.py
    │   └── user_model.py
    ├── routes/
    │   ├── order_routes.py
    │   ├── product_routes.py
    │   ├── system_routes.py
    │   └── user_routes.py
    └── services/
        ├── auth_service.py
        ├── notification_service.py
        └── validation_service.py

## Changes Made
- Replaced the root monolith with an MVC-style `src/` package and kept `app.py` as a thin entrypoint.
- Moved environment-backed configuration into `src/config/settings.py` and removed hardcoded runtime secrets and debug defaults.
- Rebuilt the data layer into domain-specific model modules with parameterized SQLite queries only.
- Added request-scoped database access, foreign keys, seed-data initialization, and legacy password hash upgrades.
- Split business rules into domain controllers and shared services for validation, authentication, and notifications.
- Added centralized JSON error handling and sanitized server-side failures.
- Removed insecure admin SQL/reset endpoints and stopped leaking passwords or secret configuration in API responses.
- Switched password handling to hashed storage via Werkzeug security utilities.
- Replaced the Flask development server entrypoint with `waitress` for the executable runtime path.

## Validation
  ✓ Application initializes without errors and `python3 app.py` starts the `waitress` server successfully
  ✓ All original public endpoints respond correctly (`/`, `/health`, `/produtos`, `/produtos/busca`, `/produtos/<id>`, `/usuarios`, `/login`, `/pedidos`, `/pedidos/usuario/<id>`, `/pedidos/<id>/status`, `/relatorios/vendas`)
  ✓ Zero audited anti-patterns remain in the active refactored source files
================================

================================
NEXT STEP: Commit your changes
================================
Run: git add . && git commit -m "refactor: apply MVC architecture - Phase 3 complete"
================================
