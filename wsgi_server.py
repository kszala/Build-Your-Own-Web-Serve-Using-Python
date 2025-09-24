import io
import socket
import sys

SERVER_ADDRESS = (HOST, PORT) = '', 8888

class WSGIServer(object):
    # ----------------------
    # Server setup
    # ----------------------
    def __init__(self, server_address):
        self.listen_socket = listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_address)
        listen_socket.listen(1)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []  # <-- Where we'll store status + headers from the app

    # ----------------------
    # Set which application/framework we are serving
    # ----------------------
    def set_app(self, application):
        self.application = application

    # ----------------------
    # Main server loop: Accept client connections
    # ----------------------
    def serve_forever(self):
        while True:
            # Step 1: Client request comes in
            self.client_connection, client_address = self.listen_socket.accept()
            # Step 2: Handle request (talk to WSGI app)
            self.handle_one_request()

    # ----------------------
    # Handle a single HTTP request
    # ----------------------
    def handle_one_request(self):
        # Read raw bytes from client
        request_data = self.client_connection.recv(1024)
        if not request_data:
            self.client_connection.close()
            return

        # Decode bytes to string
        self.request_data = request_data = request_data.decode('utf-8')

        # Optional: print request for debugging
        print(''.join(f'< {line}\n' for line in request_data.splitlines()))

        # Parse request line (GET /path HTTP/1.1)
        self.parse_request(request_data)

        # Step 3: Prepare environ dictionary
        env = self.get_environ()  # <-- WSGI environ sent to application

        # Step 4: Call the WSGI application
        result = self.application(env, self.start_response)

        # Step 5: Send back the HTTP response
        self.finish_response(result)

    # ----------------------
    # Parse request line (simplified)
    # ----------------------
    def parse_request(self, request_data):
        request_line = request_data.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        self.request_method, self.path, self.request_version = request_line.split()

    # ----------------------
    # Create the WSGI environ dictionary
    # ----------------------
    def get_environ(self):
        env = {}
        env['wsgi.version'] = (1,0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)  # Raw request body
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = self.server_name
        env['SERVER_PORT'] = str(self.server_port)
        return env  # <-- Passed to application

    # ----------------------
    # This is the WSGI callable the server gives the app to send status + headers
    # ----------------------
    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', 'Mon, 15 Jul 2019 5:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        # Store what the app gave us (server will use this later)
        self.headers_set = [status, response_headers + server_headers]

    # ----------------------
    # Finish response: combine status, headers, body → send to client
    # ----------------------
    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set

            # Build HTTP response
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += f'{header[0]}: {header[1]}\r\n'
            response += '\r\n'

            # Append response body (iterable returned by WSGI app)
            for data in result:
                response += data.decode('utf-8')

            # Debug print
            print(''.join(f'> {line}\n' for line in response.splitlines()))

            # Send bytes back to client
            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()  # Close connection after response

def make_server(server_address,application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exist('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module,application = app_path.split(':')
    module = __import__(module)
    application = getattr(module,application)
    httpd = make_server(SERVER_ADDRESS,application)
    print(f'Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()
