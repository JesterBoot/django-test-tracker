import factory

from tests.users.factories import UserFactory
from workflows.models import Comment, Task
from workflows.models.enums import TaskStatus


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: f"Task {n}")
    description = factory.Faker("sentence")
    status = TaskStatus.TODO
    created_by = factory.SubFactory(UserFactory)
    assignee = None


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    task = factory.SubFactory(TaskFactory)
    author = factory.LazyAttribute(lambda obj: obj.task.created_by)
    text = factory.Sequence(lambda n: f"Comment {n}")
