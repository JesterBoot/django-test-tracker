from collections.abc import Iterable

from users.models import User


def select_users(q: str | None, limit: int, *, exclude_user_id) -> Iterable[User]:
    qs = (
        User.objects.only("id", "email")
        .filter(is_active=True)
        .exclude(id=exclude_user_id)
        .order_by("email")
    )

    if q:
        qs = qs.filter(email__icontains=q)

    return qs[:limit]
