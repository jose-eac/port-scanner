# Port Scanner (Python)

A simple threaded TCP port scanner implemented in Python. Scans a target host for open ports in a specified range using concurrent worker threads.

## Features

- TCP connect scan (`socket.connect_ex`) for reliable open/closed detection
- Threaded scanning for higher performance
- Configurable port range and thread count
- Optional verbose mode to show closed ports

## Requirements

- Python 3.6+

## Usage

```bash
python3 port-scanner.py <target> [options]
```

### Positional argument

- `target`: target hostname or IP address (e.g. `127.0.0.1`, `localhost`)

### Optional arguments

- `-s`, `--start`: start port (default `1`)
- `-e`, `--end`: end port (default `1024`)
- `-t`, `--threads`: number of worker threads (default `100`)
- `-v`, `--verbose`: include closed ports in output

## Examples

Scan common ports on localhost:

```bash
python3 port-scanner.py 127.0.0.1
```

Scan a custom range with fewer threads:

```bash
python3 port-scanner.py 192.168.1.10 -s 1 -e 500 -t 50
```

Scan and show both open and closed ports:

```bash
python3 port-scanner.py example.com -v
```

## Notes

- Requires network reachability to target host
- Large ranges and high thread counts can generate heavy network traffic and consume CPU
- Run with appropriate authorization
