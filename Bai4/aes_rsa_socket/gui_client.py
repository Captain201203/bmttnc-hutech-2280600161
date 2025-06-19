from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import struct
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

def send_with_length(sock, data):
    sock.sendall(struct.pack('>I', len(data)) + data)

def recv_with_length(sock):
    raw_len = recvall(sock, 4)
    if not raw_len:
        return None
    msg_len = struct.unpack('>I', raw_len)[0]
    return recvall(sock, msg_len)

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("AES-RSA Socket Chat Client")
        self.text_area = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.entry = tk.Entry(master, width=50)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.send_btn = tk.Button(master, text="Gửi", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=(5,10), pady=(0,10))
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(('localhost', 12345))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không kết nối được tới server: {e}")
            master.destroy()
            return

        self.client_key = RSA.generate(2048)
        self.server_public_key = RSA.import_key(recv_with_length(self.client_socket))
        send_with_length(self.client_socket, self.client_key.publickey().export_key(format='PEM'))
        encrypted_aes_key = recv_with_length(self.client_socket)
        cipher_rsa = PKCS1_OAEP.new(self.client_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def encrypt_message(self, message):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_message.decode()

    def send_message(self):
        message = self.entry.get()
        if not message:
            return
        encrypted_message = self.encrypt_message(message)
        send_with_length(self.client_socket, encrypted_message)
        self.append_message(f"Bạn: {message}")
        self.entry.delete(0, tk.END)
        if message == "exit":
            self.on_close()

    def receive_messages(self):
        while self.running:
            try:
                encrypted_message = recv_with_length(self.client_socket)
                if not encrypted_message:
                    break
                decrypted_message = self.decrypt_message(encrypted_message)
                self.append_message(f"Khách: {decrypted_message}")
            except Exception:
                break

    def append_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def on_close(self):
        self.running = False
        try:
            self.client_socket.close()
        except:
            pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()