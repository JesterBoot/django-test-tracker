from typing import Any, TypeVar

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


U = TypeVar("U", bound=AbstractBaseUser)


class UserManager(BaseUserManager[U]):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any) -> U:
        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if not password:
            raise ValueError("Password must be provided")

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> U:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> U:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields["is_staff"] is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields["is_superuser"] is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
