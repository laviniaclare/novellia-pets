from flask import Blueprint
from .data import PETS, VACCINES, ALLERGIES, animalType, allergySeverity

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return "Hello from Flask — home endpoint!\n"
