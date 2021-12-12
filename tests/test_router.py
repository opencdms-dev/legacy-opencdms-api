from sqlalchemy.orm.session import Session
from starlette.testclient import TestClient
from passlib.hash import django_pbkdf2_sha256 as handler
from opencdms_api.models import AuthUser


def test_register_new_user(client: TestClient, session: Session):
    assert session.query(AuthUser).count() == 0
    response = client.post(
        "/users",
        json={
            "email": "test_register_new_user@gmail.com",
            "username": "register_new_user",
            "firstName": "Shaibu",
            "lastName": "Shaibu",
            "password": "my_password",
        },
    )
    assert response.status_code == 201
    new_user = session.query(AuthUser).one()
    assert new_user is not None
    assert new_user.username == "register_new_user"
    assert new_user.email == "test_register_new_user@gmail.com"
    assert new_user.first_name == "Shaibu"
    assert new_user.last_name == "Shaibu"
    assert handler.verify("my_password", new_user.password)


def test_register_user_with_existing_username_fail(
    user: AuthUser, client: TestClient, session: Session
):
    prev_count = session.query(AuthUser).count()
    response = client.post(
        "/users",
        json={
            "email": "test_register_user_with_existing_username_fail@gmail.com",  # noqa
            "username": user.username,
            "firstName": "Shaibu",
            "lastName": "Shaibu",
            "password": "my_password",
        },
    )
    assert response.status_code == 409
    session.expire_all()
    assert session.query(AuthUser).count() == prev_count


def test_authenticate_user(user: AuthUser, client: TestClient):
    response = client.post(
        "/auth", json={"username": user.username, "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_authenticate_user_with_wrong_credentials_fail(
    user: AuthUser, client: TestClient
):
    response = client.post(
        "/auth", json={"username": user.username, "password": "wrong_password"}
    )
    assert response.status_code == 400


def test_access_to_surface_api_without_auth_fail(client: TestClient):
    response = client.get("/surface/api/stations")
    assert response.status_code == 401


def test_access_to_mch_api_without_auth_fail(client: TestClient):
    response = client.get("/mch/API/stations")
    assert response.status_code == 401
