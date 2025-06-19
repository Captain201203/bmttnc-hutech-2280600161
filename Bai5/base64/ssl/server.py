import socket
import ssl
import threading

server_address = ('localhost', 12345)

clients = []

def handle_client(client_socket):
    clients.append(client_socket)
    
    print(f"Đã kết nối với: {client_socket.getpeername()}")
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            print(f"Nhận dữ liệu: {data.decode('utf-8')}")
            
            for client in clients:
                if client != client_socket:
                    try:
                        client.send(data)
                        
                    except:
                        clients.remove(client)
    
    except:
        clients.remove(client_socket)
        
    finally:
        print(f"Đóng kết nối với: {client_socket.getpeername()}")
        clients.remove(client_socket)
        client_socket.close()
        
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print(f"Server đang chờ kết nối...")

while True:
    client_socket, clent_address = server_socket.accept()
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='./certificates/server-cert.crt', keyfile='./certificates/server-key.key')
    
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    
    client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
    client_thread.start()
