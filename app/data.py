from enum import Enum

class allergySeverity(Enum):
    MILD = "Mild"
    SEVERE = "Severe"

class animalType(Enum):
    DOG = "Dog"
    CAT = "Cat"
    BIRD = "Bird"
    RABBIT = "Rabbit"
    OTHER = "Other"

PETS = {
    1: {"name": "Fido", "type": animalType.DOG, "owner_name": "Alice", "dob": "2018-06-01" },
    2: {"name": "Whiskers", "type": animalType.CAT, "owner_name": "Bob", "dob": "2019-09-15" },
    3: {"name": "Tweety", "type": animalType.BIRD, "owner_name": "Carol", "dob": "2020-03-22" },
}

VACCINES = {
    1: {"pet_id": 1, "name": "Rabies", "date_administered": "2019-06-01"},
    2: {"pet_id": 2, "name": "Feline Distemper", "date_administered": "2020-09-15"},
}

ALLERGIES = {
    1: {"pet_id": 1, "allergy_name": "Pollen", "reactions": "Sneezing", "severity": allergySeverity.MILD},
}
