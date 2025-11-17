from app import create_app


def test_home_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    # make sure the body contains the expected greeting
    assert b"Hello from Flask" in response.data
