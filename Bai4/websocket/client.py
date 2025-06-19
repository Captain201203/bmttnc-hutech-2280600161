import tornado.websocket
import tornado.ioloop

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        
    def start(self):
        self.connect_and_read()
        
    def stop(self):
        self.io_loop.stop()
        
    def connect_and_read(self):
        print("Connecting to WebSocket server...")
        future = tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket"
        )
        future.add_done_callback(self.on_connection_open)
        
    def on_connection_open(self, future):
        try:
            self.connection = future.result()
            print("Connected to server.")
            self.read_message()
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            self.io_loop.call_later(5, self.connect_and_read)
        
    def read_message(self):
        self.connection.read_message(callback=self.on_message)
        
    def on_message(self, message):
        if message is None:
            print("Disconnected from server, reconnecting...")
            self.connect_and_read()
            return
        print(f"Received message: {message}")
        self.read_message()
        
def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()
    
if __name__ == "__main__":
    main()