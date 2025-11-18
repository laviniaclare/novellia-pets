from flask import Blueprint, render_template, request, redirect, url_for, current_app, abort
from .data import PETS, VACCINES, ALLERGIES, USERS, animalType, allergySeverity

from models.user import User
from models.pet import Pet
from models.vaccine_record import VaccineRecord
from models.allergy_record import AllergyRecord

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template(
        "home.html",
        users=USERS,
        current_user_id=current_app.config.get("CURRENT_USER_ID"),
    )


@bp.route("/select-user", methods=["POST"])
def set_user():
    """
    Set the global current user id (stored in app.config) from the form.

    The form sends a field named `user`. If empty, current user is set to None.
    """
    user_val = request.form.get("user", "").strip()
    if user_val:
        try:
            current_app.config["CURRENT_USER_ID"] = int(user_val)
        except ValueError:
            current_app.config["CURRENT_USER_ID"] = None
    else:
        current_app.config["CURRENT_USER_ID"] = None

    return redirect(url_for("main.list_pets"))


@bp.route("/pets", methods=["GET"])
def list_pets():
    current_user_id = current_app.config.get("CURRENT_USER_ID")
    # TODO: It would be nice to add a toast or something if the user is redirected to home
    if not current_user_id:
        return redirect(url_for("main.home"))
    else:
        user = User.get_current_user(current_user_id)
        if user:
            pets = user.get_pets()
        else:
            return redirect(url_for("main.home"))

    return render_template(
        "pets.html",
        pets=pets,
    )


@bp.route("/pets/<int:pet_id>")
def show_pet_profile(pet_id):
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    allergies = pet.get_allergies()
    vaccines = pet.get_vaccines()

    return render_template(
        "pet_profile.html",
        pet=pet,
        allergies=allergies,
        vaccines=vaccines,
    )


@bp.route("/pets/<int:pet_id>/update", methods=["GET", "POST"])
def update_pet(pet_id: int):
    """ 
    GET: Renders the form
    POST: Updates the pet

    Only the owner (current_user_id) may update the pet.
    """
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        type_name = request.form.get("type", "").strip()
        dob = request.form.get("dob", "").strip()

        if not name:
            return render_template("edit_pet_form.html", pet=pet, animalType=animalType, error="Name is required")

        pet_dict = PETS.get(pet_id)
        if pet_dict is None:
            abort(404)

        pet_dict["name"] = name
        # Since users are selecting from a drop down they can only select valid types
        # so we don't need to validate, but we could make it more robust by doing so
        pet_dict["type"] = animalType[type_name]
        pet_dict["dob"] = dob

        return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

    # GET -> render edit form
    return render_template("edit_pet_form.html", pet=pet, animalType=animalType)
    

@bp.route("/pets/create", methods=["GET", "POST"])
def create_pet():
    """
    Create a new pet

    GET: render form
    POST: Add new pet to PETS (in-memory for now, but in a real prod app we would use a database) 
          and then redirect to the new pet's profile
    """
    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if not current_user_id:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        type_name = request.form.get("type", "").strip()
        dob = request.form.get("dob", "").strip()

        if not name:
            # simple validation: name required - We could get fancy with this but for now we're keeping things simple
            return render_template("create_pet_form.html", animalType=animalType, error="Name is required", current_user_id=current_user_id)

        new_pet_id = max(PETS.keys(), default=0) + 1
        pet_type = animalType[type_name]

        PETS[new_pet_id] = {"name": name, "type": pet_type, "owner_id": int(current_user_id), "dob": dob}

        return redirect(url_for("main.show_pet_profile", pet_id=new_pet_id))

    # GET
    return render_template("create_pet_form.html", animalType=animalType, current_user_id=current_app.config.get("CURRENT_USER_ID"))


@bp.route("/pets/<int:pet_id>/delete", methods=["POST"])
def delete_pet(pet_id: int):
    """
    Delete a pet by id
    """
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    # simple ownership check
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    # remove the pet from the in-memory store - in the real world we would use a database
    PETS.pop(pet_id, None)

    return redirect(url_for("main.list_pets"))


