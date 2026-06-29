import os
from app.extensions import db
from app.models.ml_models_model import MlModel
from app.models.riwayat_prediksi_model import RiwayatPrediksi


class MlModelsRepository:
    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        query = MlModel.query

        # 1. Filter berdasarkan search keyword
        if search:
            query = query.filter(MlModel.versi.ilike(f"%{search}%"))

        # 2. Sorting by tanggal
        query = query.order_by(MlModel.uploaded_at.desc())

        # 3. pagination
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated.items, paginated.total, paginated.pages

    @staticmethod
    def get_by_id(id_ml_model):
        return MlModel.query.get(id_ml_model)

    @staticmethod
    def get_by_versi(versi):
        return MlModel.query.filter_by(versi=versi).first()

    @staticmethod
    def get_active_model():
        model_active = MlModel.query.filter_by(is_current=True).first()
        total_model = MlModel.query.count()
        return model_active, total_model

    @staticmethod
    def create(uploaded_by, file_path, versi, r_squared, mae):
        # 1. Cek apakah versi sudah ada
        existing_model = MlModelsRepository.get_by_versi(versi)
        if existing_model:
            raise ValueError(f"Model ML dengan versi '{versi}' sudah ada")

        # 2. Cek apakah file path sudah ada
        existing_path = MlModel.query.filter_by(file_path=file_path).first()
        if existing_path:
            raise ValueError(f"Model ML dengan path '{file_path}' sudah ada")

        # 3. Set model lama menjadi tidak aktif (is_current = False)
        MlModel.query.filter_by(is_current=True).update({"is_current": False})

        # 4. Buat instansi model ML baru
        ml_model = MlModel(
            uploaded_by=uploaded_by,
            file_path=file_path,
            versi=versi,
            r_squared=r_squared,
            mae=mae,
            is_current=True,
        )
        db.session.add(ml_model)
        db.session.commit()

        return ml_model

    @staticmethod
    def set_active(id_ml_model):
        model = MlModelsRepository.get_by_id(id_ml_model)
        # 1. cek apakah model ada
        if not model:
            raise ValueError(f"Model ML dengan ID {id_ml_model} tidak ditemukan")
        # 2. cek apakah model yang dipilih itu aktif
        if not model.is_current:
            # 3. update status model yang aktif menjadi false
            MlModel.query.filter_by(is_current=True).update({"is_current": False})
            # 4. update status model yang dipilih menjadi aktif
            model.is_current = True
            db.session.commit()

        return model

    @staticmethod
    def delete(id_ml_model):
        # 1. cek apakah model ada
        existing_model = MlModel.query.get(id_ml_model)

        if not existing_model:
            raise ValueError(f"Model ML dengan ID {id_ml_model} tidak ditemukan")

        # 2. Cegah penghapusan model yang sudah dipakai riwayat prediksi.
        has_predict_history = RiwayatPrediksi.query.filter_by(
            id_ml_model=id_ml_model
        ).first()
        if has_predict_history:
            raise ValueError(
                f"Model ML dengan ID {id_ml_model} tidak bisa dihapus karena sudah dipakai pada riwayat prediksi"
            )

        # 3. delete model
        MlModel.query.filter_by(id_ml_model=id_ml_model).delete()
        db.session.commit()

        return existing_model
