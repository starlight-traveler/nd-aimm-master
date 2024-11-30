# logging_handler.py
import logging
import socket
import json
from datetime import datetime

class TCPLogHandler(logging.Handler):
    def __init__(self, host, port):
        super().__init__()
        self.server_address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.server_address)
        except Exception as e:
            print(f"Failed to connect to log server {host}:{port} - {e}")
            self.sock = None

    def emit(self, record):
        if self.sock:
            try:
                log_entry = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'logger': record.name,
                    'level': record.levelname,
                    'message': record.getMessage()
                }
                message = json.dumps(log_entry) + '\n'  # Add newline as delimiter
                self.sock.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send log message: {e}")

    def close(self):
        if self.sock:
            self.sock.close()
        super().close()
