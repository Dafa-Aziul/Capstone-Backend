# Dokumentasi API Prediksi Harga Mobil Bekas

## Base URL & Autentikasi

- **Base URL API**: Sesuai dengan konfigurasi environment Anda (contoh: `http://localhost:5000`)
- **Autentikasi**: Sebagian besar endpoint membutuhkan autentikasi berupa **Cookie (JWT)**. Cookie akan otomatis diset saat memanggil endpoint `/auth/login`.

---

### 1. Authentication (`/auth`)

#### a. Register

Endpoint untuk mendaftarkan user baru ke dalam sistem.

- **URL**: `/auth/register`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "nama": "<nama_lengkap>",
    "email": "<email_user>",
    "password": "<password_min_6_karakter>"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Registrasi berhasil",
    "data": {
      "user": {
        "id_user": 1,
        "nama": "<nama_lengkap>",
        "email": "<email_user>",
        "role": "user",
        "is_active": true,
        "created_at": "<timestamp>"
      }
    },
    "timestamp": "<timestamp>"
  }
  ```

#### b. Login

Endpoint untuk login. Mengembalikan data user dan secara otomatis mengatur `access_token` dan `refresh_token` di dalam HTTP-Only Cookie.

- **URL**: `/auth/login`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "email": "<email_user>",
    "password": "<password>"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Login berhasil",
    "data": {
      "user": {
        "id_user": 1,
        "nama": "<nama_lengkap>",
        "email": "<email_user>",
        "role": "<role>",
        "is_active": true,
        "created_at": "<timestamp>"
      }
    },
    "timestamp": "<timestamp>"
  }
  ```

#### c. Refresh Token

Endpoint untuk memperbarui Access Token jika sudah kedaluwarsa (menggunakan Refresh Token di cookie).

- **URL**: `/auth/refresh`
- **Method**: `POST`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Token berhasil diperbarui",
    "timestamp": "<timestamp>"
  }
  ```

#### d. Logout

Endpoint untuk menghapus sesi login (menghapus cookie).

- **URL**: `/auth/logout`
- **Method**: `POST`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Logout berhasil",
    "timestamp": "<timestamp>"
  }
  ```

#### e. Get Current User

Endpoint untuk mendapatkan informasi user yang sedang login berdasarkan token di cookie.

