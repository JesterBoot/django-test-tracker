import pytest

from users.models import User


@pytest.mark.django_db
def test_create_user_missing_email():
    manager = User.objects
    with pytest.raises(ValueError):
        manager.create_user(email="", password="123")


@pytest.mark.django_db
def test_create_user_missing_password():
    manager = User.objects
    with pytest.raises(ValueError):
        manager.create_user(email="a@b.com", password=None)


@pytest.mark.django_db
def test_create_superuser_invalid_flags():
    # is_staff must be True
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com",
            password="123",
            is_staff=False,
            is_superuser=True,
        )

    # is_superuser must be True
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com",
            password="123",
            is_staff=True,
            is_superuser=False,
        )


@pytest.mark.django_db
def test_create_superuser_success():
    manager = User.objects
    user = manager.create_superuser(
        email="admin@example.com",
        password="123",
    )
    assert user.is_superuser
    assert user.is_staff
