import socket
import threading
import queue
import time

HOST = "127.0.0.1"
PORT = 5000
NUM_WORKERS = 3
NUM_CLIENTS = 5


class Worker(threading.Thread):
    def __init__(self, name, q):
        super().__init__(name=name)
        self.q = q

    def run(self):
        while True:
            item = self.q.get() 
            try:
                if item is None:  
                    print(f"[{self.name}] menerima sentinel, berhenti")
                    break

                conn, addr = item
                print(f"[{self.name}] memproses client {addr}")
                data = conn.recv(1024).decode()
                time.sleep(1) 
                reply = f"{self.name}: {data.upper()}"
                conn.sendall(reply.encode())
                conn.close()
            finally:
                self.q.task_done()


def main():
    q = queue.Queue()

    workers = [Worker(f"Worker-{i}", q) for i in range(1, NUM_WORKERS + 1)]
    for w in workers:
        w.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server berjalan di {HOST}:{PORT}")

    for _ in range(NUM_CLIENTS):
        conn, addr = server.accept()
        print(f"[Main] koneksi dari {addr} dimasukkan ke queue")
        q.put((conn, addr))
    for _ in workers:
        q.put(None)

    q.join()
    for w in workers:
        w.join()

    server.close()
    print("Semua koneksi selesai diproses, server berhenti")


if __name__ == "__main__":
    main()