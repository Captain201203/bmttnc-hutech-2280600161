from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

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

client_key = RSA.generate(2048)

server_public_key = RSA.import_key(recv_with_length(client_socket))

send_with_length(client_socket, client_key.publickey().export_key(format='PEM'))

encrypted_aes_key = recv_with_length(client_socket)

cipher_rsa = PKCS1_OAEP.new(client_key)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

def receive_messages():
    while True:
        encrypted_message = recv_with_length(client_socket)
        if not encrypted_message:
            break
        decrypted_message = decrypt_message(aes_key, encrypted_message)
        print(f"Received: {decrypted_message}")

receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    message = input("Enter message ('exit' to quit): ")
    encrypted_message = encrypt_message(message, aes_key)
    send_with_length(client_socket, encrypted_message)
    if message == "exit":
        break

client_socket.close()
