import asyncio
import uuid
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class Request:
    def __init__(self, reader, writer, session_id=None):
        self.reader = reader
        self.writer = writer
        self.session_id = session_id
        self.method = None
        self.path = None
        self.headers = {}
        self.body = None
        self.session = {}

class SessionStore:
    def __init__(self):
        self.sessions = {}
        self.lock = asyncio.Lock()

    async def get_session(self, session_id):
        async with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {}
            return self.sessions[session_id]

    async def create_session(self):
        async with self.lock:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {}
            return session_id

    async def clear_expired(self):
        async with self.lock:
            expired_ids = [sid for sid, session in self.sessions.items() if time.time() - session.get('last_access', 0) > 3600]
            for sid in expired_ids:
                del self.sessions[sid]

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.routes = {}
        self.session_store = SessionStore()

    def route(self, path):
        def decorator(handler):
            self.routes[path] = handler
            return handler
        return decorator

    async def handle_request(self, reader, writer):
        request = Request(reader, writer)
        raw_request = (await reader.read(8192)).decode('utf-8')
        if not raw_request:
            writer.close()
            return
        
        lines = raw_request.split('\r\n')
        request_line = lines[0].split()
        request.method = request_line[0]
        request.path = urlparse(request_line[1]).path
        
        headers = dict(line.split(": ", 1) for line in lines[1:] if ": " in line)
        request.headers = headers
        
        session_id = None
        if 'Cookie' in headers:
            cookies = parse_qs(headers['Cookie'].replace('; ', '&'))
            if 'session_id' in cookies:
                session_id = cookies['session_id'][0]

        if not session_id:
            session_id = await self.session_store.create_session()
        
        request.session_id = session_id
        request.session = await self.session_store.get_session(session_id)
        request.session['last_access'] = time.time()

        if request.path in self.routes:
            handler = self.routes[request.path]
            response = await handler(request)
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"
        
        writer.write(response.encode('utf-8'))
        writer.write(f"Set-Cookie: session_id={request.session_id}\r\n".encode('utf-8'))
        await writer.drain()
        writer.close()

    async def start(self):
        server = await asyncio.start_server(self.handle_request, self.host, self.port)
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = Server('127.0.0.1', 8080)
    
    @server.route('/')
    async def index_handler(request):
        visits = request.session.get('visits', 0) + 1
        request.session['visits'] = visits
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, you have visited this page {visits} times."

    asyncio.run(server.start())