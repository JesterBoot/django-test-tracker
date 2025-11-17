from uuid import UUID

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from workflows.api.serializers import (
    CommentCreateSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
    CommentUpdateSerializer,
)
from workflows.exceptions.comment_exceptions import (
    CommentNotFoundError,
)
from workflows.selectors.comment_selectors import (
    get_comment_by_id,
    list_comments_for_task,
)
from workflows.services.comment_services import (
    create_comment,
    delete_comment,
    update_comment,
)


class CommentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="comments_list",
        tags=["Comments"],
        summary="Получить список комментариев к задаче",
        responses={
            200: CommentListSerializer,
            404: OpenApiResponse(description="Задача не найдена"),
        },
    )
    def get(self, reqeust, task_id: UUID):
        comments = list_comments_for_task(task_id)
        data = CommentListSerializer(comments, many=True).data
        return Response(data)

    @extend_schema(
        operation_id="comments_create",
        tags=["Comments"],
        summary="Создать комментарий к задаче",
        request=CommentCreateSerializer,
        responses={
            201: CommentDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Задача не найдена"),
        },
    )
    def post(self, request, task_id: UUID):
        payload = {**request.data, "task_id": task_id}

        serializer = CommentCreateSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        comment = create_comment(serializer.validated_data, user=request.user)

        return Response(CommentDetailSerializer(comment).data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="comments_retrieve",
        tags=["Comments"],
        summary="Получить комментарий по ID",
        responses={
            200: CommentDetailSerializer,
            404: OpenApiResponse(description="Комментарий не найден"),
        },
    )
    def get(self, request, comment_id: UUID):
        comment = get_comment_by_id(comment_id)
        if comment is None:
            raise CommentNotFoundError("Комментарий не найден.")
        return Response(CommentDetailSerializer(comment).data)

    @extend_schema(
        operation_id="comments_update",
        tags=["Comments"],
        summary="Обновить комментарий",
        request=CommentUpdateSerializer,
        responses={
            200: CommentDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            403: OpenApiResponse(description="Недостаточно прав"),
            404: OpenApiResponse(description="Комментарий не найден"),
        },
    )
    def patch(self, request, comment_id: UUID):
        serializer = CommentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = update_comment(comment_id, serializer.validated_data, user=request.user)
        return Response(CommentDetailSerializer(comment).data)

    @extend_schema(
        operation_id="comments_delete",
        tags=["Comments"],
        summary="Удалить комментарий",
        responses={
            204: OpenApiResponse(description="Успешное удаление"),
            403: OpenApiResponse(description="Недостаточно прав"),
            404: OpenApiResponse(description="Комментарий не найден"),
        },
    )
    def delete(self, request, comment_id: UUID):
        delete_comment(comment_id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
