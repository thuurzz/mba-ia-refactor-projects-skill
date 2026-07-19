# MVC Architecture Guidelines

Target architecture rules for the refactoring process. These guidelines are **technology-agnostic** — they apply to Python/Flask, Node.js/Express, Ruby/Rails, PHP/Laravel, Java/Spring, and any other backend framework.

---

## Core Principle: Separation of Concerns

Every file in the project must have **ONE clear responsibility**. If a file does more than one thing, it should be split.

---

## Layer Definitions

### 1. Models (Data Layer)

**Responsibility:** Data access ONLY. No business logic, no HTTP concerns, no validation beyond schema constraints.

**What goes here:**

- Database schema definitions (ORM models, table definitions)
- CRUD operations (create, read, update, delete)
- Query methods (find by id, find by email, search with filters)
- Data serialization (`to_dict()`, `toJSON()`)
- Relationship definitions (foreign keys, joins)

**What does NOT go here:**

- Business rules (e.g., "order total must be > 0")
- HTTP request/response handling
- Authentication/authorization logic
- Email sending, notifications
- Input validation (beyond database constraints)

**Naming convention:**

- Python: `<entity>_model.py` or `<entity>.py` (e.g., `product_model.py`, `user.py`)
- Node.js: `<entity>.model.js` (e.g., `product.model.js`)
- One file per domain entity

**Example (Python/Flask + SQLAlchemy):**

```python
# models/product.py
from database import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    @staticmethod
    def find_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def search(term=None, category=None, min_price=None, max_price=None):
        query = Product.query
        if term:
            query = query.filter(Product.name.ilike(f'%{term}%'))
        if category:
            query = query.filter(Product.category == category)
        return query.all()
```

**Example (Node.js/Express):**

```javascript
// models/course.model.js
const db = require("../config/database");

class Course {
  static findById(id) {
    return new Promise((resolve, reject) => {
      db.get("SELECT * FROM courses WHERE id = ?", [id], (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  }

  static findAllActive() {
    return new Promise((resolve, reject) => {
      db.all("SELECT * FROM courses WHERE active = 1", [], (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  }
}

module.exports = Course;
```

---

### 2. Controllers (Business Logic Layer)

**Responsibility:** Business logic and orchestration. Controllers know WHAT to do, not HOW to do HTTP.

**What goes here:**

- Business rules and validations
- Orchestrating multiple model calls
- Applying domain logic (calculations, state transitions)
- Calling services (email, notifications)
- Preparing data for the view/response

**What does NOT go here:**

- HTTP request parsing (`request.json`, `req.body`)
- HTTP response formatting (`jsonify()`, `res.json()`)
- Route definitions (`@app.route`, `app.get()`)
- Direct SQL queries (use models)

**Naming convention:**

- Python: `<entity>_controller.py` (e.g., `product_controller.py`)
- Node.js: `<entity>.controller.js` (e.g., `product.controller.js`)

**Example (Python/Flask):**

```python
# controllers/product_controller.py
from models.product import Product

class ProductController:
    @staticmethod
    def list_products():
        products = Product.query.all()
        return [p.to_dict() for p in products]

    @staticmethod
    def create_product(data):
        # Business validation
        errors = []
        if not data.get('name') or len(data['name']) < 2:
            errors.append('Name must be at least 2 characters')
        if data.get('price', 0) < 0:
            errors.append('Price cannot be negative')
        if errors:
            return None, errors

        product = Product(
            name=data['name'],
            price=data['price'],
            stock=data.get('stock', 0)
        )
        db.session.add(product)
        db.session.commit()
        return product.to_dict(), None
```

**Example (Node.js/Express):**

```javascript
// controllers/checkout.controller.js
const Course = require("../models/course.model");
const User = require("../models/user.model");
const Enrollment = require("../models/enrollment.model");

class CheckoutController {
  static async processCheckout(userData, courseId, cardInfo) {
    // Business logic
    const course = await Course.findById(courseId);
    if (!course) {
      throw new Error("Course not found");
    }

    let user = await User.findByEmail(userData.email);
    if (!user) {
      user = await User.create(userData);
    }

    const paymentResult = await PaymentService.process(cardInfo, course.price);
    if (!paymentResult.success) {
      throw new Error("Payment declined");
    }

    const enrollment = await Enrollment.create(user.id, courseId, course.price);
    return { enrollment_id: enrollment.id, status: "success" };
  }
}
```

---

### 3. Routes / Views (HTTP Layer)

