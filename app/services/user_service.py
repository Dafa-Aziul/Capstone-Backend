from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_all(page=1, per_page=10, search=None):

        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")

        item_not_organize, total, total_pages = UserRepository.get_all(
            page=page, per_page=per_page, search=search
        )

        return {
            "data": item_not_organize,
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
    def set_status(target_user_id, current_user_id):
        if int(target_user_id) == int(current_user_id):
            raise ValueError("Tidak dapat update status sendiri")
        return UserRepository.set_status_user(target_user_id)