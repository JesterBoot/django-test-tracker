import os
import socket
import time


host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", "5432"))

print(f"Waiting for PostgreSQL at {host}:{port}...", flush=True)

for i in range(1800):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)
            sock.connect((host, port))
        print("PostgreSQL is available.", flush=True)
        break
    except OSError:
        time.sleep(0.1)
else:
    raise TimeoutError("PostgreSQL connection timeout")
