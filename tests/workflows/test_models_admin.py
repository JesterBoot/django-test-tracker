import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from tests.users.factories import UserFactory
from tests.workflows.factories import CommentFactory, TaskFactory
from workflows.admin import CommentInline, TaskAdmin
from workflows.models import Task


class DummySite(AdminSite):
    pass


@pytest.mark.django_db
def test_task_str_and_comment_str():
    task = TaskFactory(title="Read", status="todo")
    comment = CommentFactory(task=task, text="Note")

    assert str(task) == "Read (todo)"
    assert "Комментарий от" in str(comment)


@pytest.mark.django_db
def test_admin_helpers_and_queryset():
    request = RequestFactory().get("/")
    task = TaskFactory(assignee=UserFactory())

    admin_obj = TaskAdmin(Task, DummySite())
    qs = admin_obj.get_queryset(request)
    assert "created_by" in qs.query.select_related
    assert "assignee" in qs.query.select_related

    assert admin_obj.created_by_email(task) == task.created_by.email
    assert admin_obj.assignee_email(task) == task.assignee.email

    inline = CommentInline(Task, DummySite())
    comment = CommentFactory(task=task)
    assert inline.author_email(comment) == comment.author.email
