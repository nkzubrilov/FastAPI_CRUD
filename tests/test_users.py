import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    r = client.post("/users/", json={'email': 'test@testmail.xyz', 'password': 'qwerty'})
    new_user = schemas.UserResponse(**r.json())
    assert r.status_code == 201
    assert new_user.email == 'test@testmail.xyz'


def test_login_user(client, create_user):
    user = create_user[0]
    r = client.post("/login", data={'username': user['email'], 'password': user['password']})
    assert r.status_code == 200
    login_response = schemas.Token(**r.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, settings.algorithm)
    user_id = payload.get('user_id')
    assert user_id == user['id']
    assert login_response.token_type == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [('true_data', 'some_random_password', 403),
                                                          ('wrong@email.abc', 'true_data', 403),
                                                          ('wrong123@yahoo.com', '111wronpassword111', 403),
                                                          (None, 'true_data', 422),
                                                          ('true_data', None, 422)])
def test_wrong_login(client, create_user, email, password, status_code):
    user = create_user[1]
    if email == 'true_data':
        email = user['email']
    if password == 'true_data':
        password = user['password']
    r = client.post("/login", data={'username': email, 'password': password})
    assert r.status_code == status_code


def test_get_user(client, create_user):
    user = create_user[0]
    r = client.get(f"/users/{user['id']}")
    assert r.status_code == 200
    user_schema = schemas.UserResponse(**r.json())
    assert user_schema.id == user['id']
    assert user_schema.email == user['email']
    assert user_schema.created_at


def test_get_wrong_user(client, create_user):
    r = client.get("/users/-9999")
    assert r.status_code == 404
    assert r.json()['detail'] == 'User with ID -9999 was not found'
