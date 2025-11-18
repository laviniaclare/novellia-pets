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
    1: {"name": "Pete", "type": animalType.DOG, "owner_id": 1, "dob": "2018-06-01" },
    2: {"name": "Darling", "type": animalType.CAT, "owner_id": 2, "dob": "2019-09-15" },
    3: {"name": "Tweety", "type": animalType.BIRD, "owner_id": 3, "dob": "2020-03-22" },
    4: {"name": "Cleo", "type": animalType.RABBIT, "owner_id": 1, "dob": "2021-11-11" },
}

VACCINES = {
    1: {"pet_id": 1, "name": "Rabies", "date_administered": "2019-06-01"},
    2: {"pet_id": 2, "name": "Feline Distemper", "date_administered": "2020-09-15"},
    3: {"pet_id": 1, "name": "Parvovirus", "date_administered": "2021-03-22"},
}

ALLERGIES = {
    1: {"pet_id": 1, "allergy_name": "Pollen", "reactions": "Sneezing", "severity": allergySeverity.MILD},
    2: {"pet_id": 1, "allergy_name": "Chocolate", "reactions": "Itching, Vomiting", "severity": allergySeverity.SEVERE},
}

USERS = {1: {"name": "Alice"}, 2: {"name": "Bob"}, 3: {"name": "Carol"}}
