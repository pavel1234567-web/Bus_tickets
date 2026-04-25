"""
Middleware for logging requests to debug 500 errors.
"""

import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request
        logger.info(f"Incoming request: {request.method} {request.path}")
        logger.info(f"Content-Type: {request.content_type}")
        
        # Get response
        response = self.get_response(request)
        
        # Log response status
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code >= 500:
            logger.error(f"500 error on {request.method} {request.path}")
            # Log more details for 500 errors
            logger.error(f"Headers: {dict(request.headers)}")
            if hasattr(request, 'body') and request.body:
                logger.error(f"Body: {request.body[:500]}...")  # First 500 chars
        
        return response
