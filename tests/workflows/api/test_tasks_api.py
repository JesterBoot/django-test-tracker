from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse

from tests.users.factories import UserFactory
from tests.workflows.factories import TaskFactory
from workflows.models import Task
from workflows.models.enums import TaskStatus


@pytest.mark.django_db
def test_create_task_with_assignee(auth_client, user, other_user):
    url = reverse("task-list")
    payload = {
        "title": "New task",
        "description": "Test task description",
        "assignee_id": str(other_user.id),
    }

    response = auth_client.post(url, payload, format="json")

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    task = Task.objects.get(id=data["id"])
    assert data["title"] == payload["title"]
    assert data["assignee_id"] == str(other_user.id)
    assert task.created_by_id == user.id
    assert task.assignee_id == other_user.id


@pytest.mark.django_db
def test_list_tasks_filters_by_status_and_assignee(make_auth_client, user, other_user):
    target = TaskFactory(
        status=TaskStatus.IN_PROGRESS,
        created_by=user,
        assignee=other_user,
    )
    TaskFactory(status=TaskStatus.TODO)

    client = make_auth_client(user)
    url = reverse("task-list")
    response = client.get(
        url,
        {"status": TaskStatus.IN_PROGRESS, "assignee_id": str(other_user.id)},
    )

    assert response.status_code == HTTPStatus.OK
    ids = [item["id"] for item in response.json()]
    assert ids == [str(target.id)]


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("client_role", "expected_status"),
    (
        ("creator", HTTPStatus.OK),
        ("assignee", HTTPStatus.OK),
        ("stranger", HTTPStatus.FORBIDDEN),
    ),
)
def test_update_permissions(make_auth_client, user, other_user, client_role, expected_status):
    task = TaskFactory(created_by=user, assignee=other_user)
    clients = {
        "creator": make_auth_client(user),
        "assignee": make_auth_client(other_user),
        "stranger": make_auth_client(UserFactory()),
    }
    url = reverse("task-detail", kwargs={"task_id": task.id})

    response = clients[client_role].patch(url, {"title": "Updated"}, format="json")

    assert response.status_code == expected_status
    task.refresh_from_db()
    if expected_status == HTTPStatus.OK:
        assert task.title == "Updated"
    else:
        assert task.title != "Updated"


@pytest.mark.django_db
def test_delete_only_creator(make_auth_client, user, other_user):
    task = TaskFactory(created_by=user, assignee=other_user)
    assignee_client = make_auth_client(other_user)
    creator_client = make_auth_client(user)
    url = reverse("task-detail", kwargs={"task_id": task.id})

    forbidden_response = assignee_client.delete(url)
    assert forbidden_response.status_code == HTTPStatus.FORBIDDEN
    assert Task.objects.filter(id=task.id).exists()

    ok_response = creator_client.delete(url)
    assert ok_response.status_code == HTTPStatus.NO_CONTENT
    assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_get_nonexistent_task_returns_404(auth_client):
    url = reverse("task-detail", kwargs={"task_id": uuid4()})

    response = auth_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json().get("error") == "task_not_found"


@pytest.mark.django_db
def test_get_task_detail_success(make_auth_client, user, other_user):
    task = TaskFactory(created_by=user, assignee=other_user)
    client = make_auth_client(user)
    url = reverse("task-detail", kwargs={"task_id": task.id})

    response = client.get(url)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["id"] == str(task.id)
    assert data["assignee_id"] == str(other_user.id)
