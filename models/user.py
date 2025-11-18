from app.data import USERS, PETS


class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def get_pets(self):
        pets = []
        for pid, info in PETS.items():
            if info.get("owner_id") == self.id:
                pet = {"id": pid, **info}
                pets.append(pet)
        return pets

    @staticmethod
    def get_current_user(current_user_id: int):
        if current_user_id is None:
            return None

        entry = USERS.get(int(current_user_id))
        if not entry:
            return None
        return User(int(current_user_id), entry.get("name"))