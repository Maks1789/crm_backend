import logging

logger = logging.getLogger(__name__)


class RequestHeadersLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        headers = {
            key: value for key, value in request.META.items()
            if key.startswith('HTTP_') or key in ('CONTENT_TYPE', 'CONTENT_LENGTH')
        }

        # 🔍 Основні заголовки
        logger.critical("📥 Request Headers: %s", headers)
        logger.critical("📨 Method: %s | Path: %s", request.method, request.path)

        # 🔐 Користувач
        user = getattr(request, 'user', None)
        logger.critical("👤 User: %s | Authenticated: %s", user, user.is_authenticated if user else None)

        # 🍪 Cookies
        logger.critical("🍪 Cookies: %s", request.COOKIES)

        try:
            logger.critical("🔐 Session: %s", dict(request.session.items()))
        except Exception as e:
            logger.warning("⚠️ Session read error: %s", e)

        # 🧾 POST тіло без конфлікту
        if request.method == "POST":
            try:
                body = request.body.decode("utf-8")
                logger.critical("📦 Raw Body: %s", body)
            except Exception as e:
                logger.warning("⚠️ Body read error: %s", e)

        elif request.method == "GET":
            logger.critical("🔍 GET params: %s", request.GET)

        # 🚀 Передати далі
        return self.get_response(request)
