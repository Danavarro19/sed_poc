class Response:
    def __init__(self, body='', status='200 OK', headers=None):
        self.body = body
        self.status = status
        self.headers = headers or [('Content-Type', 'text/html; charset=utf-8')]

    def set_header(self, name, value):
        self.headers.append((name, value))

    @classmethod
    def redirect(cls, location, status='302 Found'):
        response = cls(body='', status=status)
        response.set_header('Location', location)
        return response

    def wsgi_response(self, start_response):
        start_response(self.status, self.headers)
        if isinstance(self.body, str):
            return [self.body.encode('utf-8')]
        elif isinstance(self.body, bytes):
            return [self.body]
        else:
            return [b'Invalid response type']