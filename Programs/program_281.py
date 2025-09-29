import asyncio
import socket
import random
import struct

DNS_SERVER = '8.8.8.8' 
DNS_PORT = 53
TIMEOUT = 5

def build_query(domain):
    query_id = random.getrandbits(16)
    
    header = struct.pack("!HHHHHH", query_id, 0x0100, 1, 0, 0, 0)
    
    qname = b''
    for part in domain.split('.'):
        qname += struct.pack("!B", len(part)) + part.encode('utf-8')
    qname += b'\x00'
    
    qtype = struct.pack("!H", 1)
    qclass = struct.pack("!H", 1)
    
    return header + qname + qtype + qclass

async def resolve_domain(domain):
    query = build_query(domain)
    
    transport, protocol = await asyncio.get_event_loop().create_datagram_endpoint(
        lambda: DNSProtocol(), remote_addr=(DNS_SERVER, DNS_PORT)
    )
    
    protocol.send(query)
    
    try:
        response = await asyncio.wait_for(protocol.response_future, TIMEOUT)
        
        if len(response) < 12:
            return "Error: Short response"
        
        header = struct.unpack("!HHHHHH", response[:12])
        an_count = header[3]
        
        offset = len(query)
        
        # Skip question section and find answers
        
        return f"A records found: {an_count}"
        
    except asyncio.TimeoutError:
        return "Timeout"
    finally:
        transport.close()

class DNSProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.response_future = asyncio.get_event_loop().create_future()
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if not self.response_future.done():
            self.response_future.set_result(data)

    def send(self, data):
        self.transport.sendto(data)

if __name__ == '__main__':
    async def main_resolver():
        result = await resolve_domain("google.com")
        print(f"Result for google.com: {result}")

    asyncio.run(main_resolver())