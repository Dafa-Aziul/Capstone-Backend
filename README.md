## Backend Structure

This project uses a Flask app factory pattern so configuration and extension setup stay modular and easier to maintain.

### Main folders

- `app/`: main application package
- `app/config/`: application configuration classes
- `app/controllers/`: request handlers
- `app/services/`: business logic
- `app/repositories/`: database access layer
- `app/models/`: database models
- `app/routes/`: route registration
- `app/schemas/`: request and response schemas
- `app/middlewares/`: middleware helpers
- `app/utils/`: shared utilities
- `app/ml/`: machine learning related code
- `app/extensions.py`: shared Flask extensions such as `db`, `migrate`, and `jwt`
- `migrations/`: database migration files
- `tests/`: automated tests
- `uploads/`: uploaded runtime files
- `artifacts/`: generated artifacts

### Current architecture

- `app/__init__.py`: app factory, config loading, blueprint registration, and startup database logging
- `app/config/settings.py`: environment-based Flask configuration
- `app/routes/root_routes.py`: base API routes such as `/`, `/welcome`, and `/health`
- `app/utils/api_response.py`: standardized API response helpers
- `app/models/base.py`: reusable base model and timestamp mixin

### Model convention

- `BaseModel`: provides a standard integer primary key named `id`
- `TimestampMixin`: provides `created_at` and `updated_at`
- `to_dict()`: serializes model fields into a dictionary for simple API responses

Example:

```python
from app.extensions import db
from app.models import BaseModel, TimestampMixin


class ExampleModel(BaseModel, TimestampMixin):
    __tablename__ = "examples"

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
```

### API response standard

All API responses should use the shared helpers from `app/utils/api_response.py`.

Success response format:

```json
{
  "success": true,
  "message": "Request successful",
  "timestamp": "2026-06-02T06:39:04.414871+00:00",
  "data": {
    "example": "value"
  },
  "meta": {
    "page": 1
  }
}
```

Notes:

- field order is `success`, `message`, `timestamp`, `data`, `meta`
- `data` is optional and only appears when provided
- `meta` is optional and only appears when provided
- `timestamp` is generated automatically in UTC ISO 8601 format

Usage:

```python
from app.utils.api_response import error_response, success_response

return success_response("Data fetched successfully")
return success_response("Data fetched successfully", data=result)
return success_response("Data fetched successfully", data=result, meta=pagination)
return error_response("Validation failed", errors=validation_errors, status_code=422)
```

### Root endpoints

- `GET /`: base API welcome response
- `GET /welcome`: simple welcome endpoint
- `GET /health`: health check endpoint

### Database startup logging

When the Flask app starts, it performs a simple database connectivity check using `SELECT 1`.

If the connection succeeds, the app logs:

```text
Database connection successful.
```

If the connection fails, the app logs the exception for debugging.

### Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file with:

```env
PORT=5000
DB_HOST=localhost
DB_PORT=3306
DB_NAME=capstone
DB_USER=root
DB_PASSWORD=your_password
JWT_SECRET_KEY=your_secret_key
FLASK_ENV=development
```

### Run

```bash
python run.py
```

### Notes

- `venv/`, `__pycache__/`, `.env`, `uploads/`, and `artifacts/` are ignored by Git through `.gitignore`
- `__pycache__/` is a Python-generated cache directory and should not be committed
