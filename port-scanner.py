import socket
import threading
import argparse
from queue import Queue

def scan(target, queue):
    while not queue.empty():
        port = queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((target, port)) == 0:
                print(f"[*] Port {port} is open")
            s.close()
        except:
            pass
        finally:
            queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="A simple threaded port scanner.")
    parser.add_argument("target", help="The IP or hostname to scan (e.g. , 127.0.0.1)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Starting port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Ending port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")

    args = parser.parse_args()

    target = args.target
    queue = Queue()

    for port in range(args.start, args.end + 1):
        queue.put(port)

    print(f"--- Scanning {target} from port {args.start} to {args.end} ---")

    for _ in range(args.threads):
        t = threading.Thread(target=scan, args=(target, queue))
        t.daemon = True 
        t.start()

    queue.join()
    print("--- Scan Complete ---")

if __name__ == "__main__":
    main()