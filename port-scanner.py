import socket
import threading
import argparse
import time
import sys
from queue import Queue

print_lock = threading.Lock()

def is_port_open(target, port, timeout = 1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((target, port)) == 0
    except:
        return False
    
def scan(target, queue, verbose):
    while not queue.empty():
        port = queue.get()
        is_open = is_port_open(target, port)

        with print_lock:
            if is_open:
                print(f"[*] Port {port:5} is open")   
            elif verbose:
                print(f"[*] Port {port:5} is closed")
        queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="A simple threaded port scanner.")
    parser.add_argument("target", help="The IP or hostname to scan (e.g. , 127.0.0.1)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Starting port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Ending port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show closed ports")

    args = parser.parse_args()

    print(f"\n--- Starting Scan on {args.target} ---")
    start_time = time.time()

    target = args.target
    queue = Queue()

    for port in range(args.start, args.end + 1):
        queue.put(port)

    print(f"--- Scanning {target} from port {args.start} to {args.end} ---")

    # Thread Management
    try:
        for _ in range(args.threads):
            t = threading.Thread(target=scan, args=(target, queue, args.verbose))
            t.daemon = True 
            t.start()
    
        queue.join()
    except KeyboardInterrupt:
        sys.exit()

    end_time = time.time()
    duration = end_time - start_time
    print(f"--- Scan Completed in {duration:.2f} seconds ---\n")

if __name__ == "__main__":
    main()
