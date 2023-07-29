"""
MIDDLEWARES
"""

async def add_request_id_header(request, response):
    """Adds req id header

    Args:
        request (Request): Sanic request object
        response (Response): Sanic response object
    """
    response.headers["X-Request-ID"] = request.id