# Anti-Patterns Catalog

Catalog of architectural anti-patterns, code smells, and security vulnerabilities with detection signals and severity classification. This catalog is **technology-agnostic** — detection signals work across Python, JavaScript, Java, Ruby, PHP, Go, and other languages.

---

## CRITICAL Severity

### AP-001: SQL Injection

**Detection signals:**
- String concatenation in SQL queries: `"SELECT * FROM " + table`, `"WHERE id = " + id`, `f"SELECT * FROM {table}"`
- Template literals in queries: `` `SELECT * FROM users WHERE id = ${id}` ``
- No usage of parameterized queries (`?` placeholders, `$1`, `%s` with tuple, prepared statements)
- Raw `execute()` with string formatting: `cursor.execute("SELECT * FROM x WHERE y = '" + y + "'")`
- Endpoints that accept raw SQL from user input (e.g., `/admin/query` with `request.json.sql`)

**Impact:** Attacker can execute arbitrary SQL — read/modify/delete any data in the database.

**Recommendation:** Use parameterized queries 100% of the time. Examples:
- Python: `cursor.execute("SELECT * FROM x WHERE y = ?", (y,))`
- Node.js: `db.run("SELECT * FROM x WHERE y = ?", [y])`
- Java: `PreparedStatement ps = conn.prepareStatement("SELECT * FROM x WHERE y = ?")`

---

### AP-002: Hardcoded Credentials / Secrets

**Detection signals:**
- Variable names containing: `password`, `secret`, `key`, `token`, `api_key`, `private`, `credential`
- Assigned to string literals (not from env): `SECRET_KEY = "abc123"`, `const apiKey = "sk-..."`
- Database credentials in source: `dbPass: "mypassword"`, `user: "admin", password: "admin123"`
- Payment gateway keys: `stripe_key`, `paymentGatewayKey`, `pk_live_`
- SMTP/email credentials: `smtp_user`, `email_password`, `EMAIL_HOST_PASSWORD`
- JWT secrets: `JWT_SECRET = "mysecret"`, `jwtSecret = "hardcoded"`

**Impact:** If code is ever exposed (public repo, leak, former employee), attackers gain access to all integrated services.

**Recommendation:** Use environment variables or a secrets manager:
- Python: `os.environ.get("SECRET_KEY")`
- Node.js: `process.env.SECRET_KEY`
- Never commit `.env` files; provide `.env.example` with placeholder values.

---

### AP-003: God Class / God Module

**Detection signals:**
- Single file > 200 lines with multiple unrelated responsibilities
- File contains: database queries + business logic + validation + formatting + routing
- Class with > 10 public methods serving different domains
- File name is generic (`models.py`, `utils.js`, `AppManager.js`, `helpers.py`) but contains everything
- Multiple domain entities handled in one file (products, users, orders, payments all together)

**Impact:** Violates Single Responsibility Principle. Impossible to test in isolation. Any change risks breaking unrelated functionality.

**Recommendation:** Split by domain entity. Each file should handle ONE thing:
- `models/produto.py` — only product data access
- `controllers/pedido_controller.py` — only order business logic
- `routes/user_routes.py` — only user route definitions

---

### AP-004: Plaintext Password Storage

**Detection signals:**
- Passwords stored/comparated without hashing: `WHERE senha = '...'`
- No hash function used before storage: `INSERT INTO users (..., password) VALUES (..., 'plaintext')`
- Passwords in seed data as plaintext: `('admin', 'admin@email.com', 'admin123')`
- Login comparing raw strings: `if user.password == input_password`

**Impact:** Database breach exposes all user passwords. Users often reuse passwords across services.

**Recommendation:** Always hash passwords with bcrypt, scrypt, or argon2:
- Python: `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`
- Node.js: `await bcrypt.hash(password, 10)`

---

### AP-005: Weak Cryptographic Hashing

**Detection signals:**
- Usage of MD5: `hashlib.md5()`, `md5()`, `MD5()`
- Usage of SHA-1: `hashlib.sha1()`, `sha1()`
- Custom/homegrown hash functions: loops with string concatenation, base64 tricks
- No salt in hashing

**Impact:** MD5 and SHA-1 are cryptographically broken. Custom hashes are trivially reversible. Rainbow table attacks are feasible.

**Recommendation:** Use bcrypt, scrypt, or argon2 for passwords. Use SHA-256/512 only for non-security checksums.

---

### AP-006: Logging Sensitive Data

**Detection signals:**
- `console.log` or `print` containing variables named: `password`, `card`, `credit`, `ssn`, `token`, `secret`
- Logging full request bodies that may contain PII
- Logging credit card numbers: `console.log("Processing card " + cc)`
- Logging authentication tokens

