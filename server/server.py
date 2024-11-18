from service.user import validate_session
from url import urls
from pprint import pprint

from .request import Request
from .response import Response
from .router import Router


class Server:
    def __init__(self):
        self.router = Router()

        for path, handler in urls:
            self.router.add_route(path, handler)

    def add_route(self, path, handler):
        self.router.add_route(path, handler)

    def handle_request(self, environ, start_response):
        pprint(environ)
        request = Request(environ)
        handler, kwargs = self.router.get_handler(request.path)

        if request.is_authenticated:
            request.set_user(validate_session(request.get_cookie("session_token")))

        if handler:
            try:
                if kwargs:
                    response = handler(request, **kwargs)
                else:
                    response = handler(request)
            except TypeError:
                response = handler(request)

            if isinstance(response, Response):
                return response.wsgi_response(start_response)
            elif isinstance(response, str):
                response_obj = Response(body=response)
                return response_obj.wsgi_response(start_response)
            else:
                # Handle unexpected response types
                error_response = Response(body='500 Internal Server Error', status='500 Internal Server Error')
                return error_response.wsgi_response(start_response)
        else:
            not_found_response = Response(body='404 Not Found', status='404 Not Found')
            return not_found_response.wsgi_response(start_response)






