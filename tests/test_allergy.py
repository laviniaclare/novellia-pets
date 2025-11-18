from app import create_app


def test_create_allergy_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import ALLERGIES

    before_ids = set(ALLERGIES.keys())

    resp = client.post(
        "/pets/1/create_allergy_record",
        data={"allergy_name": "TestAllergy", "reactions": "Sneezing", "severity": "MILD"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    after_ids = set(ALLERGIES.keys())
    new_ids = after_ids - before_ids
    assert len(new_ids) == 1
    new_id = new_ids.pop()
    assert ALLERGIES[new_id]["pet_id"] == 1
    assert ALLERGIES[new_id]["allergy_name"] == "TestAllergy"
    assert ALLERGIES[new_id]["reactions"] == "Sneezing"
    # severity stored as enum member
    from app.data import allergySeverity
    assert ALLERGIES[new_id]["severity"] == allergySeverity.MILD


def test_update_allergy_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1 and has allergy id 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import ALLERGIES

    # ensure at least one allergy exists for pet 1
    found = [aid for aid, info in ALLERGIES.items() if info.get("pet_id") == 1]
    assert found
    aid = found[0]

    old_name = ALLERGIES[aid]["allergy_name"]

    resp_get = client.get(f"/pets/1/edit_allergy_record/{aid}")
    assert resp_get.status_code == 200

    # post update
    resp = client.post(
        f"/pets/1/edit_allergy_record/{aid}",
        data={"allergy_name": "UpdatedAllergy", "reactions": "Itching", "severity": "SEVERE"},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    assert ALLERGIES[aid]["allergy_name"] == "UpdatedAllergy"
    assert ALLERGIES[aid]["reactions"] == "Itching"
    from app.data import allergySeverity
    assert ALLERGIES[aid]["severity"] == allergySeverity.SEVERE
    assert ALLERGIES[aid]["allergy_name"] != old_name


def test_delete_allergy_record():
    app = create_app()
    client = app.test_client()

    # select user 1 who owns pet 1
    client.post("/select-user", data={"user": "1"}, follow_redirects=True)

    from app.data import ALLERGIES

    # create a temporary allergy to delete
    new_id = max(ALLERGIES.keys(), default=0) + 1
    ALLERGIES[new_id] = {"pet_id": 1, "allergy_name": "ToDelete", "reactions": "Sneezing", "severity": None}
    assert new_id in ALLERGIES

    resp = client.post(f"/pets/1/delete_allergy_record/{new_id}", follow_redirects=True)
    assert resp.status_code == 200
    assert new_id not in ALLERGIES
