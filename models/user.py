from app.data import USERS, PETS
from flask import current_app


class User:
    def __init__(self, id: int, name: str, permission: str):
        self.id = id
        self.name = name
        self.permission = permission

    def get_pets(self):
        pets = []
        for pid, info in PETS.items():
            if info.get("owner_id") == self.id:
                pet = {"id": pid, **info}
                pets.append(pet)
        return pets

    @staticmethod
    def get_current_user():
        current_user_id = current_app.config.get("CURRENT_USER_ID")
        if current_user_id is None:
            return None

        try:
            user_id = int(current_user_id)
        except (TypeError, ValueError):
            return None

        current_user = USERS.get(user_id)
        if not current_user:
            return None

        permission = current_user.get("permission", None)
        return User(user_id, current_user.get("name"), permission)