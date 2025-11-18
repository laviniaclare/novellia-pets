from app.data import PETS, ALLERGIES, VACCINES


class VaccineRecord:
    def __init__(self, id: int, name, pet_id, date_administered):
        self.id = id
        self.name = name
        self.pet_id = pet_id
        self.date_administered = date_administered

    @staticmethod
    def get_vaccine_record_by_id(vaccine_record_id: int):
        # ensure numeric id
        try:
            vaccine_record_id = int(vaccine_record_id)
        except (TypeError, ValueError):
            return None

        vaccine_record = VACCINES.get(vaccine_record_id)
        if vaccine_record:
            return VaccineRecord(vaccine_record_id, vaccine_record["name"], vaccine_record["pet_id"], vaccine_record["date_administered"])
        return None

