import socket
import threading
import sys
import time

class P2PPeer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.connected_peer_address = None
        self.running = True
        self.message_lock = threading.Lock() # To prevent mixed output from print

    def start_listening(self):
        """Starts listening for incoming connections."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1) # Listen for one incoming connection
            print(f"Listening on {self.host}:{self.port}...")
            
            conn, addr = self.server_socket.accept()
            with self.message_lock:
                print(f"Accepted connection from {addr}")
            self.client_socket = conn
            self.connected_peer_address = addr
            threading.Thread(target=self._receive_messages, daemon=True).start()
        except socket.error as e:
            with self.message_lock:
                print(f"Error starting listener: {e}")
            self.running = False

    def connect_to_peer(self, peer_host, peer_port):
        """Connects to another peer."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer_host, peer_port))
            with self.message_lock:
                print(f"Connected to {peer_host}:{peer_port}")
            self.client_socket = s
            self.connected_peer_address = (peer_host, peer_port)
            threading.Thread(target=self._receive_messages, daemon=True).start()
        except socket.error as e:
            with self.message_lock:
                print(f"Error connecting to {peer_host}:{peer_port}: {e}")
            self.running = False

    def _receive_messages(self):
        """Receives messages from the connected peer."""
        while self.running:
            try:
                if not self.client_socket:
                    time.sleep(0.1) # Wait for connection
                    continue
                
                data = self.client_socket.recv(1024)
                if not data:
                    with self.message_lock:
                        print(f"Peer {self.connected_peer_address} disconnected.")
                    self._close_client_socket()
                    break
                
                message = data.decode('utf-8')
                with self.message_lock:
                    print(f"\n[{self.connected_peer_address[0]}:{self.connected_peer_address[1]}] {message}\n> ", end="")
                    sys.stdout.flush() # Ensure prompt is visible after message
            except (socket.error, ConnectionResetError) as e:
                with self.message_lock:
                    print(f"Error receiving from {self.connected_peer_address}: {e}")
                self._close_client_socket()
                break
            except Exception as e:
                with self.message_lock:
                    print(f"Unexpected error in receiver: {e}")
                self._close_client_socket()
                break
        with self.message_lock:
            print("Receiver thread stopped.")

    def _send_message_loop(self):
        """Allows user to type and send messages."""
        while self.running:
            if not self.client_socket:
                with self.message_lock:
                    print("Not connected to any peer. Waiting for connection...")
                # Wait for connection to be established by listener or connector
                while not self.client_socket and self.running:
                    time.sleep(0.5)
                if not self.running: break # Exit if stopping
                
            try:
                with self.message_lock:
                    message = input("> ")
                if message.lower() == 'exit':
                    self.stop()
                    break
                if self.client_socket:
                    self.client_socket.sendall(message.encode('utf-8'))
            except (socket.error, BrokenPipeError) as e:
                with self.message_lock:
                    print(f"Error sending message: {e}. Peer disconnected?")
                self._close_client_socket()
            except EOFError: # Handles Ctrl+D on Unix-like systems
                self.stop()
                break
            except Exception as e:
                with self.message_lock:
                    print(f"Unexpected error in sender: {e}")
                self.stop()
                break
        with self.message_lock:
            print("Sender thread stopped.")

    def _close_client_socket(self):
        """Helper to close the client socket."""
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
                with self.message_lock:
                    print("Client socket closed.")
            except OSError:
                pass # Socket already closed
            self.client_socket = None
            self.connected_peer_address = None

    def stop(self):
        """Stops the peer and closes all sockets."""
        with self.message_lock:
            print("Shutting down peer...")
        self.running = False
        self._close_client_socket()
        
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
            except OSError:
                pass # Socket might already be closed or not bound
        with self.message_lock:
            print("Peer stopped.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python p2p_chat.py <listen_port> [connect_ip] [connect_port]")
        print("Example (Peer 1): python p2p_chat.py 5000")
        print("Example (Peer 2): python p2p_chat.py 5001 127.0.0.1 5000")
        sys.exit(1)

    my_host = "127.0.0.1" # Use localhost for testing
    my_port = int(sys.argv[1])

    peer = P2PPeer(my_host, my_port)

    listen_thread = threading.Thread(target=peer.start_listening, daemon=True)
    listen_thread.start()

    if len(sys.argv) == 4:
        connect_ip = sys.argv[2]
        connect_port = int(sys.argv[3])
        connect_thread = threading.Thread(target=peer.connect_to_peer, args=(connect_ip, connect_port), daemon=True)
        connect_thread.start()
    else:
        with peer.message_lock:
            print("No connect arguments provided. Will wait for incoming connection.")

    # Start the message sending loop in the main thread
    peer._send_message_loop()

    # Ensure all threads are stopped gracefully before exiting
    if listen_thread.is_alive():
        listen_thread.join(timeout=1) # Give it a chance to finish
    if peer.client_socket_thread and peer.client_socket_thread.is_alive():
        peer.client_socket_thread.join(timeout=1)

if __name__ == "__main__":
    # To test:
    # 1. Open Terminal 1: python your_script_name.py 5000
    # 2. Open Terminal 2: python your_script_name.py 5001 127.0.0.1 5000
    # Now type messages in either terminal.
    main()