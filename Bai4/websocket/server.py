import random
import tornado.web
import tornado.websocket
import tornado.ioloop

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()
    
    def open(self):
        WebSocketServer.clients.add(self)
        
    def on_close(self):
        WebSocketServer.clients.remove(self)
        
    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message {message} to {len(cls.clients)} client(s)")
        for client in cls.clients:
            client.write_message(message)
    
    def check_origin(self, origin):
        return True  # Cho phép mọi origin, chỉ dùng cho demo/dev

class RandomWorldSelector:
    def __init__(self, word_list):
        self.word_list = word_list
        
    def sample(self):
        return random.choice(self.word_list)
        
def main():
    app = tornado.web.Application([
        (r"/websocket", WebSocketServer),
    ])
    
    app.listen(8888)
    
    io_loop = tornado.ioloop.IOLoop.current()
    
    word_selector = RandomWorldSelector(["apple", "banana", "orange", "grape", "kiwi"])

    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()),
        3000  # Gửi tin nhắn mỗi 3 giây
    )    
    periodic_callback.start()
    
    io_loop.start()

if __name__ == "__main__":
    main()
