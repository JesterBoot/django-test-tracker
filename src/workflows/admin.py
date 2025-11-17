from django.contrib import admin

from workflows.models import Comment, Task


class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = "task"
    extra = 0

    fields = (
        "author_email",
        "text",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "author_email",
        "created_at",
        "updated_at",
    )

    def author_email(self, obj):
        return obj.author.email if obj.author else "—"

    author_email.short_description = "Автор"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "created_by_email",
        "assignee_email",
        "created_at",
    )
    list_filter = ("status", "assignee")
    search_fields = ("title", "description")
    ordering = ("-created_at",)

    inlines = [CommentInline]

    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("created_by", "assignee")

    def created_by_email(self, obj):
        return obj.created_by.email if obj.created_by else "—"

    created_by_email.short_description = "Создатель"

    def assignee_email(self, obj):
        return obj.assignee.email if obj.assignee else "—"

    assignee_email.short_description = "Исполнитель"
