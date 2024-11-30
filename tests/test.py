import logging
import random
import time
import threading
from logging_handler import TCPLogHandler

# Configure the logger with the TCPLogHandler
def setup_logger(name, host, port):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the logging level
    tcp_handler = TCPLogHandler(host, port)
    logger.addHandler(tcp_handler)
    return logger

def generate_test_logs(logger, port):
    levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    messages = [
        "System initialized successfully.",
        "Processing user input.",
        "Warning: Low disk space.",
        "Error connecting to database.",
        "Critical: System failure imminent!",
        "Debugging connection issues.",
        "User connected.",
        "User disconnected.",
        "File uploaded successfully.",
        "Scheduled task executed."
    ]

    for _ in range(10):  # Send 10 test log messages
        level = random.choice(levels)
        message = random.choice(messages)
        logger.log(level, f"Port {port}: {message}")
        time.sleep(random.uniform(0.5, 2))  # Random delay between messages

if __name__ == "__main__":
    # Host and ports must match the TCP servers in `master_control.py`
    host = "127.0.0.1"
    ports = [9001, 9002, 9003, 9004, 9005, 9006]

    # Create and configure loggers for each port
    loggers = [setup_logger(f"Logger-{port}", host, port) for port in ports]

    # Generate test logs for each logger in separate threads
    threads = []
    for logger, port in zip(loggers, ports):
        t = threading.Thread(target=generate_test_logs, args=(logger, port))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()
