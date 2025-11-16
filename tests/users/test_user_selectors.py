import pytest

from users.selectors.user_selectors import get_user_by_email


@pytest.mark.django_db
def test_get_user_by_email_not_found():
    user = get_user_by_email("missing@example.com")
    assert user is None
