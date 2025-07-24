"""
Networking utilities for PyPacman Multiplayer
"""

import socket
import json
import time
from typing import Optional, Dict, Any


def get_local_ip() -> str:
    """Get the local IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'


def send_message(sock: socket.socket, message: Dict[str, Any]) -> bool:
    """Send a JSON message to a socket"""
    try:
        message_str = json.dumps(message)
        sock.send(message_str.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False


def receive_message(sock: socket.socket) -> Optional[Dict[str, Any]]:
    """Receive a JSON message from a socket"""
    try:
        data = sock.recv(2048).decode('utf-8')
        if not data:
            return None
        return json.loads(data)
    except Exception as e:
        print(f"Failed to receive message: {e}")
        return None


def wait_for_server_start(server_instance, timeout: float = 5.0) -> bool:
    """Wait for a server to start up"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            port = server_instance.get_port()
            if port is not None:
                return True
        except:
            pass
        time.sleep(0.1)
    
    return False


def test_connection(host: str, port: int, timeout: float = 3.0) -> bool:
    """Test if a connection can be made to a host:port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False
