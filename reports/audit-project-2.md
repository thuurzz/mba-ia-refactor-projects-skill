================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript (Node.js) + Express 4.18.2
Files:   3 analyzed | ~183 lines of code

## Summary
CRITICAL: 5 | HIGH: 3 | MEDIUM: 4 | LOW: 4

## Findings

### [CRITICAL] Hardcoded Credentials and Integration Secrets
File: src/utils.js:1-6
Description: Database credentials, a production-like payment gateway key, SMTP user, and the application port are hardcoded in source code through the `config` object instead of being loaded from the environment.
Impact: If the repository or runtime logs are exposed, attackers gain direct access to internal services and payment integrations.
Recommendation: Move secrets and runtime configuration to environment variables and keep only safe defaults or placeholders in source.

### [CRITICAL] God Class Combining Database, Routing, and Business Rules
File: src/AppManager.js:1-138
Description: `AppManager` owns database bootstrapping, schema creation, seed data, route registration, checkout orchestration, payment decisions, reporting logic, and destructive user deletion in a single module.
Impact: Any change in one area risks regressions in unrelated behavior and makes isolated testing or MVC separation impractical.
Recommendation: Split responsibilities into dedicated models, controllers, routes, and services by domain entity.

### [CRITICAL] Plaintext Password in Seed Data
File: src/AppManager.js:18
Description: The initial seeded user is inserted with `pass` set to the literal value `123`, storing a password in plaintext in the database.
Impact: A database leak immediately exposes reusable user credentials and normalizes insecure password handling in the codebase.
Recommendation: Never seed plaintext passwords; hash them with bcrypt before insert and store only the hash.

### [CRITICAL] Weak Homegrown Password Hashing
File: src/utils.js:17-23, src/AppManager.js:68-69
Description: New user passwords are transformed with a custom `badCrypto` function based on repeated base64 concatenation and truncation, without salting or a vetted password hashing algorithm.
Impact: The resulting hashes are trivial to brute-force or reverse compared with bcrypt, scrypt, or argon2.
Recommendation: Replace `badCrypto` with bcrypt password hashing and verify passwords with the same library.

### [CRITICAL] Sensitive Payment Data Logged to Console
File: src/AppManager.js:45
Description: The checkout flow logs the full card number and the payment gateway key with `console.log` during payment processing.
Impact: Sensitive payment and secret data can leak through logs, violating PCI-DSS and exposing credentials to anyone with log access.
Recommendation: Remove sensitive fields from logs entirely and adopt structured logging with redaction or masking.

### [HIGH] Business Logic Embedded Directly in Route Handlers
File: src/AppManager.js:28-129
Description: Route handlers perform request validation, user lookup/creation, payment decisioning, enrollment creation, audit logging, and financial report aggregation directly against the database.
Impact: HTTP concerns, domain rules, and persistence are tightly coupled, which blocks MVC organization and makes change isolation difficult.
Recommendation: Keep routes thin and move checkout/report logic into controllers and services, with models handling data access only.

### [HIGH] Global Mutable State Shared Across Requests
File: src/utils.js:9-15,24
Description: `globalCache` is declared at module scope and mutated by `logAndCache`, then exported for use across the process lifetime.
Impact: Shared mutable state can leak data between requests and becomes unsafe or unpredictable under concurrency or horizontal scaling.
Recommendation: Replace process-global state with a proper cache service or persist needed state in the database.

### [HIGH] Administrative and Destructive Routes Have No Authentication
File: src/AppManager.js:80-137
Description: `/api/admin/financial-report` and `DELETE /api/users/:id` are exposed without any authentication, authorization, or middleware checks.
Impact: Any caller can read financial data or delete users, which is a direct access-control vulnerability.
Recommendation: Add authenticated middleware and explicit authorization rules before allowing admin or destructive actions.

### [MEDIUM] N+1 Query Pattern in Financial Report Generation
File: src/AppManager.js:83-126
Description: The report first loads all courses, then for each course loads enrollments, then for each enrollment loads the user and payment separately.
Impact: Query volume grows multiplicatively with dataset size, causing avoidable latency and database load.
Recommendation: Replace nested per-record lookups with joined or batched queries that return courses, enrollments, users, and payments together.

### [MEDIUM] User Deletion Leaves Orphaned Records
File: src/AppManager.js:12-16,131-135
Description: The schema does not define foreign keys with cascade behavior, and the delete route removes a user while explicitly leaving enrollments and payments behind.
Impact: Orphaned records corrupt reporting, waste storage, and make future data maintenance increasingly brittle.
Recommendation: Add relational constraints with cascade behavior or perform transactional cleanup of dependent records before deleting a user.

### [MEDIUM] Deprecated Callback-Based sqlite3 Usage Without Error Handling on Connection
File: src/AppManager.js:1,7,25-137
Description: The application relies on callback-heavy `sqlite3` APIs throughout the module and opens `new sqlite3.Database(':memory:')` without handling connection initialization errors.
Impact: The code is harder to maintain, harder to compose with async flows, and more fragile when upgrading libraries or expanding the application.
Recommendation: Wrap persistence behind model classes and migrate to a modern async-friendly database access layer or adapter.

