# 📚 Dokumentasi Struktur Project - Best Practice

## 🎯 Overview

Struktur project mengikuti **Clean Architecture Pattern** dengan lapisan:

1. **Routes** - HTTP endpoint layer
2. **Controllers** - Request handler & response formatter
3. **Services** - Business logic layer
4. **Repositories** - Data access layer (Database queries)
5. **Schemas** - Data validation & serialization
6. **Models** - Database models (Entities)

---

## 📁 Struktur File untuk Fitur Merek Kendaraan

```
app/
├── models/
│   └── merek_model.py              # ✅ Database model (Merek)
│
├── schemas/
│   └── merek_schema.py             # ✅ NEW - Request/Response validation
│
├── repositories/
│   └── merek_repository.py         # ✅ NEW - Database operations (CRUD)
│
├── services/
│   └── merek_service.py            # ✅ NEW - Business logic
│
├── controllers/
│   └── merek_controller.py         # ✅ NEW - HTTP handlers
│
└── routes/
    ├── root_routes.py
    └── merek_routes.py             # ✅ NEW - Endpoint registration
```

---

## 🔄 Flow Perjalanan Request

```
REQUEST: GET /api/mereks?page=1&per_page=10&search=Honda
  ↓
1. merek_routes.py
   - Route handler menerima request
   - Validates path parameters
   ↓
2. merek_controller.py (MerekController.list_mereks())
   - Extract query parameters: page, per_page, search
   - Call service layer
   - Format response dengan schema
   ↓
3. merek_service.py (MerekService.get_all_mereks())
   - Validate business rules
   - Call repository
   - Return processed data
   ↓
4. merek_repository.py (MerekRepository.get_all())
   - Build database query
   - Apply filters (search)
   - Pagination
   - Execute query
   ↓
5. merek_model.py (Merek model)
   - Query database
   - Return ORM objects
   ↓
6. merek_schema.py (mereks_schema)
   - Serialize objects to JSON
   ↓
RESPONSE:
{
  "success": true,
  "message": "List merek berhasil diambil",
  "data": {
    "mereks": [
      {"id_merek": 1, "nama_merek": "Honda"},
      {"id_merek": 2, "nama_merek": "Toyota"}
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 2,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

## 📝 Penjelasan Setiap Layer

### 1️⃣ **Models** (app/models/)

Mendefinisikan struktur database dan relasi.

```python
# merek_model.py
class Merek(db.Model):
    __tablename__ = "merek"
    id_merek = db.Column(...)
    nama_merek = db.Column(...)
    model_kendaraans = db.relationship(...)  # Relasi ke ModelKendaraan
```

**Tanggung Jawab:**

- Define database schema
- Define relationships

---

### 2️⃣ **Repositories** (app/repositories/)

Data Access Layer - semua query database ada di sini.

```python
# merek_repository.py
class MerekRepository:
    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        """Query dengan pagination & filter"""
        query = Merek.query
        if search:
            query = query.filter(Merek.nama_merek.ilike(f"%{search}%"))
        return query.paginate(page, per_page)

    @staticmethod
    def get_by_id(id_merek):
        """Get single record"""
        return Merek.query.get(id_merek)

    @staticmethod
    def create(nama_merek):
        """Insert new record"""
        merek = Merek(nama_merek=nama_merek)
        db.session.add(merek)
        db.session.commit()
        return merek
```

**Tanggung Jawab:**

- Execute database queries (SELECT, INSERT, UPDATE, DELETE)
- Handle database transactions
- Return ORM objects

**Keuntungan:**

- ✅ All database queries in one place
- ✅ Easy to test (mock repository)
- ✅ Easy to switch database (just change repository)
- ✅ Reusable queries

---

### 3️⃣ **Services** (app/services/)

Business Logic Layer - semua rule bisnis ada di sini.

```python
# merek_service.py
class MerekService:
    @staticmethod
    def get_all_mereks(page=1, per_page=10, search=None):
        """Koordinasi business logic"""
        # Validasi parameter
        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")

        # Panggil repository
        items, total, total_pages = MerekRepository.get_all(
            page=page,
            per_page=per_page,
            search=search
        )

        # Return data yang sudah diproses
        return {
            'items': items,
            'pagination': {...}
        }

    @staticmethod
    def create_merek(nama_merek):
        """Validasi sebelum create"""
        if not nama_merek or not nama_merek.strip():
            raise ValueError("Nama merek tidak boleh kosong")

        return MerekRepository.create(nama_merek.strip())
