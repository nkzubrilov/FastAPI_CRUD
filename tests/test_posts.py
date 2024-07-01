from datetime import datetime
from sqlalchemy import select
import pytest

from app import schemas, models


def test_get_all_posts(authorized_client, create_posts):
    r = authorized_client.get("/posts/")
    posts = r.json()
    assert r.status_code == 200
    assert len(posts) == len(create_posts)

    posts.sort(key=lambda x: x['post']['id'])
    create_posts.sort(key=lambda x: x.id)
    for post, model in zip(posts, create_posts):
        assert post['post']['title'] == model.title
        assert post['post']['content'] == model.content
        assert post['post']['id'] == model.id
        assert datetime.fromisoformat(post['post']['created_at']) == model.created_at
        assert post['post']['user_id'] == model.user_id


def test_get_one_post(authorized_client, create_posts):
    r = authorized_client.get(f"/posts/{create_posts[1].id}")
    post = r.json()
    model = create_posts[1]
    assert post['post']['title'] == model.title
    assert post['post']['content'] == model.content
    assert post['post']['id'] == model.id
    assert datetime.fromisoformat(post['post']['created_at']) == model.created_at
    assert post['post']['user_id'] == model.user_id


def test_get_all_posts_unauthorized(client, create_posts):
    r = client.get("/posts/")
    assert r.status_code == 401


def test_get_one_post_unauthorized(client, create_posts):
    r = client.get(f"/posts/{create_posts[0].id}")
    assert r.status_code == 401


def test_get_post_wrong_id(authorized_client, create_posts):
    r = authorized_client.get("/posts/9999")
    assert r.status_code == 404
    assert r.json()['detail'] == 'Post with ID 9999 was not found'


@pytest.mark.parametrize("title, content, published", [
                             ('new title!', 'new content!', True),
                             ('test title', 'test content', False),
                             ('Hello world!', 'I love Python!', True)
                         ])
def test_create_post(authorized_client, create_user, title, content, published):
    user = create_user[0]
    r = authorized_client.post("/posts/", json={'title': title, 'content': content, 'published': published})
    new_post = schemas.PostResponse(**r.json())
    assert r.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.user_id == user['id']


def test_create_post_default_published(authorized_client, create_user):
    user = create_user[0]
    r = authorized_client.post("/posts/", json={'title': 'some title', 'content': 'and some content'})
    new_post = schemas.PostResponse(**r.json())
    assert r.status_code == 201
    assert new_post.title == 'some title'
    assert new_post.content == 'and some content'
    assert new_post.published is True
    assert new_post.user_id == user['id']


def test_create_post_unauthorized(client):
    r = client.post("/posts/", json={'title': 'some title', 'content': 'and some content'})
    assert r.status_code == 401


def test_delete_post(authorized_client, session, create_posts):
    r = authorized_client.delete(f"/posts/{create_posts[0].id}")
    posts_after_deletion = session.scalars(select(models.Posts)).all()
    assert r.status_code == 204
    assert len(posts_after_deletion) == len(create_posts) - 1


def test_delete_post_wrong_id(authorized_client, create_posts):
    r = authorized_client.delete(f"/posts/9999")
    assert r.status_code == 404
    assert r.json()['detail'] == 'Post with ID 9999 does not exist'


def test_delete_post_unauthorized(client, create_posts):
    r = client.delete((f"/posts/{create_posts[2].id}"))
    assert r.status_code == 401


def test_delete_other_user_post(authorized_client, create_posts):
    r = authorized_client.delete(f"/posts/{create_posts[-1].id}")
    assert r.status_code == 403


def test_update_post(authorized_client, create_posts):
    post_data = {'title': 'upd. title',
                 'content': 'updated content',
                 'id': create_posts[0].id}
    r = authorized_client.put(f"/posts/{create_posts[0].id}", json=post_data)
    assert r.status_code == 200
    updated_post = schemas.PostResponse(**r.json())
    assert updated_post.title == post_data['title']
    assert updated_post.content == post_data['content']
    assert updated_post.id == post_data['id']


def test_update_other_user_post(authorized_client, create_posts):
    post_data = {'title': 'upd. title',
                 'content': 'updated content',
                 'id': create_posts[-1].id}
    r = authorized_client.put(f"/posts/{create_posts[-1].id}", json=post_data)
    assert r.status_code == 403
    assert r.json()['detail'] == 'Not authorized to perform the requested action'


def test_update_post_unauthorized(client, create_posts):
    post_data = {'title': 'upd. title',
                 'content': 'updated content',
                 'id': create_posts[0].id}
    r = client.put(f"/posts/{create_posts[0].id}", json=post_data)
    assert r.status_code == 401


def test_update_post_wrong_id(authorized_client, create_posts):
    post_data = {'title': 'upd. title',
                 'content': 'updated content',
                 'id': '9999'}
    r = authorized_client.put(f"/posts/9999", json=post_data)
    assert r.status_code == 404
    assert r.json()['detail'] == 'Post with ID 9999 does not exist'