### [MEDIUM] Dead Code and Unused Exports Increase Noise
File: src/AppManager.js:2, src/utils.js:10,24
Description: `totalRevenue` is imported into `AppManager` and exported from `utils`, but it is never read or updated anywhere in the application.
Impact: Unused code increases cognitive load and misleads maintainers about state that does not actually affect runtime behavior.
Recommendation: Remove unused globals and exports, then rely on linting to prevent dead code from reappearing.

### [LOW] Console Logging Used as Operational Logging
File: src/app.js:13, src/AppManager.js:45, src/utils.js:13
Description: The application uses raw `console.log` for startup, checkout processing, and cache activity instead of a structured logger with levels.
Impact: Production diagnostics become noisy and difficult to filter, aggregate, or sanitize.
Recommendation: Replace `console.log` with a logging library such as `pino` or `winston` and use explicit log levels.

### [LOW] Magic Strings and Inline Defaults Drive Domain Behavior
File: src/AppManager.js:46-48,68,135, src/utils.js:6
Description: Payment outcomes (`PAID`, `DENIED`), a fallback password (`123456`), a hardcoded success message, and the default port are embedded directly in code.
Impact: Behavior is harder to change safely because critical values are scattered instead of named and centralized.
Recommendation: Extract domain constants and configuration defaults into dedicated modules.

### [LOW] Poor Variable Naming Reduces Readability
File: src/AppManager.js:29-33,43,52,81,86,93, src/utils.js:17
Description: Variables such as `u`, `e`, `p`, `cid`, `cc`, `enrId`, `report`, `coursesPending`, `enrPending`, and `pwd` obscure intent and mix naming styles.
Impact: Maintenance slows down because readers must reconstruct meaning from surrounding code instead of the identifiers themselves.
Recommendation: Rename variables to descriptive domain terms such as `userName`, `email`, `courseId`, `cardNumber`, and `enrollmentId`.

### [LOW] Input Validation Is Incomplete and Superficial
File: src/AppManager.js:29-35
Description: The checkout route only checks field presence and does not validate email format, card format, numeric course identifiers, string lengths, or password quality.
Impact: Invalid or malformed data can enter the system and trigger inconsistent behavior deeper in the flow.
Recommendation: Validate request payloads at the route boundary with a schema library such as Joi or Zod.

================================
Total: 16 findings
================================

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── app.js
├── config/
│   ├── constants.js
│   ├── database.js
│   └── index.js
├── controllers/
│   ├── admin.controller.js
│   ├── checkout.controller.js
│   └── user.controller.js
├── middlewares/
│   ├── async-handler.js
│   ├── auth.middleware.js
│   └── errorHandler.js
├── models/
│   ├── audit-log.model.js
│   ├── course.model.js
│   ├── enrollment.model.js
│   ├── payment.model.js
│   ├── report.model.js
│   └── user.model.js
├── routes/
│   ├── admin.routes.js
│   ├── checkout.routes.js
│   ├── index.js
│   └── user.routes.js
└── services/
    ├── http-error.js
    ├── logger.service.js
    ├── password.service.js
    └── payment.service.js

## Changes Made
- Extracted runtime configuration into `src/config` and required `ADMIN_TOKEN` from the environment instead of hardcoding operational secrets in source.
- Replaced the monolithic `AppManager` with explicit MVC layers: models for data access, controllers for orchestration, route modules for HTTP wiring, and middleware for auth/error handling.
- Rebuilt SQLite schema initialization with foreign keys enabled and cascading deletes to prevent orphaned enrollments and payments.
- Replaced plaintext/custom password handling with salted `crypto.scryptSync` hashes for seeded and newly created users.
- Removed sensitive logging and process-global mutable cache usage; added structured logging that records only safe metadata such as card last four digits.
- Added admin authentication for `/api/admin/financial-report` and `DELETE /api/users/:id` using `x-admin-token` or `Authorization: Bearer`.
- Replaced nested report queries with a single JOIN-based query to eliminate the N+1 access pattern.
- Centralized validation and error handling so routes stay thin and business rules live in controllers.
- Updated developer docs and request samples to reflect environment setup and admin token requirements.

## Validation
  ✓ Application boots without errors (`ADMIN_TOKEN=development-admin-token node -e "require('./src/app').createApp()..."` returned `boot-ok`)
  ✓ `POST /api/checkout` returns `200` with `{"enrollment_id":2,"msg":"Sucesso"}` for a valid Visa-style card
  ✓ `POST /api/checkout` returns `400` with `{"error":"Pagamento recusado"}` for a denied card
  ✓ `GET /api/admin/financial-report` returns `200` with aggregated course revenue and student data behind admin auth
  ✓ `DELETE /api/users/1` returns `200` and subsequent financial report shows `Clean Architecture` with `revenue: 0` and `students: []`, confirming cascade cleanup
  ✓ Zero Phase-2 anti-patterns remain in the refactored runtime paths
================================
