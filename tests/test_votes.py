import pytest


def test_vote_post(authorized_client, create_posts):
    r = authorized_client.post(f"/votes/", json={'post_id': create_posts[0].id, 'dir': 1})
    assert r.status_code == 201
    assert r.json()['message'] == 'successfully added vote'


def test_vote_post_already_voted(authorized_client, create_posts, create_vote):
    r = authorized_client.post(f"/votes/", json={'post_id': create_posts[0].id, 'dir': 1})
    assert r.status_code == 409


def test_delete_vote(authorized_client, create_posts, create_vote):
    r = authorized_client.post(f"/votes/", json={'post_id': create_posts[0].id, 'dir': 0})
    assert r.status_code == 201
    assert r.json()['message'] == 'successfully deleted vote'


def test_delete_vote_non_exist(authorized_client, create_posts):
    r = authorized_client.post(f"/votes/", json={'post_id': create_posts[0].id, 'dir': 0})
    assert r.status_code == 404


def test_vote_post_wrong_id(authorized_client, create_posts):
    r = authorized_client.post(f"/votes/", json={'post_id': 9999, 'dir': 0})
    assert r.status_code == 404
    assert r.json()['detail'] == 'Post with id 9999 does not exist'


@pytest.mark.parametrize("dir", [1, 0])
def test_vote_post_unauthorized(client, create_posts, dir):
    r = client.post(f"/votes/", json={'post_id': create_posts[0].id, 'dir': dir})
    assert r.status_code == 401