**Impact:** Violates PCI-DSS, GDPR, LGPD. Sensitive data in logs is a compliance nightmare.

**Recommendation:** Never log sensitive data. Use structured logging with redaction:
- Mask credit cards: `****-****-****-${cc.slice(-4)}`
- Never log passwords, tokens, or PII

---

## HIGH Severity

### AP-007: Business Logic in Routes/Controllers

**Detection signals:**
- Route handlers containing: validation logic, business rules, data transformation, multiple if/else for business decisions
- Route handler > 30 lines
- Direct database queries in route handlers (bypassing models/services)
- Validation rules (min/max length, allowed values, format checks) inside route functions

**Impact:** Violates MVC separation. Routes should only handle HTTP concerns (request parsing, response formatting). Business logic should be in controllers/services.

**Recommendation:** Extract business logic to controller/service layer:
- Routes: parse request → call controller → format response
- Controllers: validate → apply business rules → call models
- Models: data access only

---

### AP-008: Debug Mode in Production

**Detection signals:**
- `DEBUG = True`, `debug: true`, `app.run(debug=True)`, `NODE_ENV = 'development'`
- Debug toolbar enabled
- Stack traces exposed to users
- Interactive debugger enabled (Werkzeug, Django debug)

**Impact:** Exposes internal paths, stack traces, environment details. Werkzeug debugger allows remote code execution.

**Recommendation:** Use environment variables:
- `DEBUG = os.environ.get("DEBUG", "false").lower() == "true"`
- `app.run(debug=False)` in production

---

### AP-009: Global Mutable State

**Detection signals:**
- Module-level mutable variables: `cache = {}`, `let globalCache = {}`
- Global variables modified across requests: `totalRevenue = 0` then `totalRevenue += amount`
- Singletons without thread safety
- `global` keyword in Python functions

**Impact:** Unpredictable behavior in concurrent requests. State leaks between users. Not thread-safe.

**Recommendation:** Use proper state management:
- Database for persistent state
- Redis/Memcached for cache
- Request-local context for per-request state

---

### AP-010: Missing Authentication / Fake Auth

**Detection signals:**
- Fake/hardcoded tokens: `'token': 'fake-jwt-token-' + str(user.id)`
- No token validation on protected routes
- Authentication commented out or TODO
- `if user.is_admin` without actual auth check

**Impact:** Anyone can access protected resources. No real security.

**Recommendation:** Implement proper JWT or session-based authentication with a library like `PyJWT`, `jsonwebtoken`, or `passport`.

---

### AP-011: Information Leakage in Responses

**Detection signals:**
- API responses returning: password hashes, internal paths, database names, secret keys
- Health check endpoints exposing: `secret_key`, `db_path`, `debug` status, `environment`
- Error responses with full stack traces
- `to_dict()` methods including sensitive fields like `password`

**Impact:** Attackers gain reconnaissance information to plan targeted attacks.

**Recommendation:** Filter sensitive fields from API responses. Use serializers/schemas that explicitly whitelist fields.

---

## MEDIUM Severity

### AP-012: N+1 Query Problem

**Detection signals:**
- Database queries inside loops: `for item in items: cursor.execute("SELECT ...")`
- Nested queries: query A → for each result → query B → for each result → query C
- Multiple `db.get()` or `Model.query` calls inside `forEach`/`for` loops
- No usage of JOINs, eager loading, or batch queries

**Impact:** For N parent records, executes N×M additional queries. Performance degrades exponentially with data growth.

**Recommendation:** Use JOINs, eager loading, or batch queries:
- SQL: `SELECT * FROM pedidos JOIN itens_pedido ON ...`
- SQLAlchemy: `Task.query.options(joinedload(Task.user)).all()`
- Sequelize: `Model.findAll({ include: [RelatedModel] })`

---

### AP-013: Code Duplication

**Detection signals:**
- Same validation logic in create and update handlers
- Repeated overdue/status calculation logic across multiple files
- Copy-pasted error handling blocks
- Same data transformation in multiple places

**Impact:** Violates DRY principle. Bug fixes must be applied in multiple places. Inconsistent behavior when only some copies are updated.

**Recommendation:** Extract shared logic into reusable functions/services. Create validation helpers, status calculators, and error handlers.

---

### AP-014: Missing Cascade / Orphaned Records

**Detection signals:**
- DELETE operations that don't clean up related records
- Foreign keys without ON DELETE CASCADE
- Comments like "matrículas e pagamentos ficaram sujos no banco"
- Manual deletion of parent without child cleanup

**Impact:** Database inconsistency. Orphaned records accumulate, wasting space and causing incorrect reports.

