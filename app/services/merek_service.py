from app.repositories.merek_repository import MerekRepository


class MerekService:
    @staticmethod
    def get_all_mereks(page=1, per_page=10, search=None):
        # 1. Validasi parameter
        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")

        # 2. Get data dari repository
        items, total, total_pages = MerekRepository.get_all(
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
    def get_merek_by_id(id_merek):
        merek = MerekRepository.get_by_id(id_merek)
        if not merek:
            raise ValueError(f"Merek dengan ID {id_merek} tidak ditemukan")

        return merek

    @staticmethod
    def create_merek(nama_merek):
        # 1. Validasi input
        if not nama_merek or not nama_merek.strip():
            raise ValueError("Nama merek tidak boleh kosong")

        nama_merek = nama_merek.strip()

        # 2. Delegasi ke repository
        return MerekRepository.create(nama_merek)

    @staticmethod
    def update_merek(id_merek, nama_merek):
        # 1. Validasi input
        if not nama_merek or not nama_merek.strip():
            raise ValueError("Nama merek tidak boleh kosong")

        nama_merek = nama_merek.strip()

        # 2. Delegasi ke repository
        return MerekRepository.update(id_merek, nama_merek)

    @staticmethod
    def delete_merek(id_merek):
        # 1. Cek apakah merek punya model kendaraan
        merek = MerekRepository.get_by_id(id_merek)
        if not merek:
            raise ValueError(f"Merek dengan ID {id_merek} tidak ditemukan")

        # 2. Cek relasi (opsional - tergantung cascade policy)
        if merek.model_kendaraans:
            raise ValueError(
                f"Tidak bisa hapus merek '{merek.nama_merek}' karena masih ada model kendaraan"
            )
        # 3. Delegasi ke repository
        return MerekRepository.delete(id_merek)
