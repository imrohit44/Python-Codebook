import socket

def get_http_response(host, port, path="/"):
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )
    
    with socket.create_connection((host, port), timeout=5) as sock:
        sock.sendall(request.encode())
        
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            
        header_end = response.find(b'\r\n\r\n')
        headers_raw = response[:header_end].decode()
        body = response[header_end + 4:].decode()
        
        headers = {}
        header_lines = headers_raw.split('\r\n')
        status_line = header_lines[0].split()
        
        for line in header_lines[1:]:
            if ':' in line:
                key, value = line.split(': ', 1)
                headers[key.strip()] = value.strip()

        return {
            'status': status_line[1],
            'status_text': status_line[2],
            'headers': headers,
            'body_length': len(body),
            'body_start': body[:100]
        }

if __name__ == '__main__':
    response_data = get_http_response('example.com', 80)
    print(f"Status: {response_data['status']} {response_data['status_text']}")
    print(f"Content-Length: {response_data['headers'].get('Content-Length')}")
    print(f"Body snippet: {response_data['body_start']}...")