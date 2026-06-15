from app.repositories.model_kendaraan_repository import ModelKendaraanRepository
from app.repositories.merek_repository import MerekRepository


class ModelKendaraanService:
    @staticmethod
    def get_all_model_kendaraans(page=1, per_page=10, search=None):
        # 1. Validasi parameter
        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")
        # 2. pagination
        items, total, total_pages = ModelKendaraanRepository.get_all(
            page=page, per_page=per_page, search=search
        )

        return {
            "data": items,
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
    def get_model_kendaraan_by_id(id_model):
        model = ModelKendaraanRepository.get_by_id(id_model=id_model)
        if not model:
            raise ValueError(f"Model Kendaraan dengan ID {id_model} tidak ditemukan")

        return model

    @staticmethod
    def get_model_kendaraan_by_merek(id_merek, search=None):
        merek = MerekRepository.get_by_id(id_merek=id_merek)

        if not merek:
            raise ValueError(f"Merek dengan Id {id_merek} tidak ditemukan")

        model = ModelKendaraanRepository.get_by_merek(id_merek, search=search)
        
        return model

    @staticmethod
    def create_model_kendaraan(id_merek, nama_model):
        # Validasi Input
        if not nama_model or not nama_model.strip():
            raise ValueError("Nama Model tidak boleh kosong")

        nama_model = nama_model.strip()

        return ModelKendaraanRepository.create(id_merek, nama_model)

    @staticmethod
    def update_model_kendaraan(id_model, id_merek, nama_model):
        if nama_model is not None:
            if not nama_model or not nama_model.strip():
                raise ValueError("Nama Model tidak boleh kosong")
            nama_model = nama_model.strip()

        return ModelKendaraanRepository.update(
            id_model=id_model,
            id_merek=id_merek,
            nama_model=nama_model,
        )

    @staticmethod
    def delete_model_kendaraan(id_model):
        return ModelKendaraanRepository.delete(id_model)
