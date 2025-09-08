import asyncio
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

class Request:
    def __init__(self, method, path, headers):
        self.method = method
        self.path = path
        self.headers = headers
        self.response = None

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routes = {}
        self.middleware_pipeline = []

    def use(self, middleware):
        self.middleware_pipeline.append(middleware)

    def route(self, path):
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator

    async def _handle_request(self, reader, writer):
        raw_request = (await reader.read(8192)).decode('utf-8')
        if not raw_request:
            writer.close()
            return
        
        request_line = raw_request.split('\r\n')[0].split()
        method, path = request_line[0], urlparse(request_line[1]).path
        headers = {line.split(': ')[0]: line.split(': ')[1] for line in raw_request.split('\r\n')[1:] if ': ' in line}
        
        request = Request(method, path, headers)
        
        for middleware in self.middleware_pipeline:
            await middleware(request)
            if request.response:
                break
        
        if not request.response:
            if path in self.routes:
                await self.routes[path](request)
            else:
                request.response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"
        
        writer.write(request.response.encode('utf-8'))
        await writer.drain()
        writer.close()

    async def start(self):
        server = await asyncio.start_server(self._handle_request, self.host, self.port)
        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    server = Server('127.0.0.1', 8080)

    async def logger_middleware(request):
        print(f"[{time.time()}] Request for {request.path}")
    
    async def auth_middleware(request):
        if 'Authorization' not in request.headers:
            request.response = "HTTP/1.1 401 Unauthorized\r\n\r\nUnauthorized"

    server.use(logger_middleware)
    server.use(auth_middleware)

    @server.route('/data')
    async def data_handler(request):
        request.response = "HTTP/1.1 200 OK\r\n\r\nData received."
        
    asyncio.run(server.start())