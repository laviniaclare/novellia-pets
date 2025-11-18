from app import create_app


def test_home_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    # make sure the body contains the expected greeting and a select
    assert b"Hello from Flask" in response.data or b"Welcome to Novellia Pets" in response.data
    assert b"<select" in response.data
    # ensure at least one user option is present
    assert b"<option value=\"1\"" in response.data or b"Alice" in response.data


def test_set_current_user():
    app = create_app()
    client = app.test_client()

    # select user id 2 (Bob)
    resp = client.post("/select-user", data={"user": "2"}, follow_redirects=True)
    # after posting we redirect to /pets so the response should be the pets page
    assert resp.status_code == 200
    # app config should be updated
    assert app.config["CURRENT_USER_ID"] == 2
    # the pets page should show at least one pet for Bob (check PETS data)
    from app.data import PETS
    # find a pet owned by user 2 and ensure its name appears on the page
    pet_names = [info.get("name") for pid, info in PETS.items() if info.get("owner_id") == 2]
    assert any(name.encode() in resp.data for name in pet_names)


def test_delete_pet():
    app = create_app()
    client = app.test_client()
    # select user 2 (Bob) who will own the temporary pet
    client.post("/select-user", data={"user": "2"}, follow_redirects=True)

    # create a temporary pet owned by user 2 so we don't delete a fixture
    from app.data import PETS, animalType
    # pick a new id (next integer not present in PETS)
    new_id = max(PETS.keys(), default=0) + 1
    PETS[new_id] = {
        "name": "TempPet",
        "type": animalType.CAT,
        "owner_id": 2,
        "dob": "2020-01-01",
    }
    # sanity check the pet exists
    assert new_id in PETS

    # perform delete of the newly created pet
    resp = client.post(f"/pets/{new_id}/delete", follow_redirects=True)
    assert resp.status_code == 200

    # pet should be removed from in-memory store
    assert new_id not in PETS
