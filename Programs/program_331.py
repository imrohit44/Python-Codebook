import asyncio
import random
import time

class Server:
    def __init__(self, server_id, num_servers, loop):
        self.id = server_id
        self.num_servers = num_servers
        self.loop = loop
        self.state = 'Follower'
        self.current_term = 0
        self.voted_for = None
        self.election_timeout = random.uniform(5, 10) / 10  # 0.5s to 1.0s
        self.last_heartbeat = time.time()
        self.votes_received = 0
        self.task = loop.create_task(self.run())

    async def run(self):
        while True:
            if self.state == 'Follower':
                if time.time() - self.last_heartbeat > self.election_timeout:
                    print(f"Server {self.id}: Election timeout. Transitioning to Candidate.")
                    self.state = 'Candidate'
                    self.election_timeout = random.uniform(10, 20) / 10  # Reset for new election
                    self.loop.create_task(self.start_election())
            
            elif self.state == 'Leader':
                await self.send_heartbeats()
                await asyncio.sleep(0.1) # Heartbeat interval
            
            await asyncio.sleep(0.01)

    async def start_election(self):
        self.current_term += 1
        self.voted_for = self.id
        self.votes_received = 1
        
        print(f"Server {self.id}: Starting election for Term {self.current_term}.")

        for peer_id in range(self.num_servers):
            if peer_id != self.id:
                self.loop.create_task(self.request_vote(peer_id))

    async def request_vote(self, peer_id):
        # Simulate network delay
        await asyncio.sleep(random.uniform(0.01, 0.1))
        
        # Peer response logic (simplified: always grants vote if term is higher)
        if self.state == 'Candidate':
            is_valid = random.choice([True, False]) # Simplification
            if is_valid:
                self.votes_received += 1
                if self.votes_received > self.num_servers / 2:
                    self.state = 'Leader'
                    print(f"Server {self.id}: Elected LEADER for Term {self.current_term}!")
                    self.loop.create_task(self.send_heartbeats())
            else:
                pass # Handle becoming follower if higher term is seen

    async def send_heartbeats(self):
        if self.state != 'Leader': return
        print(f"Leader {self.id} (T{self.current_term}): Sending heartbeat.")
        # In a real implementation, this would send AppendEntries to all peers

async def main():
    NUM_SERVERS = 5
    loop = asyncio.get_event_loop()
    servers = [Server(i, NUM_SERVERS, loop) for i in range(NUM_SERVERS)]
    
    await asyncio.sleep(5)
    for s in servers:
        s.task