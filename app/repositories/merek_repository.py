from app.extensions import db
from app.models.merek_model import Merek
from sqlalchemy import func


class MerekRepository:

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        query = Merek.query

        # 1. Filter berdasarkan search keyword
        if search:
            query = query.filter(Merek.nama_merek.ilike(f"%{search}%"))

        # 2. Sorting by nama_merek
        query = query.order_by(Merek.nama_merek.asc())

        # 3. Pagination
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated.items, paginated.total, paginated.pages

    @staticmethod
    def get_by_id(id_merek):
        return Merek.query.get(id_merek)

    @staticmethod
    def get_by_name(nama_merek):
        return Merek.query.filter_by(nama_merek=nama_merek).first()

    @staticmethod
    def create(nama_merek):
        # 1. Check apakah nama_merek sudah ada
        existing = MerekRepository.get_by_name(nama_merek)
        if existing:
            raise ValueError(f"Merek dengan nama '{nama_merek}' sudah ada")

        # 2. Buat instansi Merek baru
        merek = Merek(nama_merek=nama_merek)
        db.session.add(merek)
        db.session.commit()

        return merek

    @staticmethod
    def update(id_merek, nama_merek):
        # 1. cek apakah merek ada
        merek = MerekRepository.get_by_id(id_merek)
        if not merek:
            raise ValueError(f"Merek dengan ID {id_merek} tidak ditemukan")

        # 2. Check apakah nama baru sudah ada
        existing = Merek.query.filter(
            Merek.nama_merek == nama_merek, Merek.id_merek != id_merek
        ).first()
        if existing:
            raise ValueError(f"Merek dengan nama '{nama_merek}' sudah ada")
        # 3. update merek
        merek.nama_merek = nama_merek
        db.session.commit()

        return merek

    @staticmethod
    def delete(id_merek):
        # 1. cek apakkah merek ada
        merek = MerekRepository.get_by_id(id_merek)
        if not merek:
            raise ValueError(f"Merek dengan ID {id_merek} tidak ditemukan")

        # 2. delete merek
        db.session.delete(merek)
        db.session.commit()

        return True

    @staticmethod
    def count():
        return Merek.query.count()