- **URL**: `/auth/me`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Data user berhasil diambil",
    "data": {
      "id_user": 1,
      "nama": "<nama_lengkap>",
      "email": "<email_user>",
      "role": "<role>",
      "is_active": true,
      "created_at": "<timestamp>"
    },
    "timestamp": "<timestamp>"
  }
  ```

---

### 2. Merek Kendaraan (`/merek`)

#### a. Get All Merek

Endpoint untuk mendapatkan daftar semua merek kendaraan.

- **URL**: `/merek`
- **Method**: `GET`
- **Parameter Query (opsional)**:
  - `page`: Nomor halaman (default: 1)
  - `per_page`: Jumlah data per halaman (default: 10)
  - `search`: Kata kunci pencarian nama merek
- **Response**:

  ```json
  {
    "success": true,
    "message": "List merek berhasil diambil",
    "timestamp": "2026-06-14T16:05:18.049186+00:00",
    "data": [
      {
        "id_merek": 1,
        "nama_merek": "Audi"
      },
      {
        "id_merek": 2,
        "nama_merek": "Bmw"
      },
      {
        "id_merek": 3,
        "nama_merek": "Ford"
      },
      {
        "id_merek": 4,
        "nama_merek": "Hyundi"
      },
      {
        "id_merek": 5,
        "nama_merek": "Merc"
      },
      {
        "id_merek": 6,
        "nama_merek": "Skoda"
      },
      {
        "id_merek": 11,
        "nama_merek": "test Model update"
      },
      {
        "id_merek": 7,
        "nama_merek": "Toyota"
      },
      {
        "id_merek": 8,
        "nama_merek": "Vauxhall"
      },
      {
        "id_merek": 9,
        "nama_merek": "Vw"
      }
    ],
    "meta": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 10,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
  ```

#### b. Get Detail Merek

- **URL**: `/merek/<id_merek>`
- **Method**: `GET`
- **Response** :

  ```json
  {
    "success": true,
    "message": "Detail merek berhasil diambil",
    "timestamp": "2026-06-14T16:06:12.537952+00:00",
    "data": {
      "id_merek": 1,
      "nama_merek": "Audi"
    }
  }
  ```

#### c. Create Merek

- **URL**: `/merek`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "nama_merek": "Honda"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Merek berhasil dibuat",
    "timestamp": "2026-06-14T16:07:41.417846+00:00",
    "data": {
      "id_merek": 13,
      "nama_merek": "test"
    }
  }
  ```

#### d. Update Merek

- **URL**: `/merek/<id_merek>`
- **Method**: `PUT`
- **Request Body**:

  ```json
  {
    "nama_merek": "Honda Baru"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Merek berhasil diupdate",
    "timestamp": "2026-06-14T16:08:48.252769+00:00",
    "data": {
      "id_merek": 13,
      "nama_merek": "test mer"
    }
  }
  ```

#### e. Delete Merek

- **URL**: `/merek/<id_merek>`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Merek berhasil dihapus",
    "timestamp": "2026-06-14T16:09:44.252769+00:00"
  }
  ```

---

### 3. Model Kendaraan (`/model-kendaraan`)

#### a. Get All Model

- **URL**: `/model-kendaraan`
- **Method**: `GET`
- **Parameter Query**:
  - `page`: Nomor halaman (default: 1)
  - `per_page`: Jumlah data per halaman (default: 10)
  - `search`: Kata kunci pencarian nama model kendaraan
- **Response**: Mengembalikan list model kendaraan beserta data paginasi.

  ```json
  {
    "success": true,
    "message": "List model kendaraan berhasil diambil",
    "timestamp": "2026-06-14T16:10:57.928300+00:00",
    "data": [
      {
        "id_model": 1,
        "id_merek": 2,
        "nama_model": "1 Series"
      },
      {
        "id_model": 2,
        "id_merek": 5,
        "nama_model": "180"
      },
      {
        "id_model": 3,
        "id_merek": 2,
        "nama_model": "2 Series"
      },
      {
        "id_model": 4,
        "id_merek": 5,
        "nama_model": "200"
      },
      {
        "id_model": 5,
        "id_merek": 5,
        "nama_model": "220"
      },
      {
        "id_model": 6,
        "id_merek": 5,
        "nama_model": "230"
      },
      {
        "id_model": 7,
        "id_merek": 2,
        "nama_model": "3 Series"
      },
      {
        "id_model": 8,
        "id_merek": 2,
        "nama_model": "4 Series"
      },
      {
        "id_model": 9,
        "id_merek": 2,
        "nama_model": "5 Series"
      },
      {
        "id_model": 10,
        "id_merek": 2,
        "nama_model": "6 Series"
      }
    ],
    "meta": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 195,
      "total_pages": 20,
      "has_next": true,
      "has_prev": false
    }
  }
  ```

#### b. Get Model by Merek

Mendapatkan daftar model kendaraan spesifik berdasarkan ID Merek.

- **URL**: `/model-kendaraan/<id_merek>/merek`
- **Method**: `GET`
- **Parameter Query (opsional)**:
  - `search` : Kata kunci pencarian nama model kendaraan
- **Response**:

  ```json
  {
    "success": true,
    "message": "List model kendaraan berdasarkan merek berhasil diambil",
    "timestamp": "2026-06-14T16:11:29.258081+00:00",
    "data": [
      {
        "id_model": 1,
        "id_merek": 2,
        "nama_model": "1 Series"
      },
      {
        "id_model": 3,
        "id_merek": 2,
        "nama_model": "2 Series"
      },
      {
        "id_model": 7,
        "id_merek": 2,
        "nama_model": "3 Series"
      },
      ...
    ]
  }
  ```

#### c. Get Detail Model

- **URL**: `/model-kendaraan/<id_model>`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Detail model kendaraan berhasil diambil",
    "timestamp": "2026-06-14T16:11:29.258081+00:00",
    "data": {
      "id_model": 1,
      "id_merek": 2,
      "nama_model": "1 Series"
    }
  }
  ```

