from app import create_app


def test_create_vaccine_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import VACCINES

    before_ids = set(VACCINES.keys())

    resp = client.post(
        "/pets/1/create_vaccine_record",
        data={"name": "TestVaccine", "date_administered": "2025-01-01"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    after_ids = set(VACCINES.keys())
    new_ids = after_ids - before_ids
    assert len(new_ids) == 1
    new_id = new_ids.pop()
    assert VACCINES[new_id]["pet_id"] == 1
    assert VACCINES[new_id]["name"] == "TestVaccine"
    assert VACCINES[new_id]["date_administered"] == "2025-01-01"


def test_update_vaccine_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1 and vaccine 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import VACCINES

    # ensure vaccine 1 exists and belongs to pet 1
    assert 1 in VACCINES and VACCINES[1]["pet_id"] == 1

    old_name = VACCINES[1]["name"]

    resp_get = client.get("/pets/1/edit_vaccine_record/1")
    assert resp_get.status_code == 200

    # post update
    resp = client.post(
        "/pets/1/edit_vaccine_record/1",
        data={"name": "UpdatedVaccine", "date_administered": "2025-02-02"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    assert VACCINES[1]["name"] == "UpdatedVaccine"
    assert VACCINES[1]["date_administered"] == "2025-02-02"
    assert VACCINES[1]["name"] != old_name


def test_delete_vaccine_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import VACCINES

    # create a temporary vaccine to delete
    new_id = max(VACCINES.keys(), default=0) + 1
    VACCINES[new_id] = {"pet_id": 1, "name": "ToDelete", "date_administered": "2025-03-03"}
    assert new_id in VACCINES

    resp = client.post(f"/pets/1/delete_vaccine_record/{new_id}", follow_redirects=True)
    assert resp.status_code == 200
    assert new_id not in VACCINES
