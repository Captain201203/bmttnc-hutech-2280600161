import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import os

class DHServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DH Key Exchange Server")
        self.window.geometry("700x500")

        # Khóa bí mật
        self.private_key = int.from_bytes(os.urandom(32), byteorder='big')
        self.public_key = None
        self.shared_key = None

        self.setup_gui()
        self.server_socket = None
        self.listen_thread = None

    def setup_gui(self):
        # Thông tin khóa
        info_frame = tk.LabelFrame(self.window, text="Thông tin khóa", padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(info_frame, text="Khóa bí mật (a):").grid(row=0, column=0, sticky='w')
        self.private_label = tk.Label(info_frame, text=str(self.private_key))
        self.private_label.grid(row=0, column=1, sticky='w')

        tk.Label(info_frame, text="Khóa công khai (A = g^a mod p):").grid(row=1, column=0, sticky='w')
        self.public_label = tk.Label(info_frame, text="Chưa tạo")
        self.public_label.grid(row=1, column=1, sticky='w')

        tk.Label(info_frame, text="Khóa chung (K = B^a mod p):").grid(row=2, column=0, sticky='w')
        self.shared_label = tk.Label(info_frame, text="Chưa tạo")
        self.shared_label.grid(row=2, column=1, sticky='w')

        # Log
        log_frame = tk.LabelFrame(self.window, text="Log", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)

        # Nút điều khiển
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="Khởi động Server", command=self.start_server).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Dừng Server", command=self.stop_server).pack(side=tk.LEFT, padx=5)

    def add_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_server(self):
        if self.server_socket:
            self.add_log("Server đã chạy.")
            return
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        self.add_log("Server đang chạy và lắng nghe kết nối...")
        self.listen_thread = threading.Thread(target=self.listen_for_connections, daemon=True)
        self.listen_thread.start()

    def stop_server(self):
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
            self.add_log("Server đã dừng.")
        self.window.destroy()

    def handle_client(self, client_socket, client_address):
        try:
            self.add_log(f"Kết nối mới từ {client_address}")

            # Nhận g và p từ client
            g = int(client_socket.recv(4096).decode())
            p = int(client_socket.recv(4096).decode())

            # Tính A = g^a mod p
            A = pow(g, self.private_key, p)
            self.public_key = A
            self.public_label.config(text=str(A))
            client_socket.send(str(A).encode())

            # Nhận B từ client
            B = int(client_socket.recv(4096).decode())

            # Tính khóa chung K = B^a mod p
            K = pow(B, self.private_key, p)
            self.shared_key = K
            self.shared_label.config(text=str(K))
            self.add_log(f"Khóa chung với {client_address}: {K}")

        except Exception as e:
            self.add_log(f"Lỗi với client {client_address}: {str(e)}")
        finally:
            client_socket.close()
            self.add_log(f"Đóng kết nối với {client_address}")

    def listen_for_connections(self):
        while self.server_socket:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
            except:
                break

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = DHServerGUI()
    gui.run()