#### d. Create Model

- **URL**: `/model-kendaraan`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "id_merek": 1,
    "nama_model": "Innova"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Model kendaraan berhasil dibuat",
    "timestamp": "2026-06-14T16:12:11.417846+00:00",
    "data": {
      "id_model": 196,
      "id_merek": 1,
      "nama_model": "Innova"
    }
  }
  ```

#### e. Update Model

- **URL**: `/model-kendaraan/<id_model>`
- **Method**: `PUT`
- **Request Body**:

  ```json
  {
    "id_merek": 1,
    "nama_model": "Innova Reborn"
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Model kendaraan berhasil diupdate",
    "timestamp": "2026-06-14T16:13:48.252769+00:00",
    "data": {
      "id_model": 196,
      "id_merek": 1,
      "nama_model": "Innova Reborn"
    }
  }
  ```

#### f. Delete Model

- **URL**: `/model-kendaraan/<id_model>`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Model kendaraan berhasil dihapus",
    "timestamp": "2026-06-14T16:14:44.252769+00:00"
  }
  ```

---

### 4. Machine Learning Models (`/ml-model`) - _Admin Only_

#### a. Get All Models

- **URL**: `/ml-model`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "List model ML berhasil diambil",
    "timestamp": "<timestamp>",
    "data": [
      {
        "id_ml_model": 5,
        "uploaded_by": 1,
        "file_path": "uploads/models/v2.0_ebe84898_model_gradient_boosting.joblib",
        "versi": "v2.0",
        "r_squared": 0.9492,
        "mae": 1394.22,
        "is_current": false,
        "uploaded_at": "<timestamp>"
      },
      {
        "id_ml_model": 4,
        "uploaded_by": 1,
        "file_path": "uploads/models/v1.5_11083233_model_gradient_boosting.joblib",
        "versi": "v1.5",
        "r_squared": 0.9492,
        "mae": 1394.22,
        "is_current": true,
        "uploaded_at": "<timestamp>"
      },
      ...
    ],
    "meta": {
        "current_page": 1,
        "per_page": 10,
        "total_items": 3,
        "total_pages": 1,
        "has_next": false,
        "has_prev": false
    }
  }
  ```

#### b. Get Active Model

Mengambil informasi model ML yang saat ini sedang aktif digunakan sistem.

- **URL**: `/ml-model/active`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Data model aktif berhasil didapatkan",
    "timestamp": "2026-06-14T14:23:06.143471+00:00",
    "data": {
      "id_ml_model": 3,
      "uploaded_by": 1,
      "file_path": "uploads/models/v1.0_773bc896_model_gradient_boosting.joblib",
      "versi": "v1.0",
      "r_squared": 0.9492,
      "mae": 1394.22,
      "is_current": true,
      "uploaded_at": "2026-06-09T10:25:00",
      "total_models": 2
    }
  }
  ```

#### c. Get Model Detail

