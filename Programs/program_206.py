import socket
import threading
import concurrent.futures
import time

def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        if not data:
            return
        
        request = data.decode('utf-8')
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(request)}\r\n\r\n{request}"
        conn.sendall(response.encode('utf-8'))
    except Exception:
        pass
    finally:
        conn.close()

def start_server(host, port, max_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen()
            print(f"Server listening on {host}:{port}")
            while True:
                conn, addr = sock.accept()
                executor.submit(handle_client, conn, addr)

if __name__ == '__main__':
    start_server('127.0.0.1', 8080, max_workers=5)