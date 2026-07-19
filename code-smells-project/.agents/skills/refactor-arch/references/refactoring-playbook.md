# Refactoring Playbook

Concrete transformation patterns for each anti-pattern. Each pattern includes **before/after code examples** in both Python and JavaScript to ensure technology-agnostic applicability.

---

## Pattern 1: Fix SQL Injection → Parameterized Queries

**Anti-Pattern:** AP-001 | **Severity:** CRITICAL

### Python — Before ❌

```python
# models.py
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES ('" + nome + "', " + str(preco) + ")"
)
cursor.execute(
    "UPDATE produtos SET nome = '" + nome + "' WHERE id = " + str(id)
)
```

### Python — After ✅

```python
# models/product_model.py
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    (nome, preco)
)
cursor.execute(
    "UPDATE produtos SET nome = ? WHERE id = ?",
    (nome, id)
)
```

### JavaScript — Before ❌

```javascript
db.run("SELECT * FROM courses WHERE id = " + courseId);
db.run(
  "INSERT INTO users (name, email) VALUES ('" + name + "', '" + email + "')",
);
```

### JavaScript — After ✅

```javascript
db.run("SELECT * FROM courses WHERE id = ?", [courseId]);
db.run("INSERT INTO users (name, email) VALUES (?, ?)", [name, email]);
```

---

## Pattern 2: Extract Hardcoded Config → Environment Variables

**Anti-Pattern:** AP-002 | **Severity:** CRITICAL

### Python — Before ❌

```python
# app.py
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True
```

### Python — After ✅

```python
# config/settings.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# app.py
from config.settings import Config
app.config.from_object(Config)
```

### JavaScript — Before ❌

```javascript
// utils.js
const config = {
  dbPass: "senha_super_secreta_prod_123",
  paymentGatewayKey: "pk_live_1234567890abcdef",
};
```

### JavaScript — After ✅

```javascript
// config/index.js
module.exports = {
  dbPass: process.env.DB_PASSWORD,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
  port: process.env.PORT || 3000,
};
```

---

## Pattern 3: Split God Class → Domain Models + Controllers

**Anti-Pattern:** AP-003 | **Severity:** CRITICAL

### Python — Before ❌

```python
# models.py (350 lines — products, users, orders, reports all in one file)
def get_todos_produtos(): ...
def criar_produto(...): ...
def get_todos_usuarios(): ...
def login_usuario(...): ...
def criar_pedido(...): ...
def relatorio_vendas(): ...
```

### Python — After ✅

```python
# models/product_model.py
class ProductModel:
    @staticmethod
    def get_all(): ...
    @staticmethod
    def create(name, price, stock): ...
    @staticmethod
    def search(term, category, min_price, max_price): ...

# models/user_model.py
class UserModel:
    @staticmethod
    def get_all(): ...
    @staticmethod
    def create(name, email, password): ...
    @staticmethod
    def authenticate(email, password): ...

# models/order_model.py
class OrderModel:
    @staticmethod
    def create(user_id, items): ...
    @staticmethod
    def get_by_user(user_id): ...

# controllers/product_controller.py
class ProductController:
    @staticmethod
    def list_products(): ...
    @staticmethod
    def create_product(data): ...
```

### JavaScript — Before ❌

```javascript
// AppManager.js (130 lines — db init, routes, checkout, reports all in one class)
class AppManager {
    initDb() { /* create tables */ }
    setupRoutes(app) {
        app.post('/api/checkout', ...);  // checkout logic inline
        app.get('/api/admin/financial-report', ...);  // report logic inline
        app.delete('/api/users/:id', ...);  // user deletion inline
    }
}
```

### JavaScript — After ✅

```javascript
// models/course.model.js
class Course {
    static findById(id) { ... }
    static findAllActive() { ... }
}

// controllers/checkout.controller.js
class CheckoutController {
    static async process(userData, courseId, cardInfo) { ... }
}

// routes/checkout.routes.js
router.post('/checkout', async (req, res) => {
    const result = await CheckoutController.process(...);
    res.json(result);
});
```

---

## Pattern 4: Hash Passwords Properly

**Anti-Pattern:** AP-004, AP-005 | **Severity:** CRITICAL

### Python — Before ❌

```python
# Plaintext
cursor.execute(
    "SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'"
)

# MD5 (broken)
import hashlib
self.password = hashlib.md5(pwd.encode()).hexdigest()
```

### Python — After ✅

```python
# Use bcrypt
import bcrypt

# When creating user
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# When authenticating
user = UserModel.find_by_email(email)
if user and bcrypt.checkpw(password.encode(), user.password_hash):
    return user
```

### JavaScript — Before ❌

```javascript
// Custom "crypto" (broken)
function badCrypto(pwd) {
  let hash = "";
  for (let i = 0; i < 10000; i++) {
    hash += Buffer.from(pwd).toString("base64").substring(0, 2);
  }
  return hash.substring(0, 10);
}
```

