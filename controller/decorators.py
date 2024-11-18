from functools import wraps

from server.response import Response


def requires_authentication(handler):
    @wraps(handler)
    def wrapper(request, *args, **kwargs):
        if request.user is None:
            return Response.redirect('/signin')
        return handler(request, *args, **kwargs)
    return wrapper