- **URL**: `/ml-model/<id_ml_model>`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Detail model ML berhasil diambil",
    "timestamp": "2026-06-14T16:18:56.849035+00:00",
    "data": {
      "id_ml_model": 3,
      "uploaded_by": 1,
      "file_path": "uploads/models/v1.0_773bc896_model_gradient_boosting.joblib",
      "versi": "v1.0",
      "r_squared": 0.9492,
      "mae": 1394.22,
      "is_current": false,
      "uploaded_at": "2026-06-09T10:25:00"
    }
  }
  ```

#### d. Upload New Model

Endpoint untuk mengunggah model ML baru. Wajib menggunakan `multipart/form-data`.

- **URL**: `/ml-model`
- **Method**: `POST`
- **Form Data**:
  - `file`: (File .joblib)
  - `versi`: "v1.2"
  - `r_squared`: 0.92
  - `mae`: 1150.0
- **Response**:

  ```json
  {
    "success": true,
    "message": "Model ML berhasil diunggah dan disimpan",
    "timestamp": "2026-06-14T14:23:22.793167+00:00",
    "data": {
      "ml_model": {
        "id_ml_model": 5,
        "uploaded_by": 1,
        "file_path": "uploads/models/v2.0_ebe84898_model_gradient_boosting.joblib",
        "versi": "v2.0",
        "r_squared": 0.9492,
        "mae": 1394.22,
        "is_current": true,
        "uploaded_at": "2026-06-14T14:23:23"
      }
    }
  }
  ```

#### e. Set Model Active

Mengubah status model ML tertentu menjadi model utama (aktif).

- **URL**: `/ml-model/<id_ml_model>/active`
- **Method**: `PATCH`
- Response:

  ```json
  {
    "success": true,
    "message": "Model ML berhasil diaktifkan",
    "timestamp": "2026-06-14T16:23:54.098997+00:00",
    "data": {
      "id_ml_model": 4,
      "uploaded_by": 1,
      "file_path": "uploads/models/v1.5_11083233_model_gradient_boosting.joblib",
      "versi": "v1.5",
      "r_squared": 0.9492,
      "mae": 1394.22,
      "is_current": true,
      "uploaded_at": "2026-06-10T01:26:19"
    }
  }
  ```

#### f. Delete Model ML tertentu dari sistem

- **URL**: `/ml-model/<id_ml_model>`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Model ML berhasil dihapus",
    "timestamp": "2026-06-14T16:24:30.123456+00:00"
  }
  ```

---

### 5. Prediksi Harga Mobil (`/predict`)

#### a. Semua Riwayat Prediksi (Admin)

Endpoint untuk mendapatkan semua riwayat prediksi yang pernah dilakukan oleh semua user (Admin Only).

- **URL**: `/predict`
- **Method**: `GET`
- **Parameter Query**:
  - `page`: Nomor halaman (default: 1)
  - `per_page`: Jumlah data per halaman (default: 10)
  - `search`: Kata kunci pencarian (berdasarkan nama merek, model, atau email user)
- **Response**: Mengembalikan list riwayat prediksi beserta data paginasi.

  ```json
  {
    "success": true,
    "message": "List Predict berhasil diambil",
    "timestamp": "2026-06-14T16:30:28.413776+00:00",
    "data": [
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-09T10:36:51"
      },
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-14T16:27:40"
      }
    ],
    "meta": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 2,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
  ```

#### b. Statistik Riwayat Prediksi (Admin)

Endpoint untuk mendapatkan statistik riwayat prediksi, seperti jumlah total prediksi per model ML, rata-rata harga prediksi, dan distribusi prediksi berdasarkan merek/model.

- **URL**: `/predict/stat/admin`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Statistik prediksi admin berhasil diambil",
    "timestamp": "2026-06-14T14:29:21.854147+00:00",
    "data": {
      "total_predict": 1,
      "total_predict_today": 0,
      "total_active_users": 2,
      "model_active_version": "v1.5"
    }
  }
  ```

#### c. Chart Riwayat Prediksi (Admin)

Endpoint untuk mendapatkan data chart riwayat prediksi 1 minggu kebelakang, yang dapat digunakan untuk menampilkan grafik tren prediksi di dashboard admin.

- **URL**: `/predict/chart/admin`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Data Chart per minggu berhasil diambil",
    "data": [
      { "date": "2026-06-08", "value": 5 },
      { "date": "2026-06-09", "value": 10 },
      { "date": "2026-06-10", "value": 7 },
      { "date": "2026-06-11", "value": 3 },
      { "date": "2026-06-12", "value": 8 },
      { "date": "2026-06-13", "value": 2 },
      { "date": "2026-06-14", "value": 4 }
    ],
    "timestamp": "<timestamp>"
  }
  ```

