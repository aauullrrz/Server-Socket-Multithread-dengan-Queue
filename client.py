import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

MESSAGES = [
    "halo dari client satu",
    "ini client kedua",
    "sekarang giliran client tiga",
    "aku client empat",
    "pesan terakhir dari client lima",
]


def run_client(client_id, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(message.encode())
    reply = s.recv(1024).decode()
    print(f"[Client-{client_id}] kirim: '{message}' | balasan: '{reply}'")
    s.close()


def main():
    threads = []
    for i, msg in enumerate(MESSAGES, start=1):
        t = threading.Thread(target=run_client, args=(i, msg))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()