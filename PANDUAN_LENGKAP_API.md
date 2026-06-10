# 📚 Panduan Lengkap API - Struktur, Template & Contoh Penggunaan

Dokumentasi komprehensif untuk membangun fitur API yang konsisten menggunakan clean architecture dan response standardisasi.

---

# Table of Contents

1. [🎯 Ringkasan](#ringkasan)
2. [📦 Response Functions](#response-functions)
3. [📋 HTTP Status Codes](#http-status-codes)
4. [📐 Template untuk Membuat Fitur Baru](#template-fitur-baru)
5. [📝 Response Examples](#response-examples)
6. [📚 Contoh Penggunaan API](#contoh-penggunaan-api)
7. [✅ Checklists](#checklists)

---

<a name="ringkasan"></a>

# 🎯 Ringkasan

Semua response API menggunakan fungsi **standar** dari `app/utils/api_response.py` untuk memastikan **konsistensi format** di seluruh aplikasi.

## Prinsip Utama

- **Konsistensi**: Semua response format sama di setiap endpoint
- **Clean Architecture**: Struktur 5-layer (Schema → Repository → Service → Controller → Routes)
- **DRY Principle**: Tidak ada duplicate code, semua response logic terpusat di `api_response.py`
- **Professional**: Response format yang clean, terstruktur, dan mudah dipahami client

---

<a name="response-functions"></a>

# 📦 Response Functions

Semua controller **HARUS** menggunakan fungsi-fungsi ini dari `app/utils/api_response.py`.

## 1. `success_response(message, data=None, meta=None, status_code=200)`

Digunakan untuk response yang sukses (GET, POST, PUT, DELETE berhasil).

### Syntax

```python
from app.utils.api_response import success_response

return success_response(
    message="String deskriptif",
    data={...},         # optional - payload response
    meta={...},         # optional - metadata tambahan
    status_code=200     # 200 atau 201
)
```

### Contoh Penggunaan

```python
# ✅ Response dengan data (List)
return success_response(
    message="List merek berhasil diambil",
    data={
        'mereks': items_serialized,
        'pagination': pagination_info
    },
    status_code=200
)

# ✅ Response dengan data (Single record)
return success_response(
    message="Merek berhasil dibuat",
    data={'merek': merek_data},
    status_code=201
)

# ✅ Response tanpa data (Delete success)
return success_response(
    message="Merek berhasil dihapus",
    status_code=200
)

# ✅ Response dengan meta info
return success_response(
    message="Operation completed",
    data={'result': data},
    meta={'version': '1.0'},
    status_code=200
)
```

### Format Response

```json
{
  "success": true,
  "message": "string",
  "data": {}, // optional - hanya jika ada payload
  "meta": {}, // optional - hanya jika ada metadata
  "timestamp": "ISO 8601 format (UTC)"
}
```

---

## 2. `error_response(message, errors=None, status_code=400)`

Digunakan untuk response yang error (validation error, not found, server error, dll).

### Syntax

```python
from app.utils.api_response import error_response

return error_response(
    message="String deskriptif error",
    errors={...},       # optional - detail error
    status_code=400     # 400, 404, 409, 500, dll
)
```

### Contoh Penggunaan

```python
# ❌ Error tanpa detail
return error_response(
    message="Merek dengan nama 'Honda' sudah ada",
    status_code=400
)

# ❌ Error dengan detail (validation errors)
return error_response(
    message="Validasi input gagal",
    errors={
        'nama_merek': ['Length must be between 1 and 30.']
    },
    status_code=400
)

# ❌ Error 404
return error_response(
    message="Merek dengan ID 999 tidak ditemukan",
    status_code=404
)

# ❌ Server error dengan exception detail
return error_response(
    message="Terjadi kesalahan saat mengambil data",
    errors=str(exception),
    status_code=500
)

# ❌ Conflict error
return error_response(
    message="Tidak bisa hapus merek 'Honda' karena masih ada model kendaraan",
    status_code=409
)
```

### Format Response

```json
{
  "success": false,
  "message": "string",
  "errors": {}, // optional - hanya jika ada detail error
  "timestamp": "ISO 8601 format (UTC)"
}
```

---

<a name="http-status-codes"></a>

# 📋 HTTP Status Codes yang Digunakan

| Code    | Meaning      | Digunakan saat                                       | Contoh                              |
| ------- | ------------ | ---------------------------------------------------- | ----------------------------------- |
| **200** | OK           | GET berhasil, PUT berhasil, DELETE berhasil          | `success_response(status_code=200)` |
| **201** | Created      | POST (create) berhasil                               | `success_response(status_code=201)` |
| **400** | Bad Request  | Validasi gagal, input invalid, duplikat data         | `error_response(status_code=400)`   |
| **404** | Not Found    | Resource tidak ditemukan                             | `error_response(status_code=404)`   |
| **409** | Conflict     | Konflik data (e.g., tidak bisa delete karena relasi) | `error_response(status_code=409)`   |
| **500** | Server Error | Database error, unhandled exception                  | `error_response(status_code=500)`   |

---

<a name="template-fitur-baru"></a>

# 📐 Template untuk Membuat Fitur Baru

Panduan lengkap membuat fitur baru dengan clean architecture dan response yang konsisten.

## 📋 Struktur File yang Diperlukan

Untuk setiap fitur baru (contoh: `feature_name`), buat 5 file:

```
app/
├── schemas/feature_name_schema.py           # 1. Validasi & Serialization
├── repositories/feature_name_repository.py  # 2. Database queries
├── services/feature_name_service.py         # 3. Business logic
├── controllers/feature_name_controller.py   # 4. HTTP handlers
└── routes/feature_name_routes.py            # 5. Endpoint registration
```

---

## 1️⃣ Schema (Input Validation & Serialization)

```python
# app/schemas/feature_name_schema.py

from marshmallow import Schema, fields, validate


class FeatureNameSchema(Schema):
    """Schema untuk response"""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))

    class Meta:
        fields = ('id', 'name')


class FeatureNameCreateSchema(Schema):
    """Schema untuk request create/update"""

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={'required': 'Name is required'}
    )


# Instances untuk reuse
feature_name_schema = FeatureNameSchema()
feature_names_schema = FeatureNameSchema(many=True)
feature_name_create_schema = FeatureNameCreateSchema()
```

---

## 2️⃣ Repository (Database Access Layer)

```python
# app/repositories/feature_name_repository.py

from app.extensions import db
from app.models.feature_name_model import FeatureName


class FeatureNameRepository:
    """Repository untuk database operations"""

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        """Get all records with pagination & search"""
        query = FeatureName.query

        if search:
            query = query.filter(FeatureName.name.ilike(f"%{search}%"))

        query = query.order_by(FeatureName.name.asc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated.items, paginated.total, paginated.pages

    @staticmethod
    def get_by_id(id):
        """Get single record"""
        return FeatureName.query.get(id)

    @staticmethod
    def create(name):
        """Create new record"""
        record = FeatureName(name=name)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def update(id, name):
        """Update record"""
        record = FeatureNameRepository.get_by_id(id)
        if not record:
            raise ValueError(f"Record with ID {id} not found")

        record.name = name
        db.session.commit()
        return record

    @staticmethod
    def delete(id):
        """Delete record"""
        record = FeatureNameRepository.get_by_id(id)
        if not record:
            raise ValueError(f"Record with ID {id} not found")

        db.session.delete(record)
        db.session.commit()
        return True
```

---

## 3️⃣ Service (Business Logic)

```python
# app/services/feature_name_service.py

from app.repositories.feature_name_repository import FeatureNameRepository


class FeatureNameService:
    """Service untuk business logic"""

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        """Get all with validation"""
        if page < 1:
            raise ValueError("Page must be >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page must be between 1-100")

        items, total, total_pages = FeatureNameRepository.get_all(
            page=page,
            per_page=per_page,
            search=search
        )

        return {
            'items': items,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }

    @staticmethod
    def get_by_id(id):
        """Get single record"""
        record = FeatureNameRepository.get_by_id(id)
        if not record:
            raise ValueError(f"Record with ID {id} not found")
        return record

    @staticmethod
    def create(name):
        """Create new record"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        return FeatureNameRepository.create(name.strip())

    @staticmethod
    def update(id, name):
        """Update record"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        return FeatureNameRepository.update(id, name.strip())

    @staticmethod
    def delete(id):
        """Delete record"""
        return FeatureNameRepository.delete(id)
```

---

## 4️⃣ Controller (HTTP Handlers) - ⭐ **MENGGUNAKAN api_response.py**

```python
# app/controllers/feature_name_controller.py

from flask import request
from app.services.feature_name_service import FeatureNameService
from app.schemas.feature_name_schema import (
    feature_name_schema,
    feature_names_schema,
    feature_name_create_schema
)
# ✅ IMPORT DARI api_response.py - MANDATORY
from app.utils.api_response import success_response, error_response
from marshmallow import ValidationError


class FeatureNameController:
    """Controller untuk HTTP handling"""

    @staticmethod
    def list_all():
        """GET /api/feature-names"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            search = request.args.get('search', None, type=str)

            result = FeatureNameService.get_all(
                page=page,
                per_page=per_page,
                search=search
            )

            items_serialized = feature_names_schema.dump(result['items'])

            # ✅ GUNAKAN success_response
            return success_response(
                message="Records retrieved successfully",
                data={
                    'records': items_serialized,
                    'pagination': result['pagination']
                },
                status_code=200
            )

        except ValueError as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message=str(e),
                status_code=400
            )
        except Exception as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message="Error retrieving records",
                errors=str(e),
                status_code=500
            )

    @staticmethod
    def get_detail(id):
        """GET /api/feature-names/<id>"""
        try:
            record = FeatureNameService.get_by_id(id)
            record_data = feature_name_schema.dump(record)

            # ✅ GUNAKAN success_response
            return success_response(
                message="Record retrieved successfully",
                data={'record': record_data},
                status_code=200
            )

        except ValueError as e:
            # ✅ GUNAKAN error_response dengan status 404
            return error_response(
                message=str(e),
                status_code=404
            )
        except Exception as e:
            # ✅ GUNAKAN error_response dengan status 500
            return error_response(
                message="Error retrieving record",
                errors=str(e),
                status_code=500
            )

    @staticmethod
    def create():
        """POST /api/feature-names"""
        try:
            data = request.get_json()
            if not data:
                # ✅ GUNAKAN error_response
                return error_response(
                    message="Request body is required",
                    status_code=400
                )

            validated_data = feature_name_create_schema.load(data)
            record = FeatureNameService.create(validated_data['name'])
            record_data = feature_name_schema.dump(record)

            # ✅ GUNAKAN success_response dengan status 201
            return success_response(
                message="Record created successfully",
                data={'record': record_data},
                status_code=201
            )

        except ValidationError as e:
            # ✅ GUNAKAN error_response dengan validation errors
            return error_response(
                message="Validation failed",
                errors=e.messages,
                status_code=400
            )
        except ValueError as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message=str(e),
                status_code=400
            )
        except Exception as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message="Error creating record",
                errors=str(e),
                status_code=500
            )

    @staticmethod
    def update(id):
        """PUT /api/feature-names/<id>"""
        try:
            data = request.get_json()
            if not data:
                # ✅ GUNAKAN error_response
                return error_response(
                    message="Request body is required",
                    status_code=400
                )

            validated_data = feature_name_create_schema.load(data)
            record = FeatureNameService.update(id, validated_data['name'])
            record_data = feature_name_schema.dump(record)

            # ✅ GUNAKAN success_response
            return success_response(
                message="Record updated successfully",
                data={'record': record_data},
                status_code=200
            )

        except ValidationError as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message="Validation failed",
                errors=e.messages,
                status_code=400
            )
        except ValueError as e:
            # ✅ GUNAKAN error_response
            error_msg = str(e)
            status = 404 if "not found" in error_msg else 400
            return error_response(
                message=error_msg,
                status_code=status
            )
        except Exception as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message="Error updating record",
                errors=str(e),
                status_code=500
            )

    @staticmethod
    def delete(id):
        """DELETE /api/feature-names/<id>"""
        try:
            FeatureNameService.delete(id)

            # ✅ GUNAKAN success_response
            return success_response(
                message="Record deleted successfully",
                status_code=200
            )

        except ValueError as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message=str(e),
                status_code=404
            )
        except Exception as e:
            # ✅ GUNAKAN error_response
            return error_response(
                message="Error deleting record",
                errors=str(e),
                status_code=500
            )
```

---

## 5️⃣ Routes (Endpoint Registration & URL Mapping)

```python
# app/routes/feature_name_routes.py

from flask import Blueprint
from app.controllers.feature_name_controller import FeatureNameController

feature_name_bp = Blueprint('feature_name', __name__, url_prefix='/api/feature-names')

@feature_name_bp.route('', methods=['GET'])
def list_all():
    return FeatureNameController.list_all()

@feature_name_bp.route('', methods=['POST'])
def create():
    return FeatureNameController.create()

@feature_name_bp.route('/<int:id>', methods=['GET'])
def get_detail(id):
    return FeatureNameController.get_detail(id)

@feature_name_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    return FeatureNameController.update(id)

@feature_name_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    return FeatureNameController.delete(id)
```

---

## 6️⃣ Register Blueprint di app/**init**.py

```python
def register_blueprints(app):
    from app.routes.root_routes import root_bp
    from app.routes.merek_routes import merek_bp
    from app.routes.feature_name_routes import feature_name_bp  # ✅ ADD THIS

    app.register_blueprint(root_bp)
    app.register_blueprint(merek_bp)
    app.register_blueprint(feature_name_bp)  # ✅ ADD THIS
```

---

<a name="response-examples"></a>

# 📝 Response Examples

Contoh response untuk berbagai endpoint dan skenario.

## ✅ Success Responses

### GET /api/mereks - List Success (200)

```json
{
  "success": true,
  "message": "List merek berhasil diambil",
  "data": {
    "mereks": [
      { "id_merek": 1, "nama_merek": "Honda" },
      { "id_merek": 2, "nama_merek": "Toyota" },
      { "id_merek": 3, "nama_merek": "BMW" }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 3,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### GET /api/mereks/1 - Get Detail (200)

```json
{
  "success": true,
  "message": "Detail merek berhasil diambil",
  "data": {
    "merek": {
      "id_merek": 1,
      "nama_merek": "Honda"
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### POST /api/mereks - Create Success (201)

```json
{
  "success": true,
  "message": "Merek berhasil dibuat",
  "data": {
    "merek": {
      "id_merek": 4,
      "nama_merek": "Nissan"
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### PUT /api/mereks/4 - Update Success (200)

```json
{
  "success": true,
  "message": "Merek berhasil diupdate",
  "data": {
    "merek": {
      "id_merek": 4,
      "nama_merek": "Nissan Leaf"
    }
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### DELETE /api/mereks/4 - Delete Success (200)

```json
{
  "success": true,
  "message": "Merek berhasil dihapus",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

## ❌ Error Responses

### Validation Error (400)

```json
{
  "success": false,
  "message": "Validasi input gagal",
  "errors": {
    "nama_merek": ["Length must be between 1 and 30."]
  },
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### Not Found (404)

```json
{
  "success": false,
  "message": "Merek dengan ID 999 tidak ditemukan",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### Duplicate/Bad Request (400)

```json
{
  "success": false,
  "message": "Merek dengan nama 'Honda' sudah ada",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### Conflict - Cannot Delete (409)

```json
{
  "success": false,
  "message": "Tidak bisa hapus merek 'Honda' karena masih ada model kendaraan yang terkait",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

### Server Error (500)

```json
{
  "success": false,
  "message": "Terjadi kesalahan saat mengambil data merek",
  "errors": "database connection error details",
  "timestamp": "2026-06-03T10:30:00+00:00"
}
```

---

<a name="contoh-penggunaan-api"></a>

# 📚 Contoh Penggunaan API (Client Side)

Contoh implementasi dari berbagai client platform.

## 🛠️ Setup

### Menggunakan cURL

```bash
BASE_URL=http://localhost:5000
```

### Menggunakan Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"
```

### Menggunakan JavaScript Fetch

```javascript
const BASE_URL = "http://localhost:5000";
```

---

## 1️⃣ List Semua Merek

### cURL

```bash
curl -X GET \
  "http://localhost:5000/api/mereks?page=1&per_page=10" \
  -H "Content-Type: application/json"
```

### Python

```python
import requests

response = requests.get(f"{BASE_URL}/api/mereks", params={
    'page': 1,
    'per_page': 10
})

data = response.json()
print(f"Total merek: {data['data']['pagination']['total_items']}")
for merek in data['data']['mereks']:
    print(f"- {merek['nama_merek']}")
```

### JavaScript

```javascript
fetch(`${BASE_URL}/api/mereks?page=1&per_page=10`)
  .then((res) => res.json())
  .then((data) => {
    console.log("Total merek:", data.data.pagination.total_items);
    data.data.mereks.forEach((merek) => {
      console.log(`- ${merek.nama_merek}`);
    });
  })
  .catch((err) => console.error(err));
```

---

## 2️⃣ Search Merek

### cURL

```bash
curl -X GET \
  "http://localhost:5000/api/mereks?page=1&per_page=10&search=Honda" \
  -H "Content-Type: application/json"
```

### Python

```python
response = requests.get(f"{BASE_URL}/api/mereks", params={
    'page': 1,
    'per_page': 10,
    'search': 'Honda'
})

data = response.json()
for merek in data['data']['mereks']:
    print(f"Found: {merek['nama_merek']}")
```

### JavaScript

```javascript
const search = "Honda";
fetch(`${BASE_URL}/api/mereks?page=1&per_page=10&search=${search}`)
  .then((res) => res.json())
  .then((data) => {
    console.log(`Found ${data.data.mereks.length} merek`);
    data.data.mereks.forEach((merek) => {
      console.log(`- ${merek.nama_merek}`);
    });
  });
```

---

## 3️⃣ Get Detail Merek

### cURL

```bash
curl -X GET \
  "http://localhost:5000/api/mereks/1" \
  -H "Content-Type: application/json"
```

### Python

```python
merek_id = 1
response = requests.get(f"{BASE_URL}/api/mereks/{merek_id}")

data = response.json()
merek = data['data']['merek']
print(f"Merek: {merek['nama_merek']}")
```

### JavaScript

```javascript
const merekId = 1;
fetch(`${BASE_URL}/api/mereks/${merekId}`)
  .then((res) => res.json())
  .then((data) => {
    const merek = data.data.merek;
    console.log(`Merek: ${merek.nama_merek}`);
  });
```

---

## 4️⃣ Create Merek Baru

### cURL

```bash
curl -X POST \
  "http://localhost:5000/api/mereks" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_merek": "Nissan"
  }'
```

### Python

```python
response = requests.post(f"{BASE_URL}/api/mereks", json={
    "nama_merek": "Nissan"
})

data = response.json()
if response.status_code == 201:
    print(f"✅ Merek berhasil dibuat: {data['data']['merek']['nama_merek']}")
else:
    print(f"❌ Error: {data['message']}")
```

### JavaScript

```javascript
const newMerek = {
  nama_merek: "Nissan",
};

fetch(`${BASE_URL}/api/mereks`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(newMerek),
})
  .then((res) => res.json())
  .then((data) => {
    if (data.success) {
      console.log(`✅ Merek berhasil dibuat: ${data.data.merek.nama_merek}`);
    } else {
      console.log(`❌ Error: ${data.message}`);
    }
  });
```

---

## 5️⃣ Update Merek

### cURL

```bash
curl -X PUT \
  "http://localhost:5000/api/mereks/4" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_merek": "Nissan Leaf"
  }'
```

### Python

```python
merek_id = 4
response = requests.put(f"{BASE_URL}/api/mereks/{merek_id}", json={
    "nama_merek": "Nissan Leaf"
})

data = response.json()
if response.status_code == 200:
    print(f"✅ Merek berhasil diupdate: {data['data']['merek']['nama_merek']}")
else:
    print(f"❌ Error: {data['message']}")
```

### JavaScript

```javascript
const merekId = 4;
const updatedMerek = {
  nama_merek: "Nissan Leaf",
};

fetch(`${BASE_URL}/api/mereks/${merekId}`, {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(updatedMerek),
})
  .then((res) => res.json())
  .then((data) => {
    if (data.success) {
      console.log(`✅ Merek berhasil diupdate: ${data.data.merek.nama_merek}`);
    } else {
      console.log(`❌ Error: ${data.message}`);
    }
  });
```

---

## 6️⃣ Delete Merek

### cURL

```bash
curl -X DELETE \
  "http://localhost:5000/api/mereks/4" \
  -H "Content-Type: application/json"
```

### Python

```python
merek_id = 4
response = requests.delete(f"{BASE_URL}/api/mereks/{merek_id}")

data = response.json()
if response.status_code == 200:
    print(f"✅ Merek berhasil dihapus")
else:
    print(f"❌ Error: {data['message']}")
```

### JavaScript

```javascript
const merekId = 4;

fetch(`${BASE_URL}/api/mereks/${merekId}`, {
  method: "DELETE",
  headers: {
    "Content-Type": "application/json",
  },
})
  .then((res) => res.json())
  .then((data) => {
    if (data.success) {
      console.log("✅ Merek berhasil dihapus");
    } else {
      console.log(`❌ Error: ${data.message}`);
    }
  });
```

---

## 🔄 Complete Flow Example (Python)

```python
import requests

BASE_URL = "http://localhost:5000"

def main():
    # 1. List semua merek
    print("1️⃣ List semua merek")
    response = requests.get(f"{BASE_URL}/api/mereks")
    print(response.json())
    print()

    # 2. Create merek baru
    print("2️⃣ Create merek baru")
    response = requests.post(f"{BASE_URL}/api/mereks", json={
        "nama_merek": "Chevrolet"
    })
    print(response.json())
    new_merek_id = response.json()['data']['merek']['id_merek']
    print()

    # 3. Get detail merek
    print("3️⃣ Get detail merek")
    response = requests.get(f"{BASE_URL}/api/mereks/{new_merek_id}")
    print(response.json())
    print()

    # 4. Update merek
    print("4️⃣ Update merek")
    response = requests.put(f"{BASE_URL}/api/mereks/{new_merek_id}", json={
        "nama_merek": "Chevrolet Malibu"
    })
    print(response.json())
    print()

    # 5. Search merek
    print("5️⃣ Search merek")
    response = requests.get(f"{BASE_URL}/api/mereks", params={
        'search': 'Chevrolet'
    })
    print(response.json())
    print()

    # 6. Delete merek
    print("6️⃣ Delete merek")
    response = requests.delete(f"{BASE_URL}/api/mereks/{new_merek_id}")
    print(response.json())

if __name__ == "__main__":
    main()
```

---

<a name="checklists"></a>

# ✅ Checklists

## ✅ Checklist Membuat Fitur Baru

Gunakan checklist ini saat membuat fitur baru untuk memastikan konsistensi.

### 📋 File Structure

- [ ] Buat `app/schemas/feature_name_schema.py`
- [ ] Buat `app/repositories/feature_name_repository.py`
- [ ] Buat `app/services/feature_name_service.py`
- [ ] Buat `app/controllers/feature_name_controller.py`
- [ ] Buat `app/routes/feature_name_routes.py`

### 📋 Schema Layer

- [ ] Definisikan response schema dengan `dump_only` untuk ID
- [ ] Definisikan create schema dengan `required` fields
- [ ] Definisikan list schema dengan `many=True`
- [ ] Gunakan validation yang sesuai (`validate.Length()`, dll)
- [ ] Buat instances untuk reuse (`feature_name_schema`, dll)

### 📋 Repository Layer

- [ ] Implement `get_all()` dengan pagination dan search
- [ ] Implement `get_by_id()`
- [ ] Implement `create()`
- [ ] Implement `update()`
- [ ] Implement `delete()`
- [ ] Handle database errors dengan `raise ValueError()`

### 📋 Service Layer

- [ ] Validate input parameters (page >= 1, per_page 1-100)
- [ ] Format pagination metadata di response
- [ ] Validate business logic
- [ ] Raise `ValueError()` untuk error conditions
- [ ] Validate existence sebelum update/delete

### 📋 Controller Layer - ⭐ PENTING

- [ ] **Import dari `app.utils.api_response`**: `from app.utils.api_response import success_response, error_response`
- [ ] Gunakan **`success_response()`** untuk success (status 200 atau 201)
- [ ] Gunakan **`error_response()`** untuk error (status 400, 404, 409, 500)
- [ ] Validate request.get_json() not empty
- [ ] Deserialize input dengan schema
- [ ] Serialize output dengan schema
- [ ] Handle `ValidationError` dari marshmallow
- [ ] Handle `ValueError` dari service
- [ ] Handle generic `Exception` dengan status 500
- [ ] Status code yang **BENAR**:
  - GET/PUT/DELETE success → 200
  - POST success → 201
  - Validation error → 400
  - Not found → 404
  - Conflict → 409
  - Server error → 500

### 📋 Routes Layer

- [ ] Definisikan blueprint dengan `url_prefix='/api/...'`
- [ ] Register route GET (list)
- [ ] Register route POST (create)
- [ ] Register route GET /<id> (detail)
- [ ] Register route PUT /<id> (update)
- [ ] Register route DELETE /<id> (delete)
- [ ] Semua route mengarah ke controller method

### 📋 Integration

- [ ] Register blueprint di `app/__init__.py` dalam `register_blueprints()`
- [ ] Test semua endpoint dengan cURL atau Postman
- [ ] Verify response format (success, message, data, timestamp)
- [ ] Verify HTTP status codes
- [ ] Verify pagination metadata (jika ada)

### 📋 Response Consistency

- [ ] Semua success response format **sama**
- [ ] Semua error response format **sama**
- [ ] **Timestamp** selalu ada dan ISO format (UTC)
- [ ] **Data field** hanya ada saat ada payload
- [ ] **Errors field** hanya ada saat ada detail error
- [ ] **Message** deskriptif dan konsisten dengan business logic

---

## ✅ Checklist Code Review

Sebelum push ke repository, review code dengan checklist ini:

### 📋 Architecture

- [ ] Apakah 5-layer architecture ter-implement dengan benar?
- [ ] Apakah business logic di Service, bukan Controller?
- [ ] Apakah database queries di Repository, bukan Service?
- [ ] Apakah HTTP handling di Controller, bukan Service?
- [ ] Apakah validation di Schema dan Service?

### 📋 API Response

- [ ] Apakah semua controller mengimport dari `api_response.py`?
- [ ] Apakah semua success return `success_response()`?
- [ ] Apakah semua error return `error_response()`?
- [ ] Apakah status codes benar (200, 201, 400, 404, 409, 500)?
- [ ] Apakah response format konsisten?

### 📋 Error Handling

- [ ] Apakah ada try-except di controller?
- [ ] Apakah `ValidationError` di-handle?
- [ ] Apakah `ValueError` di-handle?
- [ ] Apakah generic `Exception` di-handle dengan status 500?
- [ ] Apakah error message deskriptif?

### 📋 Code Quality

- [ ] Apakah code bersih dan readable?
- [ ] Apakah tidak ada duplicate code?
- [ ] Apakah variable names jelas dan konsisten?
- [ ] Apakah ada docstring untuk methods?
- [ ] Apakah tidak ada hardcoded values?

### 📋 Testing

- [ ] Apakah semua endpoint sudah ditest?
- [ ] Apakah success cases tested?
- [ ] Apakah error cases tested?
- [ ] Apakah response format benar?
- [ ] Apakah pagination metadata benar?

---

## 🎯 Tips & Best Practices

### 💡 Controller Tips

```python
# ✅ DO: Handle exceptions properly
@staticmethod
def get_detail(id):
    try:
        record = Service.get_by_id(id)
        record_data = schema.dump(record)
        return success_response(
            message="Record retrieved",
            data={'record': record_data},
            status_code=200
        )
    except ValueError as e:
        return error_response(message=str(e), status_code=404)
    except Exception as e:
        return error_response(message="Server error", errors=str(e), status_code=500)

# ❌ DON'T: Use jsonify directly
from flask import jsonify
return jsonify({'success': True, 'data': record})  # WRONG!

# ❌ DON'T: Forget to import api_response
from app.controllers.merek_controller import ...  # WRONG if no import!
```

### 💡 Service Tips

```python
# ✅ DO: Validate in service
@staticmethod
def create(name):
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    return Repository.create(name.strip())

# ❌ DON'T: Put validation logic in controller
# Validation should be in Service, not Controller
```

### 💡 Repository Tips

```python
# ✅ DO: Handle database operations only
@staticmethod
def get_all(page=1, per_page=10):
    query = Model.query
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return paginated.items, paginated.total, paginated.pages

# ❌ DON'T: Put business logic in repository
# Pagination metadata should be in Service, not Repository
```

### 💡 Response Tips

```python
# ✅ DO: Use proper status codes
return success_response(message="Created", data={...}, status_code=201)  # For POST
return success_response(message="Updated", data={...}, status_code=200)  # For PUT
return error_response(message="Not found", status_code=404)  # For 404

# ❌ DON'T: Use wrong status codes
return success_response(message="Created", data={...}, status_code=200)  # WRONG!
return error_response(message="Not found", status_code=400)  # WRONG!
```

---

## 📚 File References

- **Response utilities:** `app/utils/api_response.py`
- **Example controller:** `app/controllers/merek_controller.py`
- **Example service:** `app/services/merek_service.py`
- **Example repository:** `app/repositories/merek_repository.py`
- **Architecture documentation:** `ARCHITECTURE.md`

---

## 🚀 Kesimpulan

Dengan mengikuti panduan ini, Anda akan membangun API yang:

✅ **Konsisten** - Semua response format sama  
✅ **Professional** - Clean dan terstruktur dengan baik  
✅ **Maintainable** - Mudah dipahami dan di-update  
✅ **Scalable** - Template dapat digunakan untuk semua fitur  
✅ **Robust** - Error handling yang proper  
✅ **Client-friendly** - Response format yang jelas dan predictable

**Gunakan panduan ini untuk semua fitur baru yang akan dibuat!** 🎯
