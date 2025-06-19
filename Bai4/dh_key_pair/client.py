import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
import hashlib
import os

class DHClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DH Key Exchange Client")
        self.window.geometry("600x400")
        
        # Tạo giao diện
        self.create_widgets()
        
        # Kết nối đến server
        self.connect_to_server()
        
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.window)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Khu vực hiển thị log
        self.log_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)
        
        # Frame thông tin
        info_frame = tk.Frame(main_frame)
        info_frame.pack(padx=5, pady=5, fill=tk.X)
        
        # Label hiển thị khóa
        self.private_key = int.from_bytes(os.urandom(32), byteorder='big')
        self.key_label = tk.Label(info_frame, text="Khóa bí mật: " + str(self.private_key))
        self.key_label.pack(side=tk.LEFT, padx=5)
        
        # Nút kết nối lại
        reconnect_button = tk.Button(info_frame, text="Kết nối lại", command=self.connect_to_server)
        reconnect_button.pack(side=tk.RIGHT, padx=5)
        
    def add_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))
            
            # Chọn g và p
            g = 2
            p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
            
            # Gửi g và p cho server
            self.client_socket.send(str(g).encode())
            self.client_socket.send(str(p).encode())
            
            # Tính b = g^a mod p
            b = pow(g, self.private_key, p)
            
            # Nhận A từ server
            A = int(self.client_socket.recv(1024).decode())
            
            # Gửi B cho server
            self.client_socket.send(str(b).encode())
            
            # Tính khóa chung K = A^a mod p
            K = pow(A, self.private_key, p)
            
            self.add_log(f"Kết nối thành công!")
            self.add_log(f"Khóa chung K = {K}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối đến server: {str(e)}")
            
    def run(self):
        self.window.mainloop()
        
if __name__ == "__main__":
    client = DHClient()
    client.run()