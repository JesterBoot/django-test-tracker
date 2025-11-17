from uuid import uuid4

import pytest

from tests.workflows.factories import TaskFactory
from workflows.exceptions.comment_exceptions import (
    CommentNotFoundError,
    CommentPermissionDeniedError,
)
from workflows.exceptions.task_exceptions import TaskNotFoundError, TaskPermissionDeniedError
from workflows.models.enums import TaskStatus
from workflows.selectors.task_selectors import list_tasks_filtered
from workflows.services.comment_services import delete_comment, update_comment
from workflows.services.task_services import (
    complete_task,
    create_task,
    delete_task,
    update_task,
)


@pytest.mark.django_db
def test_create_task_assigns_assignee(user, other_user):
    task = create_task(
        {"title": "X", "description": "Y", "assignee_id": other_user.id},
        user=user,
    )
    assert task.assignee_id == other_user.id
    assert task.created_by_id == user.id


@pytest.mark.django_db
def test_update_task_invalid_status_raises(user):
    task = TaskFactory(created_by=user)
    with pytest.raises(ValueError):
        update_task(task.id, {"status": "bad"}, user=user)


@pytest.mark.django_db
def test_update_task_permission_denied(other_user):
    task = TaskFactory()
    with pytest.raises(TaskPermissionDeniedError):
        update_task(task.id, {"title": "blocked"}, user=other_user)


@pytest.mark.django_db
def test_delete_task_not_found_raises(user):
    with pytest.raises(TaskNotFoundError):
        delete_task(uuid4(), user=user)


@pytest.mark.django_db
def test_complete_task_sets_done(user, other_user):
    task = TaskFactory(created_by=user, assignee=other_user, status=TaskStatus.TODO)
    completed = complete_task(task.id, user=other_user)
    assert completed.status == TaskStatus.DONE


@pytest.mark.django_db
def test_list_tasks_filtered_invalid_status():
    with pytest.raises(ValueError):
        list_tasks_filtered(status="unknown")


@pytest.mark.django_db
def test_comment_update_delete_not_found_and_permission(user, other_user):
    # Not found
    with pytest.raises(CommentNotFoundError):
        update_comment(uuid4(), {"text": "x"}, user=user)
    with pytest.raises(CommentNotFoundError):
        delete_comment(uuid4(), user=user)

    # Permission denied
    comment = TaskFactory(created_by=user).comments.create(author=user, text="hey")
    with pytest.raises(CommentPermissionDeniedError):
        update_comment(comment.id, {"text": "blocked"}, user=other_user)
    with pytest.raises(CommentPermissionDeniedError):
        delete_comment(comment.id, user=other_user)
