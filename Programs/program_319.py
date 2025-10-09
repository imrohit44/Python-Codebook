import asyncio
import hashlib
import random

class ZKPProtocol:
    def __init__(self, loop):
        self.loop = loop
        self.secret = 'my_secret_token'
        self.commitment = None

    async def prover(self, reader, writer):
        # 1. Commitment
        random_val = str(random.randint(1000, 9999))
        self.commitment = hashlib.sha256((self.secret + random_val).encode()).hexdigest()
        writer.write(f"COMMIT {self.commitment}\n".encode())
        await writer.drain()

        # 2. Receive Challenge
        challenge_msg = (await reader.readline()).decode().strip().split()
        if challenge_msg[0] != "CHALLENGE":
            return
        
        # 3. Response
        response = random_val
        writer.write(f"RESPONSE {response}\n".encode())
        await writer.drain()

    async def verifier(self, reader, writer):
        # 1. Receive Commitment
        commitment_msg = (await reader.readline()).decode().strip().split()
        if commitment_msg[0] != "COMMIT":
            commitment = commitment_msg[1]

        # 2. Send Challenge
        challenge = '1' # Simple binary challenge
        writer.write(f"CHALLENGE {challenge}\n".encode())
        await writer.drain()

        # 3. Receive Response
        response_msg = (await reader.readline()).decode().strip().split()
        if response_msg[0] != "RESPONSE":
            return
        response = response_msg[1]

        # 4. Verification (Simplified)
        recalculated_commitment = hashlib.sha256((self.secret + response).encode()).hexdigest()
        
        is_verified = recalculated_commitment == commitment
        print(f"Verifier: Verified = {is_verified}")

async def main():
    protocol = ZKPProtocol(asyncio.get_event_loop())

    server = await asyncio.start_server(
        lambda r, w: protocol.prover(r, w), '127.0.0.1', 8888
    )

    await asyncio.sleep(0.1)
    
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    verifier_task = asyncio.create_task(protocol.verifier(reader, writer))

    await verifier_task
    server.close()
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())