import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
import os

class DHClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DH Key Exchange Client")
        self.window.geometry("700x500")

        self.private_key = int.from_bytes(os.urandom(32), byteorder='big')
        self.public_key = None
        self.shared_key = None

        self.setup_gui()

    def setup_gui(self):
        # Thông tin khóa
        info_frame = tk.LabelFrame(self.window, text="Thông tin khóa", padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(info_frame, text="Khóa bí mật (b):").grid(row=0, column=0, sticky='w')
        self.private_label = tk.Label(info_frame, text=str(self.private_key))
        self.private_label.grid(row=0, column=1, sticky='w')

        tk.Label(info_frame, text="Khóa công khai (B = g^b mod p):").grid(row=1, column=0, sticky='w')
        self.public_label = tk.Label(info_frame, text="Chưa tạo")
        self.public_label.grid(row=1, column=1, sticky='w')

        tk.Label(info_frame, text="Khóa chung (K = A^b mod p):").grid(row=2, column=0, sticky='w')
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
        tk.Button(btn_frame, text="Kết nối Server", command=self.connect_to_server).pack(side=tk.LEFT, padx=5)

    def add_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def connect_to_server(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 12345))

            g = 2
            p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF

            # Gửi g và p cho server
            client_socket.send(str(g).encode())
            client_socket.send(str(p).encode())

            # Tính B = g^b mod p
            B = pow(g, self.private_key, p)
            self.public_key = B
            self.public_label.config(text=str(B))

            # Nhận A từ server
            A = int(client_socket.recv(4096).decode())

            # Gửi B cho server
            client_socket.send(str(B).encode())

            # Tính khóa chung K = A^b mod p
            K = pow(A, self.private_key, p)
            self.shared_key = K
            self.shared_label.config(text=str(K))

            self.add_log("Kết nối thành công!")
            self.add_log(f"Khóa chung với server: {K}")

            client_socket.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối đến server: {str(e)}")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = DHClientGUI()
    gui.run()