```

**Tanggung Jawab:**

- Validasi business rules
- Koordinasi antar repositories
- Transform data
- Handle exceptions

**Keuntungan:**

- ✅ Business logic terisolasi
- ✅ Easy to test (mock repository)
- ✅ Reusable di controllers/CLI

---

### 4️⃣ **Controllers** (app/controllers/)

HTTP Request Handler - menerima request dan kirim response.

```python
# merek_controller.py
class MerekController:
    @staticmethod
    def list_mereks():
        """Handle GET /api/mereks"""
        try:
            # Extract request parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', None, type=str)

            # Call service
            result = MerekService.get_all_mereks(
                page=page,
                per_page=per_page,
                search=search
            )

            # Serialize & return
            items_serialized = mereks_schema.dump(result['items'])
            return success_response(
                message="List merek berhasil diambil",
                data={
                    'mereks': items_serialized,
                    'pagination': result['pagination']
                },
                status_code=200
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            return error_response(message="Server error", status_code=500)
```

**Tanggung Jawab:**

- Extract HTTP request parameters
- Call service layer
- Handle exceptions & return appropriate HTTP status
- Serialize response
- Format error messages

**Keuntungan:**

- ✅ HTTP layer terisolasi
- ✅ Easy to add logging/auth middleware
- ✅ Consistent error handling

---

### 5️⃣ **Schemas** (app/schemas/)

Request/Response validation dan serialization.

```python
# merek_schema.py
class MerekSchema(Schema):
    """Response schema"""
    id_merek = fields.Int(dump_only=True)
    nama_merek = fields.Str(required=True, validate=validate.Length(min=1, max=30))

class MerekCreateSchema(Schema):
    """Request schema"""
    nama_merek = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=30),
        error_messages={'required': 'Nama merek wajib diisi'}
    )

# Usage
merek_data = merek_schema.dump(merek_obj)  # Serialize
validated = merek_create_schema.load(request.json)  # Validate & deserialize
```

**Tanggung Jawab:**

- Validate request data
- Transform ORM objects to JSON
- Transform JSON to Python objects
- Provide consistent API format

**Keuntungan:**

- ✅ Input validation terpusat
- ✅ Auto error messages
- ✅ Consistent API format

---

### 6️⃣ **Routes** (app/routes/)

Endpoint registration dan URL mapping.

```python
# merek_routes.py
merek_bp = Blueprint('merek', __name__, url_prefix='/api/mereks')

@merek_bp.route('', methods=['GET'])
def list_mereks():
    return MerekController.list_mereks()

@merek_bp.route('', methods=['POST'])
def create_merek():
    return MerekController.create_merek()

@merek_bp.route('/<int:id_merek>', methods=['GET'])
def get_merek_detail(id_merek):
    return MerekController.get_merek_detail(id_merek)
```

**Tanggung Jawab:**

- Map URLs to controllers
- Group related endpoints (blueprint)
- Define HTTP methods

---

## 🧪 Testing Example

```python
# tests/test_merek.py

def test_list_mereks(client, app):
    """Test list endpoint"""
    response = client.get('/api/mereks?page=1&per_page=10')
    assert response.status_code == 200
    assert response.json['success'] == True
    assert 'mereks' in response.json['data']

def test_create_merek(client, app):
    """Test create endpoint"""
    response = client.post('/api/mereks', json={
        'nama_merek': 'Honda'
    })
    assert response.status_code == 201
    assert response.json['data']['merek']['nama_merek'] == 'Honda'

