import re


class Router:
    def __init__(self):
        self.routes = {}
        self.param_routes = []

    def add_route(self, path, handler):
        if '<' in path and '>' in path:
            param_pattern = re.sub(r'<(\w+)>', r'(?P<\1>\\w+)', path)
            param_pattern = f'^{param_pattern}$'
            self.param_routes.append((re.compile(param_pattern), handler))
        else:
            self.routes[path] = handler

    def get_handler(self, path):
        if path in self.routes:
            return self.routes[path], None

        for pattern, handler in self.param_routes:
            match = pattern.match(path)
            if match:
                return handler, match.groupdict()

        return None, None

