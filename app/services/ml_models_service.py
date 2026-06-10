import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from app.repositories.ml_models_repository import MlModelsRepository


class MlModelsService:
    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        # 1. Validasi parameter paginasi
        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")

        # 2. Get data dari repository
        items, total, total_pages = MlModelsRepository.get_all(
            page=page, per_page=per_page, search=search
        )
        return {
            "items": items,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }

    @staticmethod
    def get_by_id(id_ml_model):
        model = MlModelsRepository.get_by_id(id_ml_model)
        if not model:
            raise ValueError(f"Model ML dengan ID {id_ml_model} tidak ditemukan")

        return model

    @staticmethod
    def create(uploaded_by, file, versi, r_squared, mae):
        # 1. validasi input
        if not file or not file.filename:
            raise ValueError("File model tidak boleh kosong")

        # 2. Validasi ekstensi file (.joblib)
        if not file.filename.lower().endswith(".joblib"):
            raise ValueError(
                "Ekstensi file tidak diizinkan. Hanya menerima file .joblib"
            )

        if not versi or not versi.strip():
            raise ValueError("Versi tidak boleh kosong")
        if r_squared is None or mae is None:
            raise ValueError("Nilai metrik (r_squared dan mae) harus disediakan")

        # 3. Pastikan nama file aman dan hindari karakter aneh
        filename = secure_filename(file.filename)

        # 4. Bersihkan awalan 'v' jika user sudah menginputkannya (mencegah vv1.0)
        clean_versi = versi.strip()
        if clean_versi.lower().startswith("v"):
            clean_versi = clean_versi[1:]

        # 5. Buat UUID untuk nama file
        unique_filename = f"v{clean_versi}_{uuid.uuid4().hex[:8]}_{filename}"

        # 6. Tentukan direktori upload
        project_root = os.path.dirname(current_app.root_path)
        upload_folder = os.path.join(project_root, "uploads", "models")
        os.makedirs(upload_folder, exist_ok=True)

        # 7. Path absolut untuk menyimpan file secara fisik
        file_abs_path = os.path.join(upload_folder, unique_filename)
        db_file_path = f"uploads/models/{unique_filename}"

        try:
            # 8. Simpan file kedalam disk
            file.save(file_abs_path)

            # 9. create ml models
            ml_model = MlModelsRepository.create(
                uploaded_by, db_file_path, versi.strip(), r_squared, mae
            )
            return ml_model
        except Exception as e:
            # rollback jika data gagal
            if os.path.exists(file_abs_path):
                os.remove(file_abs_path)
            raise e

    @staticmethod
    def set_active(id_ml_model):
        return MlModelsRepository.set_active(id_ml_model)

    @staticmethod
    def delete(id_ml_model):
        # 1.Hapus dari database terlebih dahulu
        deleted_model = MlModelsRepository.delete(id_ml_model)

        # 2. Jika berhasil, hapus file fisik model ML
        if deleted_model and deleted_model.file_path:
            # 3. file_path formatnya: "uploads/models/filename.joblib"
            filename = deleted_model.file_path.split("/")[-1]
            project_root = os.path.dirname(current_app.root_path)
            file_abs_path = os.path.join(project_root, "uploads", "models", filename)
            if os.path.exists(file_abs_path):
                os.remove(file_abs_path)
            else:
                raise ValueError("Model tidak ditemukan")
        return True