def test_invalid_input(client, app):
    """Test validation"""
    response = client.post('/api/mereks', json={
        'nama_merek': ''  # Invalid!
    })
    assert response.status_code == 400
    assert response.json['success'] == False
```

---

## 🚀 API Endpoints

```
GET    /api/mereks                          # List semua merek (with pagination & search)
POST   /api/mereks                          # Create merek baru
GET    /api/mereks/<id>                     # Get detail merek
PUT    /api/mereks/<id>                     # Update merek
DELETE /api/mereks/<id>                     # Delete merek
```

---

## 📊 Request/Response Examples

### 1. GET /api/mereks?page=1&per_page=10&search=Honda

**Request:**

```
GET /api/mereks?page=1&per_page=10&search=Honda HTTP/1.1
Host: localhost:5000
```

**Response (200):**

```json
{
  "success": true,
  "message": "List merek berhasil diambil",
  "data": {
    "mereks": [
      {
        "id_merek": 1,
        "nama_merek": "Honda"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 1,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

### 2. POST /api/mereks

**Request:**

```json
POST /api/mereks HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "nama_merek": "Toyota"
}
```

**Response (201):**

```json
{
  "success": true,
  "message": "Merek berhasil dibuat",
  "data": {
    "merek": {
      "id_merek": 3,
      "nama_merek": "Toyota"
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

### 3. PUT /api/mereks/1

**Request:**

```json
PUT /api/mereks/1 HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "nama_merek": "Honda Civic"
}
```

**Response (200):**

```json
{
  "success": true,
  "message": "Merek berhasil diupdate",
  "data": {
    "merek": {
      "id_merek": 1,
      "nama_merek": "Honda Civic"
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

### 4. DELETE /api/mereks/1

**Request:**

```
DELETE /api/mereks/1 HTTP/1.1
Host: localhost:5000
```

**Response (200):**

```json
{
  "success": true,
  "message": "Merek berhasil dihapus",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

### Error Response (400)

**Request:**

```json
POST /api/mereks HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "nama_merek": ""  # Empty!
}
```

**Response (400):**

```json
{
  "success": false,
  "message": "Validasi input gagal",
  "errors": {
    "nama_merek": ["Shorter than minimum length 1."]
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

## ✅ Best Practices yang Diterapkan

### 1. **Separation of Concerns**

- ✅ Each layer has single responsibility
- ✅ Database logic separate from business logic
- ✅ HTTP handling separate from business logic

### 2. **Dependency Injection**

- ✅ Service depends on Repository (injected)
- ✅ Controller depends on Service (injected)
- ✅ Easy to mock for testing

### 3. **Error Handling**

- ✅ Specific exceptions caught at each layer
- ✅ Appropriate HTTP status codes
- ✅ Descriptive error messages

### 4. **Validation**

- ✅ Input validation at schema layer
- ✅ Business rule validation at service layer
- ✅ Database constraint validation at repository layer

### 5. **Response Consistency**

- ✅ Standardized API response format
- ✅ Consistent error response format
- ✅ Pagination metadata included

### 6. **Code Reusability**

- ✅ Service can be reused (API, CLI, scheduled tasks)
- ✅ Repository can be reused across services
- ✅ Schema can be reused (request + response)

### 7. **Testability**

- ✅ Each layer can be tested independently
- ✅ Mock repositories for service tests
- ✅ Mock services for controller tests

### 8. **Documentation**

- ✅ Docstrings untuk setiap method
- ✅ Parameter types documented
- ✅ Return types documented
- ✅ Exceptions documented

---

## 🎓 Kesimpulan

Struktur ini mengikuti **Clean Architecture** dan memberikan:

- 🏗️ **Scalability** - easy to add new features
- 🧪 **Testability** - each layer can be tested
- 🔧 **Maintainability** - clear separation of concerns
- 🚀 **Productivity** - reusable components

Saat membuat fitur baru (misal: Model Kendaraan, User), ikuti pattern yang sama! 🎯
