from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
import pytest

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:"
                           f"{settings.db_port}/{settings.db_name}_test")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def create_user(client):
    users_data = [{'email': 'new.user@gmail.com', 'password': '_123QwErTy!#.-'},
                 {'email': 'second.user@testmail.abc', 'password': '__password__()'}]
    users = []
    for user in users_data:
        r = client.post("/users/", json=user)
        assert r.status_code == 201
        new_user = r.json()
        new_user['password'] = user['password']
        users.append(new_user)
    return users


@pytest.fixture
def authorized_client(client, create_user):
    user = create_user[0]
    token = create_access_token(data={'user_id': user['id']})
    client.headers['Authorization'] = f'Bearer {token}'
    return client


@pytest.fixture
def create_posts(create_user, session):
    posts_data = [{
        'title': 'first post!',
        'content': 'some stuff',
        'user_id': create_user[0]['id']
    }, {
        'title': 'second post!',
        'content': 'another some stuff',
        'user_id': create_user[0]['id']
    }, {
        'title': 'third post!',
        'content': 'yet another some stuff',
        'user_id': create_user[0]['id']
    }, {
        'title': 'another user post',
        'content': 'written by second user!',
        'user_id': create_user[1]['id']
    }]

    session.add_all(map(lambda x: models.Posts(**x), posts_data))
    session.commit()
    return session.scalars(select(models.Posts)).all()


@pytest.fixture
def create_vote(create_posts, create_user, session):
    vote = models.Votes(user_id=create_user[0]['id'], post_id=create_posts[0].id)
    session.add(vote)
    session.commit()
