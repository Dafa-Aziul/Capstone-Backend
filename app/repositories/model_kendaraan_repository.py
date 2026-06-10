from app.models.model_kendaraan_model import ModelKendaraan
from app.repositories.merek_repository import MerekRepository
from app.extensions import db


class ModelKendaraanRepository:

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        query = ModelKendaraan.query

        # 1. Filter berdasarkan search keyword
        if search:
            query = query.filter(ModelKendaraan.nama_model.ilike(f"%{search}%"))

        # 2. Sorting by nama_model
        query = query.order_by(ModelKendaraan.nama_model.asc())

        # 3. Pagination
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated.items, paginated.total, paginated.pages

    @staticmethod
    def get_by_id(id_model):
        return ModelKendaraan.query.get(id_model)

    @staticmethod
    def get_by_merek(id_merek, search=None):
        query = ModelKendaraan.query.filter_by(id_merek=id_merek)

        if search:
            query = query.filter(ModelKendaraan.nama_model.ilike(f"%{search}%"))

        return query.order_by(ModelKendaraan.nama_model.asc()).all()

    @staticmethod
    def get_by_name(nama_model):
        return ModelKendaraan.query.filter_by(nama_model=nama_model).first()

    @staticmethod
    def create(id_merek, nama_model):
        # 1. cek apaakah model kendaraaan sudah ada
        existing = ModelKendaraanRepository.get_by_name(nama_model)
        if existing:
            raise ValueError(f"Model Kendaraan dengan nama '{nama_model}' sudah ada")
        # 2. mengambil data merek
        merek = MerekRepository.get_by_id(id_merek=id_merek)
        if not merek:
            raise ValueError(f"Merek Kendaraan tidak tersedia")

        # 3. Buat instansi model kendaraan baru
        model = ModelKendaraan(id_merek=merek.id_merek, nama_model=nama_model)
        db.session.add(model)
        db.session.commit()

        return model

    @staticmethod
    def update(id_model, id_merek=None, nama_model=None):
        # 1. apakah model sudah ada
        model = ModelKendaraanRepository.get_by_id(id_model)
        if not model:
            raise ValueError(f"Model dengan ID {id_model} tidak ditemukan")

        updated = False
        # 2. cek apakah merek ada dan update
        if id_merek is not None:
            merek = MerekRepository.get_by_id(id_merek=id_merek)
            if not merek:
                raise ValueError("Merek tidak ditemukan")
            model.id_merek = merek.id_merek
            updated = True
        # 3. cek apakah model ada dan update
        if nama_model is not None:
            existing = ModelKendaraanRepository.get_by_name(nama_model)
            if existing and existing.id_model != id_model:
                raise ValueError(
                    f"Model Kendaraan dengan nama '{nama_model}' sudah ada"
                )
            model.nama_model = nama_model
            updated = True

        if not updated:
            raise ValueError("Tidak ada data yang diupdate")

        db.session.commit()
        return model

    @staticmethod
    def delete(id_model):
        # 1. cek apakah model kendaraan ada
        model = ModelKendaraan.query.get(id_model)
        if not model:
            raise ValueError(f"Model dengan ID {id_model} tidak ditemukan")
        # 2. delete model kendaraan
        ModelKendaraan.query.filter_by(id_model=id_model).delete()
        db.session.commit()

        return True
