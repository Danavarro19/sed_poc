from server import Server

server = Server()


def app(environ, start_response):
    return server.handle_request(environ, start_response)