**Recommendation:** Use foreign key constraints with CASCADE or manually delete related records in a transaction.

---

### AP-015: Unused Code / Dead Code

**Detection signals:**
- Imported modules never used: `import json, os, sys` (none used)
- Functions defined but never called
- Utility files with functions that routes reimplement manually
- Commented-out code blocks

**Impact:** Increases cognitive load. Developers waste time understanding code that doesn't run. Bloated imports slow startup.

**Recommendation:** Remove unused imports and dead code. Use linters (flake8, eslint) to detect automatically.

---

### AP-016: Generic Exception Handling

**Detection signals:**
- `except Exception as e:` or `except:` without specific exception types
- `catch (err)` without checking error type
- Returning raw exception messages to clients: `return jsonify({"erro": str(e)})`
- No differentiation between client errors (4xx) and server errors (5xx)

**Impact:** Internal error details leak to clients. Hard to debug because all errors are caught the same way.

**Recommendation:** Catch specific exceptions. Use custom error classes. Return sanitized messages to clients, log full details server-side.

---

### AP-017: Deprecated APIs

**Detection signals (Python):**
- `datetime.utcnow()` → deprecated in Python 3.12+, use `datetime.now(datetime.UTC)`
- `hashlib.md5()` for security → use `hashlib.sha256()` or bcrypt
- `sqlite3.connect(..., check_same_thread=False)` → use SQLAlchemy or connection pool
- `flask.jsonify` with raw dict → use marshmallow/pydantic schemas
- `app.run()` for production → use gunicorn/uwsgi

**Detection signals (Node.js):**
- `sqlite3` (callback-based) → use `better-sqlite3` (sync) or `sqlite3` with async/await wrapper
- `Buffer()` without `Buffer.alloc()` or `Buffer.from()`
- `request` package (deprecated) → use `fetch` or `axios`
- `body-parser` (standalone) → use `express.json()` (built-in since Express 4.16)
- `new sqlite3.Database(':memory:')` without proper error handling

**Detection signals (General):**
- Callback-based APIs where Promise/async-await is standard
- `var` instead of `let`/`const` in modern JavaScript
- `__future__` imports for features already default in current Python version

**Impact:** Deprecated APIs may be removed in future versions. Often have known bugs or security issues.

**Recommendation:** Replace with the modern equivalent. Check language/framework migration guides.

---

## LOW Severity

### AP-018: Print Statements as Logging

**Detection signals:**
- `print()` used for operational messages: `print("Server started")`, `print("Error: " + str(e))`
- `console.log()` used without a logging library
- No log levels (DEBUG, INFO, WARNING, ERROR)
- No structured logging format

**Impact:** No log level filtering, no rotation, no structured format. Difficult to debug in production.

**Recommendation:** Use proper logging:
- Python: `logging` module with `logging.getLogger(__name__)`
- Node.js: `winston`, `pino`, or `morgan`

---

### AP-019: Magic Numbers / Magic Strings

**Detection signals:**
- Numeric literals without named constants: `if len(name) < 2`, `if priority > 5`
- Status strings repeated as literals: `'pending'`, `'done'`, `'cancelled'`
- Configuration values inline: `port = 5000`, `max_retries = 3`

**Impact:** Hard to maintain. Changing a value requires finding all occurrences.

**Recommendation:** Define named constants:
- `MIN_NAME_LENGTH = 2`
- `VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']`
- `DEFAULT_PORT = 5000`

---

### AP-020: Poor Variable Naming

**Detection signals:**
- Single-letter variables (except loop counters): `u`, `e`, `p`, `c`
- Abbreviated names that obscure meaning: `cid`, `enrId`, `usr`
- Inconsistent language mixing: some variables in Portuguese, some in English
- Generic names: `data`, `result`, `temp`, `obj`

**Impact:** Reduces code readability. New developers struggle to understand the codebase.

**Recommendation:** Use descriptive names: `user`, `email`, `courseId`, `enrollmentId`. Be consistent with language.

---

### AP-021: Missing Input Validation

**Detection signals:**
- No validation of required fields
- No type checking on numeric inputs
- No length limits on string inputs
- No format validation on emails, dates, etc.

**Impact:** Invalid data enters the system, causing bugs downstream. Security risk from malformed input.

**Recommendation:** Validate all inputs at the route/controller boundary. Use schema validation libraries (marshmallow, pydantic, joi, zod).

---

## Severity Classification Rules

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Security vulnerabilities, data exposure, complete architecture violation |
| **HIGH** | Strong MVC/SOLID violations, design flaws affecting maintainability |
| **MEDIUM** | Performance issues, code duplication, standardization problems |
| **LOW** | Readability, naming, minor quality improvements |