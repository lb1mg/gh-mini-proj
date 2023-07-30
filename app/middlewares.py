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


# TODO: Add Helmet like security headers
# TODO: Add header info in 1-line comments


async def add_security_headers(request, response):
    """Adds security related headers

    Args:
        request (Request): Sanic request object
        response (Response): Sanic response object
    """
    
    # CSP header, can be too strict...
    # response.headers['Content-Security-Policy'] = "default-src 'self'; img-src *; style-src *; font-src https://themes.googleusercontent.com"
    # legacy header, prevents clickjacking
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    # contros Referer request header
    response.headers["Referrer-Policy"] = "no-referrer"
    # 'mitigates MIME-type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # disabling, buggy
    response.headers['X-XSS-Protection'] = '0'
