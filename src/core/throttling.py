import logging

from rest_framework.throttling import SimpleRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


logger = logging.getLogger(__name__)


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        # по IP, т.к. пользователь еще не авторизован
        ip = self.get_ident(request)
        return f"throttle_login_{ip}"


class RefreshTokenRateThrottle(SimpleRateThrottle):
    scope = "refresh"

    def get_cache_key(self, request, view) -> str | None:
        """
        Ограничение по user_id. Если refresh-токен невалидный или сломан -
        отключается throttling для этого запроса.
        """
        user_id = None

        if request.data and "refresh" in request.data:
            raw_refresh = request.data.get("refresh")

            try:
                token = RefreshToken(raw_refresh)
                user_id = token.get("user_id")
            except TokenError as exc:
                logger.warning("Refresh token parsing failed: %s", exc)
                return None
            except Exception as exc:
                logger.error("Unexpected error parsing refresh token: %s", exc)
                return None

        if not user_id:
            return None

        return f"throttle_refresh_{user_id}"
