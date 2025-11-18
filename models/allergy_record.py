from app.data import PETS, ALLERGIES, VACCINES


class AllergyRecord:
    def __init__(self, id: int, allergy_name: str, pet_id: int, reactions: str, severity: str):
        self.id = id
        self.allergy_name = allergy_name
        self.pet_id = pet_id
        self.reactions = reactions
        self.severity = severity

    @staticmethod
    def get_allergy_record_by_id(allergy_record_id: int):
        # ensure numeric id
        try:
            allergy_record_id = int(allergy_record_id)
        except (TypeError, ValueError):
            return None

        allergy_record = ALLERGIES.get(allergy_record_id)
        if allergy_record:
            return AllergyRecord(allergy_record_id, allergy_record["allergy_name"], allergy_record["pet_id"], allergy_record["reactions"], allergy_record["severity"])
        return None