**Responsibility:** HTTP concerns ONLY. Parse requests, call controllers, format responses.

**What goes here:**

- Route definitions (URL patterns, HTTP methods)
- Request parsing (query params, body, headers)
- Response formatting (JSON, status codes)
- Calling the appropriate controller method
- Basic request validation (is the body present? is the ID an integer?)

**What does NOT go here:**

- Business logic
- Database queries
- Complex validations
- String formatting for business purposes

**Naming convention:**

- Python: `<entity>_routes.py` (e.g., `product_routes.py`)
- Node.js: `<entity>.routes.js` (e.g., `product.routes.js`)

**Example (Python/Flask):**

```python
# routes/product_routes.py
from flask import Blueprint, request, jsonify
from controllers.product_controller import ProductController

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
def list_products():
    try:
        products = ProductController.list_products()
        return jsonify({'data': products, 'success': True}), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    result, errors = ProductController.create_product(data)
    if errors:
        return jsonify({'errors': errors}), 400

    return jsonify({'data': result, 'success': True}), 201
```

**Example (Node.js/Express):**

```javascript
// routes/checkout.routes.js
const express = require("express");
const router = express.Router();
const CheckoutController = require("../controllers/checkout.controller");

router.post("/checkout", async (req, res) => {
  try {
    const { user, course_id, card } = req.body;
    if (!user || !course_id || !card) {
      return res.status(400).json({ error: "Missing required fields" });
    }
    const result = await CheckoutController.processCheckout(
      user,
      course_id,
      card,
    );
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
```

---

### 4. Config (Configuration Layer)

**Responsibility:** Centralize ALL configuration. Nothing hardcoded anywhere else.

**What goes here:**

- Environment variables
- Database connection strings
- API keys and secrets
- Feature flags
- Application settings (port, debug mode, CORS origins)

**Example (Python):**

```python
# config/settings.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-me')
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
    PORT = int(os.environ.get('PORT', 5000))
```

**Example (Node.js):**

```javascript
// config/index.js
module.exports = {
  port: process.env.PORT || 3000,
  dbPath: process.env.DB_PATH || ":memory:",
  jwtSecret: process.env.JWT_SECRET,
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
  smtp: {
    host: process.env.SMTP_HOST,
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
};
```

---

### 5. Middlewares (Cross-Cutting Layer)

**Responsibility:** Request/response pipeline concerns that apply across routes.

**What goes here:**

- Error handling (global error handler)
- Authentication/authorization checks
- Request logging
- CORS configuration
- Rate limiting

**Example (Python/Flask):**

```python
# middlewares/error_handler.py
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
```

---

### 6. Services (Optional — Cross-Cutting Business Logic)

**Responsibility:** Business logic that spans multiple domains or integrates with external systems.

**What goes here:**

- Email sending
- Push notifications
- Payment processing
- File upload/download
- Third-party API integrations

---

## Directory Structure

### Python/Flask Target:

```
project/
├── config/
│   ├── __init__.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   └── <entity>.py
├── controllers/
│   ├── __init__.py
│   └── <entity>_controller.py
├── routes/
│   ├── __init__.py
│   └── <entity>_routes.py
├── middlewares/
│   ├── __init__.py
│   └── error_handler.py
├── services/
│   ├── __init__.py
│   └── <service>.py
├── app.py                  # Entry point
├── requirements.txt
└── .env.example
```

### Node.js/Express Target:

```
project/
├── src/
│   ├── config/
│   │   └── index.js
│   ├── models/
│   │   └── <entity>.model.js
│   ├── controllers/
│   │   └── <entity>.controller.js
│   ├── routes/
│   │   └── <entity>.routes.js
│   ├── middlewares/
│   │   └── errorHandler.js
│   ├── services/
│   │   └── <service>.js
│   └── app.js              # Entry point
├── package.json
└── .env.example
```

---

## Entry Point (app.py / app.js)

The entry point should be THIN — it only wires things together:

```python
# app.py
from flask import Flask
from config.settings import Config
from routes.product_routes import product_bp
from routes.user_routes import user_bp
from middlewares.error_handler import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)

    # Register error handlers
    register_error_handlers(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT)
```

---

## Validation Checklist

After refactoring, verify:

- [ ] No file has more than one responsibility
- [ ] No business logic in routes
- [ ] No HTTP concerns in models
- [ ] No hardcoded configuration values
- [ ] All secrets come from environment variables
- [ ] All SQL uses parameterized queries
- [ ] Error handling is centralized
- [ ] Entry point is thin (just wiring)
