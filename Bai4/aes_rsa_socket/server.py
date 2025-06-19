from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Server đang chạy và lắng nghe kết nối...")

server_key = RSA.generate(2048)

clients = []
client_lock = threading.Lock()

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

def handle_client(client_socket, client_address):
    print(f"Kết nối được thiết lập với {client_address}")
    try:
        # Gửi public key của server cho client
        send_with_length(client_socket, server_key.publickey().export_key(format='PEM'))

        # Nhận public key từ client
        client_received_key = RSA.import_key(recv_with_length(client_socket))

        # Tạo AES key và mã hóa bằng public key của client
        aes_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(client_received_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        send_with_length(client_socket, encrypted_aes_key)

        with client_lock:
            clients.append((client_socket, aes_key))

        while True:
            encrypted_message = recv_with_length(client_socket)
            if not encrypted_message:
                break

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Nhận từ {client_address}: {decrypted_message}")

            # Chuyển tiếp tin nhắn cho các client khác
            with client_lock:
                for other_client_socket, other_aes_key in list(clients):
                    if other_client_socket != client_socket:
                        try:
                            encrypted_broadcast_message = encrypt_message(decrypted_message, other_aes_key)
                            send_with_length(other_client_socket, encrypted_broadcast_message)
                        except Exception as broadcast_e:
                            print(f"Lỗi khi gửi tin nhắn cho client {other_client_socket.getpeername()}: {broadcast_e}")

            if decrypted_message == "exit":
                break

    except Exception as e:
        print(f"Lỗi xử lý client {client_address}: {e}")
    finally:
        with client_lock:
            for i, (sock, k) in enumerate(clients):
                if sock == client_socket:
                    clients.pop(i)
                    break
        client_socket.close()
        print(f"Kết nối với {client_address} đã đóng")

while True:
    try:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()
    except Exception as e:
        print(f"Lỗi chấp nhận kết nối: {e}")
        break