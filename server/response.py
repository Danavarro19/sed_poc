from http.cookies import SimpleCookie

from view.template import render_template


class Response:
    def __init__(self, body='', status='200 OK', headers=None):
        self.body = body
        self.status = status
        self.headers = headers or [('Content-Type', 'text/html; charset=utf-8')]
        self.cookies = SimpleCookie()

    def set_header(self, name, value):
        self.headers.append((name, value))

    def set_cookie(self, key, value, **kwargs):
        self.cookies[key] = value
        for k, v in kwargs.items():
            self.cookies[key][k] = v

    def delete_cookie(self, key):
        self.set_cookie(key, '', expires='Thu, 01 Jan 1970 00:00:00 GMT')

    @classmethod
    def redirect(cls, location, status='302 Found'):
        response = cls(body='', status=status)
        response.set_header('Location', location)
        return response

    @classmethod
    def not_found(cls, request):
        context = {'user': request.user}
        return cls(body=render_template('not_found.html', context=context), status='404 Not Found')

    @classmethod
    def unauthorized(cls, request):
        context = {'user': request.user}
        return cls(body=render_template('unauthorized.html', context=context), status='401 Unauthorized')

    @classmethod
    def render(cls, request, *, template_name, context=None):
        if context is None:
            context = {'user': request.user, 'session': request.session }
        else:
            context['user'] = request.user
            context['session'] = request.session
        return cls(body=render_template(template_name, context=context))

    def wsgi_response(self, start_response):
        for morsel in self.cookies.values():
            self.set_header('Set-Cookie', morsel.OutputString())

        start_response(self.status, self.headers)
        if isinstance(self.body, str):
            return [self.body.encode('utf-8')]
        elif isinstance(self.body, bytes):
            return [self.body]
        else:
            return [b'Invalid response type']
