import logging
import json

logger = logging.getLogger("django.request")

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log Request
        try:
            body = request.body.decode('utf-8')
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        except Exception:
            body = None

        logger.info(f"Request: {request.method} {request.get_full_path()}")
        response = self.get_response(request)

        # Log Response
        try:
            response_body = getattr(response, 'data', response.content.decode('utf-8'))
        except Exception:
            response_body = 'Could not decode response body'

        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Body: {response_body}")

        return response