### JavaScript — After ✅

```javascript
const bcrypt = require("bcrypt");

// When creating user
const hash = await bcrypt.hash(password, 10);

// When authenticating
const user = await User.findByEmail(email);
if (user && (await bcrypt.compare(password, user.password_hash))) {
  return user;
}
```

---

## Pattern 5: Move Business Logic from Routes → Controllers

**Anti-Pattern:** AP-007 | **Severity:** HIGH

### Python — Before ❌

```python
# routes/task_routes.py — business logic in route handler
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400
    if len(title) < 3:
        return jsonify({'error': 'Título muito curto'}), 400
    if len(title) > 200:
        return jsonify({'error': 'Título muito longo'}), 400
    # ... 30 more lines of validation and business logic
    task = Task()
    task.title = title
    # ...
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201
```

### Python — After ✅

```python
# controllers/task_controller.py
class TaskController:
    @staticmethod
    def create_task(data):
        errors = []
        title = data.get('title', '').strip()
        if not title:
            errors.append('Title is required')
        elif len(title) < 3:
            errors.append('Title must be at least 3 characters')
        elif len(title) > 200:
            errors.append('Title must be at most 200 characters')

        priority = data.get('priority', 3)
        if priority < 1 or priority > 5:
            errors.append('Priority must be between 1 and 5')

        if errors:
            return None, errors

        task = Task(title=title, priority=priority, ...)
        db.session.add(task)
        db.session.commit()
        return task.to_dict(), None

# routes/task_routes.py
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    result, errors = TaskController.create_task(data)
    if errors:
        return jsonify({'errors': errors}), 400

    return jsonify(result), 201
```

---

## Pattern 6: Fix N+1 Queries → JOINs / Eager Loading

**Anti-Pattern:** AP-012 | **Severity:** MEDIUM

### Python — Before ❌

```python
# N+1: query orders, then for each order query items, then for each item query product name
def get_todos_pedidos():
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    for pedido in pedidos:
        cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(pedido["id"]))
        for item in cursor2:
            cursor3.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

### Python — After ✅

```python
# Single query with JOINs
def get_all_orders():
    cursor.execute("""
        SELECT
            p.id, p.status, p.total, p.criado_em,
            ip.quantidade, ip.preco_unitario,
            pr.nome as produto_nome, pr.id as produto_id
        FROM pedidos p
        LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = ip.produto_id
        ORDER BY p.id
    """)
    # Group results by order in application code
    orders = {}
    for row in cursor:
        if row["id"] not in orders:
            orders[row["id"]] = {
                "id": row["id"], "status": row["status"],
                "total": row["total"], "itens": []
            }
        orders[row["id"]]["itens"].append({
            "produto_id": row["produto_id"],
            "produto_nome": row["produto_nome"],
            "quantidade": row["quantidade"]
        })
    return list(orders.values())
```

### JavaScript — Before ❌

```javascript
// N+1: for each course, query enrollments, then for each enrollment query user, then payment
db.all("SELECT * FROM courses", [], (err, courses) => {
    courses.forEach(c => {
        db.all("SELECT * FROM enrollments WHERE course_id = ?", [c.id], (err, enrollments) => {
            enrollments.forEach(enr => {
                db.get("SELECT name FROM users WHERE id = ?", [enr.user_id], ...);
                db.get("SELECT amount FROM payments WHERE enrollment_id = ?", [enr.id], ...);
            });
        });
    });
});
```

### JavaScript — After ✅

```javascript
// Single query with JOINs
db.all(
  `
    SELECT
        c.title as course_title,
        u.name as student_name,
        p.amount as paid_amount
    FROM courses c
    LEFT JOIN enrollments e ON e.course_id = c.id
    LEFT JOIN users u ON u.id = e.user_id
    LEFT JOIN payments p ON p.enrollment_id = e.id
    WHERE p.status = 'PAID'
`,
  [],
  (err, rows) => {
    // Group by course in application code
    const report = rows.reduce((acc, row) => {
      // ... grouping logic
      return acc;
    }, []);
    res.json(report);
  },
);
```

---

## Pattern 7: Centralize Error Handling

**Anti-Pattern:** AP-016 | **Severity:** MEDIUM

### Python — Before ❌

```python
# Repeated in every route handler
try:
    # ... logic ...
except Exception as e:
    return jsonify({"erro": str(e)}), 500
```

### Python — After ✅

```python
# middlewares/error_handler.py
import logging
from flask import jsonify

logger = logging.getLogger(__name__)

class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'error': error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f'Internal error: {error}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

# routes/product_routes.py
@product_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = ProductController.get_product(id)
    if not product:
        raise AppError('Product not found', 404)
    return jsonify({'data': product}), 200
