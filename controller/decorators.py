from functools import wraps

from server.response import Response


def requires_authentication(handler):
    @wraps(handler)
    def wrapper(request, *args, **kwargs):
        if request.user is None:
            return Response.redirect('/signin')
        return handler(request, *args, **kwargs)
    return wrapper


def validate_csrf(handler):
    @wraps(handler)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return handler(request, *args, **kwargs)

        csrf_token = None
        if request.form_data:
            csrf_token = request.form_data.pop('csrf_token', None)

        if not csrf_token or csrf_token != request.session.csrf_token:
            return Response.unauthorized(request)
        return handler(request, *args, **kwargs)

    return wrapper
