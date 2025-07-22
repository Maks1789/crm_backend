import logging

logger = logging.getLogger(__name__)


class RequestHeadersLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log all headers
        headers = {key: value for key, value in request.META.items()
                   if key.startswith('HTTP_') or key in ('CONTENT_TYPE', 'CONTENT_LENGTH')}

        logger.debug("Incoming request headers: %s", headers)

        # You could also log specific headers:
        # logger.debug("User-Agent: %s", request.META.get('HTTP_USER_AGENT'))
        # logger.debug("Authorization header: %s", request.META.get('HTTP_AUTHORIZATION'))

        response = self.get_response(request)
        return response