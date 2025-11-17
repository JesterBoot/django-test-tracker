from uuid import UUID

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflows.api.serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)
from workflows.exceptions.task_exceptions import (
    TaskNotFoundError,
)
from workflows.selectors.task_selectors import (
    get_task_by_id,
    list_tasks_filtered,
)
from workflows.services.task_services import (
    create_task,
    delete_task,
    update_task,
)


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Tasks"],
        summary="Получить список задач",
        parameters=[
            OpenApiParameter(
                name="status",
                type=str,
                description="Фильтр по статусу задачи (todo / in_progress / done)",
                required=False,
            ),
            OpenApiParameter(
                name="assignee_id",
                type=str,
                description="Фильтр по ID исполнителя",
                required=False,
            ),
        ],
        responses={
            200: TaskListSerializer,
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    )
    def get(self, request):
        status_param = request.query_params.get("status")
        assignee_param = request.query_params.get("assignee_id")

        tasks = list_tasks_filtered(
            status=status_param,
            assignee_id=UUID(assignee_param) if assignee_param else None,
        )

        data = TaskListSerializer(tasks, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="tasks_create",
        tags=["Tasks"],
        summary="Создать новую задачу",
        request=TaskCreateSerializer,
        responses={
            201: TaskDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Недостаточно прав"),
        },
    )
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = create_task(serializer.validated_data, user=request.user)

        response = TaskDetailSerializer(task).data
        return Response(response, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="tasks_retrieve",
        tags=["Tasks"],
        summary="Получить задачу по ID",
        responses={
            200: TaskDetailSerializer,
            404: OpenApiResponse(description="Задача не найдена"),
        },
    )
    def get(self, request, task_id: UUID):
        task = get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError("Задача не найдена.")

        data = TaskDetailSerializer(task).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id="tasks_update",
        tags=["Tasks"],
        summary="Обновить существующую задачу",
        request=TaskUpdateSerializer,
        responses={
            200: TaskDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Недостаточно прав"),
            404: OpenApiResponse(description="Задача не найдена"),
        },
    )
    def patch(self, request, task_id: UUID):
        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = update_task(task_id, serializer.validated_data, user=request.user)
        return Response(TaskDetailSerializer(task).data)

    @extend_schema(
        operation_id="tasks_delete",
        tags=["Tasks"],
        summary="Удалить задачу",
        responses={
            204: OpenApiResponse(description="Успешное удаление"),
            403: OpenApiResponse(description="Недостаточно прав"),
            404: OpenApiResponse(description="Задача не найдена"),
        },
    )
    def delete(self, request, task_id: UUID):
        delete_task(task_id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