```

### JavaScript — Before ❌

```javascript
// Repeated try-catch in every route
app.get("/api/data", (req, res) => {
  try {
    // ... logic ...
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

### JavaScript — After ✅

```javascript
// middlewares/errorHandler.js
class AppError extends Error {
  constructor(message, statusCode = 400) {
    super(message);
    this.statusCode = statusCode;
  }
}

function errorHandler(err, req, res, next) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err.message });
  }
  console.error("Internal error:", err);
  res.status(500).json({ error: "Internal server error" });
}

// app.js
app.use(errorHandler);

// routes — just throw
router.get("/data", async (req, res, next) => {
  const data = await DataController.getData();
  if (!data) throw new AppError("Data not found", 404);
  res.json(data);
});
```

---

## Pattern 8: Replace Print/Console.log → Structured Logging

**Anti-Pattern:** AP-018 | **Severity:** LOW

### Python — Before ❌

```python
print("Servidor iniciado")
print("ERRO: " + str(e))
print("Produto criado com ID: " + str(id))
```

### Python — After ✅

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Server started on port %d", port)
logger.error("Failed to create product: %s", e, exc_info=True)
logger.info("Product created with ID: %d", product_id)
```

### JavaScript — Before ❌

```javascript
console.log("Server running on port 3000");
console.log("Error: " + err.message);
```

### JavaScript — After ✅

```javascript
const winston = require("winston");
const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [new winston.transports.Console()],
});

logger.info("Server started", { port: 3000 });
logger.error("Failed to process checkout", { error: err.message });
```

---

## Pattern 9: Extract Magic Numbers → Named Constants

**Anti-Pattern:** AP-019 | **Severity:** LOW

### Python — Before ❌

```python
if len(nome) < 2:
    return error("Nome muito curto")
if len(nome) > 200:
    return error("Nome muito longo")
if preco < 0:
    return error("Preço inválido")
```

### Python — After ✅

```python
# config/constants.py or at top of controller
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 200
MIN_PRICE = 0
VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']

if len(name) < MIN_NAME_LENGTH:
    raise AppError(f'Name must be at least {MIN_NAME_LENGTH} characters')
if len(name) > MAX_NAME_LENGTH:
    raise AppError(f'Name must be at most {MAX_NAME_LENGTH} characters')
if price < MIN_PRICE:
    raise AppError('Price cannot be negative')
```

---

## Pattern 10: Remove Sensitive Data from API Responses

**Anti-Pattern:** AP-011 | **Severity:** HIGH

### Python — Before ❌

```python
# models/user.py
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'password': self.password,  # LEAKING HASH!
        'role': self.role,
    }

# controllers.py — health check leaking secrets
return jsonify({
    "status": "ok",
    "secret_key": "minha-chave-super-secreta-123",
    "db_path": "loja.db",
    "debug": True,
})
```

### Python — After ✅

```python
# models/user.py
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'role': self.role,
        # password field intentionally excluded
    }

# controllers/health_controller.py
def health_check():
    return jsonify({
        "status": "ok",
        "database": "connected",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
```

---

## Pattern 11: Fix Deprecated APIs

**Anti-Pattern:** AP-017 | **Severity:** MEDIUM

### Python — Before ❌

```python
from datetime import datetime

created_at = datetime.utcnow()          # Deprecated in 3.12
due_date = datetime.utcnow() - timedelta(days=3)
```

### Python — After ✅

```python
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc)
due_date = datetime.now(timezone.utc) - timedelta(days=3)
```

### JavaScript — Before ❌

```javascript
const db = new sqlite3.Database(":memory:"); // Callback-based, no promises
db.serialize(() => {
  db.run("CREATE TABLE ...");
  db.run("INSERT ...");
});
```

### JavaScript — After ✅

```javascript
const sqlite3 = require("better-sqlite3");
const db = sqlite3(":memory:");

// Synchronous, simpler API
db.exec(`
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
    INSERT INTO users (name) VALUES ('Admin');
`);
```

---

## Pattern 12: Add Input Validation Layer

**Anti-Pattern:** AP-021 | **Severity:** LOW

### Python — Before ❌

```python
# No validation — accepts anything
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(title=data.get('title'), priority=data.get('priority'))
    db.session.add(task)
    db.session.commit()
```

### Python — After ✅

```python
# validators/task_validator.py
from marshmallow import Schema, fields, validate, ValidationError

class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    description = fields.Str(allow_none=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'in_progress', 'done', 'cancelled']))
    priority = fields.Int(validate=validate.Range(min=1, max=5))
    due_date = fields.Date(allow_none=True)

# routes/task_routes.py
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = TaskSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    result = TaskController.create_task(data)
    return jsonify(result), 201
```

---

## Transformation Priority Order

When executing Phase 3, apply transformations in this order:

1. **CRITICAL first** — Security and data integrity (Patterns 1, 2, 3, 4)
2. **HIGH second** — Architecture and design (Patterns 5, 10)
3. **MEDIUM third** — Performance and maintainability (Patterns 6, 7, 11)
4. **LOW fourth** — Code quality (Patterns 8, 9, 12)

Within each severity level, apply transformations that create new files/directories first, then modify existing files.
