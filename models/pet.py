from app.data import PETS, ALLERGIES, VACCINES, animalType
from models.vaccine_record import VaccineRecord
from models.allergy_record import AllergyRecord


class Pet:
    def __init__(self, id: int, name: str, type: str, owner_id: int, dob: str):
        self.id = id
        self.name = name
        self.type = type
        self.owner_id = owner_id
        self.dob = dob

    @staticmethod
    def get_pet_by_id(pet_id: int):
        # ensure numeric id
        try:
            pet_id = int(pet_id)
        except (TypeError, ValueError):
            return None

        pet = PETS.get(pet_id)
        if pet:
            return Pet(pet_id, pet["name"], pet.get("type"), pet.get("owner_id"), pet.get("dob"))
        return None

    @staticmethod
    def get_pets_by_name(query):
        """
        Return a list of pet objects whose name matches the query (case-insensitive exact match).
        A nice future improvement would be to implement fuzzy matching.
        """
        if query is None:
            return []

        q = query.strip().lower()
        results = []
        for pet_id, info in PETS.items():
            pet_name = info.get("name", "")
            if pet_name and pet_name.lower() == q:
                pet = Pet(pet_id, info.get("name"), info.get("type"), info.get("owner_id"), info.get("dob"))
                pet_type = pet.type
                if hasattr(pet_type, "value"):
                    pet.type = pet_type.value
                results.append(pet)

        return results
    
    @staticmethod
    def get_pets_by_type(query):
        """
        Return a list of pet objects whose type matches the query (case-insensitive exact match).
        A nice future improvement would be to implement fuzzy matching.
        """
        if query is None:
            return []

        q = query.strip().lower()
        results = []
        for pet_id, info in PETS.items():
            pet_type = info.get("type")
            if pet_type and pet_type.value.lower() == q:
                pet = Pet(pet_id, info.get("name"), info.get("type"), info.get("owner_id"), info.get("dob"))
                if hasattr(pet.type, "value"):
                    pet.type = pet.type.value
                results.append(pet)

        return results

    @staticmethod
    def get_pet_counts_by_type():
        pet_counts_by_type = {}
        # This is NOT very efficient. If we were using a real db we would use a db query,
        # which would be much more efficient, but since our dataset is so small it's not 
        # a huge concern right now
        for pet in PETS.values():
            pet_type = pet["type"].value
            pet_counts_by_type[pet_type] = pet_counts_by_type.get(pet_type, 0) + 1
        
        for type in animalType:
            if not type in pet_counts_by_type:
                pet_counts_by_type[type.value] = 0
        
        return pet_counts_by_type

    def get_allergies(self):
        results = []
        for allergy_id, info in ALLERGIES.items():
            if info.get("pet_id") == self.id:
                results.append(AllergyRecord(allergy_id, info.get("allergy_name"), info.get("pet_id"), info.get("reactions"), info.get("severity")))
        return results

    def get_vaccines(self):
        results = []
        for vaccine_id, info in VACCINES.items():
            if info.get("pet_id") == self.id:
                results.append(VaccineRecord(vaccine_id, info["name"], info["pet_id"], info["date_administered"]))
        return results
