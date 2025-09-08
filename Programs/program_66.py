import threading
import time
import random
import queue
import socket
import json

class Node:
    def __init__(self, node_id, port, peers):
        self.node_id = node_id
        self.port = port
        self.peers = peers
        self.state = {}
        self.is_leader = False
        self.leader_id = None
        self.running = True
        self.message_queue = queue.Queue()
        self.lock = threading.Lock()
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', self.port))
        
        self.leader_timeout = random.uniform(2, 4)
        self.last_heartbeat = time.time()
        
    def _send_message(self, target_port, msg):
        try:
            self.socket.sendto(json.dumps(msg).encode(), ('127.0.0.1', target_port))
        except Exception:
            pass

    def _broadcast(self, msg):
        for port in self.peers:
            if port != self.port:
                self._send_message(port, msg)

    def _listen(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                msg = json.loads(data.decode())
                self.message_queue.put(msg)
            except Exception:
                pass

    def _handle_messages(self):
        while self.running:
            try:
                msg = self.message_queue.get(timeout=0.1)
                
                if msg['type'] == 'heartbeat' and msg['leader_id'] == self.leader_id:
                    self.last_heartbeat = time.time()
                    
                if msg['type'] == 'vote_request':
                    self._send_message(msg['sender_port'], {'type': 'vote', 'candidate_id': msg['candidate_id']})
                
                if self.is_leader and msg['type'] == 'client_command':
                    self._replicate_command(msg)

                self.message_queue.task_done()
            except queue.Empty:
                continue

    def _elect_leader(self):
        print(f"Node {self.node_id}: Starting election...")
        self.is_leader = False
        self.leader_id = None
        self.last_heartbeat = time.time()
        
        votes = 1
        candidate_id = self.node_id
        
        self._broadcast({'type': 'vote_request', 'candidate_id': candidate_id, 'sender_port': self.port})
        
        election_end_time = time.time() + 2
        
        while time.time() < election_end_time:
            try:
                msg = self.message_queue.get(timeout=0.1)
                if msg['type'] == 'vote' and msg['candidate_id'] == candidate_id:
                    votes += 1
                self.message_queue.task_done()
            except queue.Empty:
                continue
        
        if votes > len(self.peers) / 2:
            self.is_leader = True
            self.leader_id = self.node_id
            self._broadcast({'type': 'leader_announce', 'leader_id': self.node_id})
            print(f"Node {self.node_id}: Elected as leader!")
        else:
            print(f"Node {self.node_id}: Election failed. Becoming a follower.")
            
    def _replicate_command(self, cmd):
        with self.lock:
            self.state[cmd['key']] = cmd['value']
            print(f"Node {self.node_id}: Executed command '{cmd['key']}={cmd['value']}'")
            self._broadcast({'type': 'replicate', 'key': cmd['key'], 'value': cmd['value']})

    def run(self):
        listener_thread = threading.Thread(target=self._listen)
        listener_thread.daemon = True
        listener_thread.start()
        
        handler_thread = threading.Thread(target=self._handle_messages)
        handler_thread.daemon = True
        handler_thread.start()
        
        time.sleep(random.uniform(0, 1))
        
        while self.running:
            if not self.is_leader and time.time() - self.last_heartbeat > self.leader_timeout:
                self._elect_leader()
            
            if self.is_leader:
                self._broadcast({'type': 'heartbeat', 'leader_id': self.node_id})
                time.sleep(1)
            else:
                time.sleep(0.5)

def client_command(leader_port, key, value):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = {'type': 'client_command', 'key': key, 'value': value}
    sock.sendto(json.dumps(msg).encode(), ('127.0.0.1', leader_port))
    sock.close()

if __name__ == "__main__":
    peers = [8001, 8002, 8003]
    nodes = [Node(i+1, peers[i], peers) for i in range(3)]
    threads = [threading.Thread(target=node.run) for node in nodes]
    
    for t in threads:
        t.start()
        
    time.sleep(10)
    
    leader_port = nodes[0].port if nodes[0].is_leader else nodes[1].port if nodes[1].is_leader else nodes[2].port
    
    client_command(leader_port, 'user', 'Alice')
    time.sleep(1)
    client_command(leader_port, 'score', 100)
    
    time.sleep(5)
    
    for node in nodes:
        print(f"Node {node.node_id} state: {node.state}")