
class Request:
    def __init__(self, environ):
        self.environ = environ
        self.method = environ.get('REQUEST_METHOD', 'GET')
        self.path = environ.get('PATH_INFO', '/')
        self.query_string = environ.get('QUERY_STRING', '')
        self.headers = self._get_headers()
        self.content_length = int(environ.get('CONTENT_LENGTH', 0))
        self.body = self._get_body()
        self.remote_addr = environ.get('REMOTE_ADDR', '')
        self.scheme = environ.get('wsgi.url_scheme', 'http')
        self.content_type = environ.get('CONTENT_TYPE', '')

    def _get_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith('HTTP_'):
                header_name = key[5:].replace('_', '-').title()
                headers[header_name] = value
        return headers

    def _get_body(self):
        if self.content_length > 0:
            return self.environ['wsgi.input'].read(self.content_length)
        return b''

    @property
    def form_data(self):
        from urllib.parse import parse_qs
        data = parse_qs(self.body.decode('utf-8'))

        for field, value in data.items():
            if len(value) == 1:
                # noinspection PyTypeChecker
                data[field] = value[0]

        return data
