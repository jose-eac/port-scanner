import socket
import threading
import argparse
import time
import sys
from queue import Queue

# Thread lock to prevent interleaved console output from multiple threads
print_lock = threading.Lock()

def is_port_open(target: str, port: int, timeout: int = 1) -> bool:
    """
    Attempts to establish a TCP connection to a specific port.

    Args:
        target: The IP address or hostname to scan.
        port: The port number to check.
        timeout: Seconds to wait before giving up on the connection.

    Returns:
        True if the port is open, False otherwise.
    """
    try:
        # Use a context manager to ensure the socket is closed automatically
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            # connect_ex returns 0 on success (port open)
            return s.connect_ex((target, port)) == 0
    except:
        return False
    
def scan(target: str, queue: Queue, verbose: bool) -> None:
    """
    Worker function for threads to pull ports from the queue and scan them.

    Args:
        target: The IP/hostname to scan.
        queue: A thread-safe queue containing port numbers.
        verbose: If True, prints status for closed ports as well.
    """
    while not queue.empty():
        # Retrieve the next port from the queue
        port = queue.get()
        is_open = is_port_open(target, port)

        # Synchronize access to stdout to prevent garbled text
        with print_lock:
            if is_open:
                print(f"[*] Port {port:5} is open")   
            elif verbose:
                print(f"[*] Port {port:5} is closed")

        # Signal to the queue that the task is complete
        queue.task_done()

def main() -> None:
    """
    Parses command-line arguments and manages the thread pool for scanning.
    """
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

    # Populate the queue with the range of ports to scan
    for port in range(args.start, args.end + 1):
        queue.put(port)

    print(f"--- Scanning {target} from port {args.start} to {args.end} ---")
    
    # Launch worker threads
    try:
        for _ in range(args.threads):
            # daemon=True ensures threads exit when the main script does
            t = threading.Thread(target=scan, args=(target, queue, args.verbose))
            t.daemon = True 
            t.start()

        # Block until all items in the queue have been processed
        queue.join()
    except KeyboardInterrupt:
        print("\n[!] User interrupted the scan. Exiting...")
        sys.exit()

    end_time = time.time()
    duration = end_time - start_time
    print(f"--- Scan Completed in {duration:.2f} seconds ---\n")

if __name__ == "__main__":
    main()
