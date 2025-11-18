from app.data import PETS, ALLERGIES, VACCINES
from models.vaccine_record import VaccineRecord


class Pet:
    def __init__(self, id: int, name, type, owner_id, dob):
        self.id = id
        self.name = name
        self.type = type
        self.owner_id = owner_id
        self.dob = dob

    @staticmethod
    def get_pet_by_id(pet_id: int):
        # ensure numeric id
        try:
            pid = int(pet_id)
        except (TypeError, ValueError):
            return None

        pet = PETS.get(pid)
        if pet:
            return Pet(pid, pet["name"], pet.get("type"), pet.get("owner_id"), pet.get("dob"))
        return None

    def get_allergies(self):
        results = []
        for allergy_id, info in ALLERGIES.items():
            if info.get("pet_id") == self.id:
                results.append({"id": allergy_id, **info})
        return results

    def get_vaccines(self):
        results = []
        for vaccine_id, info in VACCINES.items():
            if info.get("pet_id") == self.id:
                results.append(VaccineRecord(vaccine_id, info["name"], info["pet_id"], info["date_administered"]))
        return results