#### d. Last Activity (Admin)

Endpoint untuk mendapatkan daftar aktivitas prediksi terbaru yang dilakukan oleh semua user, termasuk informasi user, mobil yang diprediksi, harga prediksi, dan waktu prediksi.

  - **URL**: `/predict/latest-activity/admin?jumlah=5`
- query parameter `jumlah` digunakan untuk menentukan berapa banyak aktivitas terbaru yang ingin ditampilkan (default: 5).
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Aktivitas terbaru berhasil diambil",
    "timestamp": "2026-06-14T16:41:45.356932+00:00",
    "data": [
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-14T16:27:40"
      },
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-09T10:36:51"
      }
    ]
  }
  ```

#### e. Riwayat by User(User)

Endpoint untuk mendapatkan daftar riwayat prediksi yang pernah dilakukan oleh user yang sedang aktif, termasuk informasi mobil yang diprediksi, harga prediksi, dan waktu prediksi.

- **URL**: `/predict/by-user`
- Query Parameter:
  - `page`: Nomor halaman (default: 1)
  - `per_page`: Jumlah data per halaman (default: 10)
  - `search`: Kata kunci pencarian berdasarkan nama merek atau model kendaraan
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "List Predict by user berhasil diambil",
    "timestamp": "2026-06-14T16:45:13.641539+00:00",
    "data": [
      {
        "id_riwayat": 4,
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "created_at": "2026-06-14T16:27:40"
      },
      {
        "id_riwayat": 1,
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "created_at": "2026-06-09T10:36:51"
      }
    ],
    "meta": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 2,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
  ```

#### f. Statistik Riwayat Prediksi by user (User)

Endpoint untuk mendapatkan statistik riwayat prediksi milik user yang sedang aktif, seperti jumlah total prediksi yang pernah dilakukan, harga prediksi terakhir, dan informasi model ML yang digunakan.

- **URL**: `/predict/stat/user`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Statistik prediksi user berhasil diambil",
    "timestamp": "2026-06-14T16:36:13.574765+00:00",
    "data": {
      "total_predict": 12,
      "avg_predict_price": 17500.25,
      "total_predict_this_month": 4,
      "total_predict_today": 1
    }
  }
  ```

#### g. Last Activity (User)

Endpoint untuk mendapatkan daftar aktivitas prediksi terbaru yang dilakukan oleh user yang sedang aktif, termasuk informasi mobil yang diprediksi, harga prediksi, dan waktu prediksi.

- **URL**: `/predict/latest-activity/user?jumlah=5`
- query parameter `jumlah` digunakan untuk menentukan berapa banyak aktivitas terbaru yang ingin ditampilkan (default: 5).
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Aktivitas terbaru user berhasil diambil",
    "timestamp": "2026-06-14T16:47:22.621879+00:00",
    "data": [
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-14T16:27:40"
      },
      {
        "nama_user": "Admin Test",
        "email": "admin@test.com",
        "mobil": "Bmw 1 Series",
        "harga_prediksi": 18025.01,
        "ml_model": "v1.0",
        "created_at": "2026-06-09T10:36:51"
      }
    ]
  }
  ```

#### h. Lakukan Prediksi (Tanpa Simpan)

Endpoint untuk memprediksi harga tanpa menyimpannya ke database riwayat.

