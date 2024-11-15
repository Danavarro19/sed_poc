from url import urls
from pprint import pprint

from .request import Request
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

        if handler:
            status = '200 OK'
            headers = [('Content-type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            try:
                if kwargs:
                    response = handler(request, **kwargs)
                else:
                    response = handler(request)
            except TypeError:
                response = handler(request)
            if isinstance(response, str):
                return [response.encode('utf-8')]
            else:
                return [b'Invalid response type']
        else:
            status = '404 Not Found'
            headers = [('Content-type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            return [b'404 Not Found']