@bp.route("/pets/<int:pet_id>/create_vaccine_record", methods=["GET", "POST"])
def create_vaccine_record(pet_id: int):
    """
    Add a new vaccine record to a pet

    GET: render form
    POST: Create a new vaccine record assigned to the given pet
    """
    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if not current_user_id:
        return redirect(url_for("main.home"))

    # ensure the pet exists and the current user owns it
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    if int(pet.owner_id) != int(current_user_id):
        abort(403)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date_administered = request.form.get("date_administered", "").strip()
        new_pet_vaccine_record_id = max(VACCINES.keys(), default=0) + 1

        VACCINES[new_pet_vaccine_record_id] = {"name": name, "date_administered": date_administered, "pet_id": pet_id}

        return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

    return render_template(
        "vaccine_record_form.html",
        pet=pet,
        vaccine=None,
        current_user_id=current_app.config.get("CURRENT_USER_ID"),
    )


@bp.route("/pets/<int:pet_id>/create_allergy_record", methods=["GET", "POST"])
def create_allergy_record(pet_id: int):
    """
    Create a new allergy record for a pet

    GET: render the form
    POST: Create a new allergy record assigned to the given pet
    """
    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if not current_user_id:
        return redirect(url_for("main.home"))

    # ensure the pet exists and the current user owns it
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    if int(pet.owner_id) != int(current_user_id):
        abort(403)

    if request.method == "POST":
        allergy_name = request.form.get("allergy_name", "").strip()
        reactions = request.form.get("reactions", "").strip()
        severity_name = request.form.get("severity", "").strip()

        new_allergy_id = max(ALLERGIES.keys(), default=0) + 1
        severity = allergySeverity[severity_name]

        ALLERGIES[new_allergy_id] = {"pet_id": pet_id, "allergy_name": allergy_name, "reactions": reactions, "severity": severity}

        return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

    return render_template("create_allergy_record_form.html", pet=pet, allergySeverity=allergySeverity)


@bp.route("/pets/<int:pet_id>/edit_vaccine_record/<int:vaccine_id>", methods=["GET", "POST"])
def edit_vaccine_record(pet_id: int, vaccine_id: int):
    """
    Edit an existing vaccine record for a pet.

    GET: render form pre-filled with existing data
    POST: update the record and redirect back to the pet profile
    """
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    vaccine_record = VaccineRecord.get_vaccine_record_by_id(vaccine_id)
    if not vaccine_record:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date_administered = request.form.get("date_administered", "").strip()

        if vaccine_id in VACCINES:
            VACCINES[vaccine_id]["name"] = name
            VACCINES[vaccine_id]["date_administered"] = date_administered
        return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

    return render_template("vaccine_record_form.html", pet=pet, vaccine=vaccine_record)


@bp.route("/pets/<int:pet_id>/edit_allergy_record/<int:allergy_id>", methods=["GET", "POST"])
def edit_allergy_record(pet_id: int, allergy_id: int):
    """
    Edit an existing allergy record for a pet.
    """

    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    allergy_record = AllergyRecord.get_allergy_record_by_id(allergy_id)
    if not allergy_record:
        abort(404)

    if request.method == "POST":
        allergy_name = request.form.get("allergy_name", "").strip()
        reactions = request.form.get("reactions", "").strip()
        severity_name = request.form.get("severity", "").strip()

        if allergy_id in ALLERGIES:
            ALLERGIES[allergy_id]["allergy_name"] = allergy_name
            ALLERGIES[allergy_id]["reactions"] = reactions
            ALLERGIES[allergy_id]["severity"] = allergySeverity[severity_name]
        return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

    return render_template("allergy_record_form.html", pet=pet, allergy=allergy_record, allergySeverity=allergySeverity)


@bp.route("/pets/<int:pet_id>/delete_vaccine_record/<int:vaccine_id>", methods=["POST"])
def delete_vaccine_record(pet_id: int, vaccine_id: int):
    """
    Delete a vaccine record by id 
    """
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    # simple ownership check
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    # remove the vaccine record from the in-memory store - in the real world we would use a database
    VACCINES.pop(vaccine_id, None)

    return redirect(url_for("main.show_pet_profile", pet_id=pet_id))

@bp.route("/pets/<int:pet_id>/delete_allergy_record/<int:allergy_id>", methods=["POST"])
def delete_allergy_record(pet_id: int, allergy_id: int):
    """
    Delete a allergy record by id 
    """
    pet = Pet.get_pet_by_id(pet_id)
    if not pet:
        abort(404)

    current_user_id = current_app.config.get("CURRENT_USER_ID")
    # simple ownership check
    if current_user_id is None or int(pet.owner_id) != int(current_user_id):
        abort(403)

    # remove the allergy record from the in-memory store - in the real world we would use a database
    ALLERGIES.pop(allergy_id, None)

    return redirect(url_for("main.show_pet_profile", pet_id=pet_id))