- **URL**: `/predict`
- **Method**: `POST`
- **Request Body**:

  ```json
  {
    "id_model": 1,
    "tahun": 2018,
    "mileage": 50000,
    "transmisi": "Automatic",
    "bahan_bakar": "Petrol",
    "pajak": 150,
    "mpg": 45.5,
    "kapasitas_mesin": 1.5
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Prediksi harga mobil berhasil dibuat.",
    "timestamp": "2026-06-14T14:32:11.338917+00:00",
    "data": {
      "prediction": 18025.0054014068,
      "model_info": {
        "id_ml_model": 4,
        "versi": "v1.5",
        "r_squared": 0.9492,
        "mae": 1394.22
      },
      "input_data": {
        "merk": "Bmw",
        "model": "1 Series",
        "year": 2019,
        "mileage": 25000,
        "transmission": "Automatic",
        "fuelType": "Petrol",
        "tax": 145,
        "mpg": 55.4,
        "engineSize": 1.5
      },
      "shap_explanation": {
        "base_value": 16788.08311383886,
        "feature_contributions": {
          "merk": 1396.8518773835212,
          "model": -1390.2389195916794,
          "transmission": 1056.3022332842775,
          "fuelType": -235.9164188275399,
          "year": 3397.33710109391,
          "mileage": -874.5979186256307,
          "tax": 37.10211308386449,
          "mpg": -836.3783862083765,
          "engineSize": -1313.5393940244396
        }
      }
    }
  }
  ```

#### i. Simpan Prediksi

- **URL**: `/predict/save`
- **Method**: `POST`
- **Request Body**: Gabungan payload poin (a) ditambah field `id_ml_model`, `harga_prediksi`, dan `shap_summary`.

  ```json
  {
    "id_model": 1,
    "tahun": 2019,
    "mileage": 25000,
    "transmisi": "Automatic",
    "bahan_bakar": "Petrol",
    "pajak": 145,
    "mpg": 55.4,
    "kapasitas_mesin": 1.5,
    "id_ml_model": 3,
    "harga_prediksi": 18025.0054014068,
    "shap_summary": {
      "base_value": 16788.08311383886,
      "feature_contributions": {
        "merk": 1396.8518773835212,
        "model": -1390.2389195916794,
        "transmission": 1056.3022332842775,
        "fuelType": -235.9164188275399,
        "year": 3397.33710109391,
        "mileage": -874.5979186256307,
        "tax": 37.10211308386449,
        "mpg": -836.3783862083765,
        "engineSize": -1313.5393940244396
      }
    }
  }
  ```

- **Response**:

  ```json
  {
    "success": true,
    "message": "Riwayat prediksi berhasil disimpan.",
    "timestamp": "2026-06-14T14:32:35.981263+00:00"
  }
  ```

#### j. Detail Riwayat Prediksi

Endpoint untuk mendapatkan detail riwayat prediksi tertentu berdasarkan ID riwayat, termasuk informasi input, hasil prediksi, model yang digunakan, dan penjelasan SHAP.

- **URL**: `/predict/<id_riwayat>`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Detail Riwayat berhasil diambil",
    "timestamp": "2026-06-14T16:48:56.646757+00:00",
    "data": {
      "id_riwayat": 1,
      "created_at": "2026-06-09T10:36:51",
      "prediction": 18025.01,
      "model_info": {
        "id_ml_model": 3,
        "versi": "v1.0",
        "r_squared": 0.9492,
        "mae": 1394.22
      },
      "input_data": {
        "merk": "Bmw",
        "model": "1 Series",
        "year": 2019,
        "mileage": 25000,
        "transmission": "Automatic",
        "fuelType": "Petrol",
        "tax": 145,
        "mpg": 55.4,
        "engineSize": 1.5
      },
      "shap_explanation": {
        "base_value": 16788.08311383886,
        "feature_contributions": {
          "merk": 1396.8518773835212,
          "model": -1390.2389195916794,
          "transmission": 1056.3022332842775,
          "fuelType": -235.9164188275399,
          "year": 3397.33710109391,
          "mileage": -874.5979186256307,
          "tax": 37.10211308386449,
          "mpg": -836.3783862083765,
          "engineSize": -1313.5393940244396
        }
      }
    }
  }
  ```

#### k. Hapus Riwayat Prediksi

Endpoint untuk menghapus riwayat prediksi tertentu berdasarkan ID riwayat.

- **URL**: `/predict/<id_riwayat>`
- **Method**: `DELETE`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Riwayat prediksi berhasil dihapus.",
    "timestamp": "2026-06-14T16:45:00.123456+00:00"
  }
  ```

