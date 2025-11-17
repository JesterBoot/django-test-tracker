from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse

from tests.workflows.factories import CommentFactory, TaskFactory
from workflows.models import Comment


@pytest.mark.django_db
def test_create_and_list_comments(auth_client, user):
    task = TaskFactory(created_by=user)
    url = reverse("comment-list", kwargs={"task_id": task.id})

    create_response = auth_client.post(url, {"text": "First"}, format="json")

    assert create_response.status_code == HTTPStatus.CREATED
    data = create_response.json()
    assert data["text"] == "First"
    assert data["task_id"] == str(task.id)
    assert data["author_id"] == str(user.id)

    list_response = auth_client.get(url)
    assert list_response.status_code == HTTPStatus.OK
    assert len(list_response.json()) == 1


@pytest.mark.django_db
def test_comment_update_only_author(make_auth_client, user, other_user):
    comment = CommentFactory(author=user)
    url = reverse("comment-detail", kwargs={"comment_id": comment.id})

    forbidden_response = make_auth_client(other_user).patch(url, {"text": "Nope"}, format="json")
    assert forbidden_response.status_code == HTTPStatus.FORBIDDEN
    comment.refresh_from_db()
    assert comment.text != "Nope"

    ok_response = make_auth_client(user).patch(url, {"text": "Updated"}, format="json")
    assert ok_response.status_code == HTTPStatus.OK
    comment.refresh_from_db()
    assert comment.text == "Updated"


@pytest.mark.django_db
def test_comment_delete_only_author(make_auth_client, user, other_user):
    comment = CommentFactory(author=user)
    url = reverse("comment-detail", kwargs={"comment_id": comment.id})

    forbidden_response = make_auth_client(other_user).delete(url)
    assert forbidden_response.status_code == HTTPStatus.FORBIDDEN
    assert Comment.objects.filter(id=comment.id).exists()

    ok_response = make_auth_client(user).delete(url)
    assert ok_response.status_code == HTTPStatus.NO_CONTENT
    assert not Comment.objects.filter(id=comment.id).exists()


@pytest.mark.django_db
def test_comment_not_found_returns_404(auth_client):
    url = reverse("comment-detail", kwargs={"comment_id": uuid4()})

    response = auth_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get("error") == "comment_not_found"


@pytest.mark.django_db
def test_list_for_missing_task_returns_404(auth_client):
    url = reverse("comment-list", kwargs={"task_id": uuid4()})

    response = auth_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get("error") == "task_not_found"


@pytest.mark.django_db
def test_create_for_missing_task_returns_404(auth_client):
    url = reverse("comment-list", kwargs={"task_id": uuid4()})

    response = auth_client.post(url, {"text": "Orphan"}, format="json")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get("error") == "task_not_found"


@pytest.mark.django_db
def test_get_comment_detail_success(auth_client, user):
    comment = CommentFactory(author=user)
    url = reverse("comment-detail", kwargs={"comment_id": comment.id})

    response = auth_client.get(url)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == str(comment.id)
