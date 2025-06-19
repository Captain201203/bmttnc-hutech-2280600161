from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import dh
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import hashlib
import os

def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters


def generate_server_keys_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

class DHServer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("DH Key Exchange Server")
        self.window.geometry("600x400")
        
        # Khởi tạo server
        self.setup_server()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Khởi động thread lắng nghe
        self.listen_thread = threading.Thread(target=self.listen_for_connections)
        self.listen_thread.daemon = True
        self.listen_thread.start()
        
    def setup_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 12345))
        self.server_socket.listen(5)
        
        # Tạo khóa bí mật
        self.private_key = int.from_bytes(os.urandom(32), byteorder='big')
        
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
        self.key_label = tk.Label(info_frame, text="Khóa bí mật: " + str(self.private_key))
        self.key_label.pack(side=tk.LEFT, padx=5)
        
        # Nút dừng server
        stop_button = tk.Button(info_frame, text="Dừng Server", command=self.stop_server)
        stop_button.pack(side=tk.RIGHT, padx=5)
        
    def add_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
        
    def handle_client(self, client_socket, client_address):
        try:
            self.add_log(f"Kết nối mới từ {client_address}")
            
            # Nhận g và p từ client
            g = int(client_socket.recv(1024).decode())
            p = int(client_socket.recv(1024).decode())
            
            # Tính A = g^a mod p
            A = pow(g, self.private_key, p)
            
            # Gửi A cho client
            client_socket.send(str(A).encode())
            
            # Nhận B từ client
            B = int(client_socket.recv(1024).decode())
            
            # Tính khóa chung K = B^a mod p
            K = pow(B, self.private_key, p)
            
            self.add_log(f"Khóa chung K = {K}")
            
        except Exception as e:
            self.add_log(f"Lỗi với client {client_address}: {str(e)}")
        finally:
            client_socket.close()
            self.add_log(f"Đóng kết nối với {client_address}")
            
    def listen_for_connections(self):
        self.add_log("Server đang chạy và lắng nghe kết nối...")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
            except:
                break
                
    def stop_server(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn dừng server?"):
            self.server_socket.close()
            self.window.destroy()
            
    def run(self):
        self.window.mainloop()
        
if __name__ == "__main__":
    server = DHServer()
    server.run()



