---

### 6. Dashboard Analytics (`/dashboard`)

Menyediakan data ringkasan untuk grafik dan statistik pada halaman depan aplikasi.

#### a. Stat Admin

- **URL**: `/dashboard/stat/admin`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Statistik Dashboard Admin berhasil diambil",
    "timestamp": "2026-06-14T14:40:47.531651+00:00",
    "data": {
      "total_predict": 1,
      "total_user": 2,
      "total_active": 2,
      "model_active_version": "v1.5"
    }
  }
  ```

#### b. Stat User

- **URL**: `/dashboard/stat/user`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Statistik Dashboard User berhasil diambil",
    "timestamp": "2026-06-14T16:51:23.342912+00:00",
    "data": {
      "total_predict": 2,
      "last_predict": "18025.01",
      "acc": 0.9492,
      "model_active_version": "v1.5"
    }
  }
  ```

#### c. Chart Dashboard Admin

- **URL**: `/dashboard/chart/admin`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Data Chart admin perbulan berhasil diambil",
    "timestamp": "2026-06-14T14:42:33.472576+00:00",
    "data": [
      {
        "date": "2026-02",
        "value": 0
      },
      {
        "date": "2026-03",
        "value": 0
      },
      {
        "date": "2026-04",
        "value": 0
      },
      {
        "date": "2026-05",
        "value": 0
      },
      {
        "date": "2026-06",
        "value": 1
      }
    ]
  }
  ```

### d. Chart Dashboard User

- **URL**: `/dashboard/chart/user`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Data Chart user perbulan berhasil diambil",
    "timestamp": "2026-06-14T16:53:12.123456+00:00",
    "data": [
      {
        "date": "2026-02",
        "value": 0
      },
      {
        "date": "2026-03",
        "value": 0
      },
      {
        "date": "2026-04",
        "value": 0
      },
      {
        "date": "2026-05",
        "value": 1
      },
      {
        "date": "2026-06",
        "value": 1
      }
    ]
  }
  ```

### 7. Manajemen User (`/user`) - _Admin Only_

#### a. Get All User

- **URL**: `/user`
- **Method**: `GET`
- **Parameter**:
  - `page`: Nomor halaman (default: 1)
  - `per_page`: Jumlah data per halaman (default: 10)
  - `search`: Kata kunci pencarian berdasarkan nama atau email user
- **Response**: Mengembalikan list user beserta data paginasi.

  ```json
  {
    "success": true,
    "message": "List user berhasil diambil",
    "timestamp": "2026-06-14T14:28:05.398890+00:00",
    "data": [
      {
        "id_user": 1,
        "nama": "Admin Test",
        "email": "admin@test.com",
        "is_active": true,
        "created_at": "2026-06-09T08:22:07"
      },
      {
        "id_user": 2,
        "nama": "User test",
        "email": "usertest@gmail.com",
        "is_active": true,
        "created_at": "2026-06-11T10:36:46"
      }
    ],
    "meta": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 2,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
  ```

#### b. Set Status User (Aktif/Non-Aktif)

Endpoint untuk memblokir atau mengaktifkan kembali akun user.

- **URL**: `/user/<id_user>/set-status`
- **Method**: `PATCH`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Status User <nama_user> berhasil diubah menjadi Tidak Aktif",
    "timestamp": "<timestamp>"
  }
  ```

#### c. Get User Stats

- **URL**: `/user/stats`
- **Method**: `GET`
- **Response**:

  ```json
  {
    "success": true,
    "message": "Statistik user berhasil diambil",
    "timestamp": "2026-06-14T08:25:13.040301+00:00",
    "data": {
      "total_users": 2,
      "total_active_users": 2,
      "total_inactive_users": 0
    }
  }
  ```
