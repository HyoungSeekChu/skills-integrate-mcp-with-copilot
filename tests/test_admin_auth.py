from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_mutations_require_teacher_login():
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "unauthorized@mergington.edu"},
    )
    unregister_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"},
    )

    assert signup_response.status_code == 401
    assert unregister_response.status_code == 401


def test_teacher_can_login_register_and_unregister_student():
    email = "auth-test@mergington.edu"
    login_response = client.post(
        "/login",
        json={"username": "teacher", "password": "mergington2026"},
    )

    assert login_response.status_code == 200
    assert client.get("/auth/status").json() == {"authenticated": True}

    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": email},
    )
    assert unregister_response.status_code == 200

    logout_response = client.post("/logout")
    assert logout_response.status_code == 200
    assert client.get("/auth/status").json() == {"authenticated": False}


def test_invalid_teacher_credentials_are_rejected():
    response = client.post(
        "/login",
        json={"username": "teacher", "password": "wrong-password"},
    )

    assert response.status_code == 401