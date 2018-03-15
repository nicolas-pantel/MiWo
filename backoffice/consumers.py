from channels.generic.websocket import JsonWebsocketConsumer


class DemoConsumer(JsonWebsocketConsumer):
    counter = 0

    def connect(self):
        print("CONNECT")
        self.accept()

    def disconnect(self, close_code):
        print("DISCONNECT")
        pass

    def receive_json(self, content):
        message = content['message']
        self.counter += 1
        print(message, self.counter)
        self.send_json({
            'message': message + " " + str(self.counter)
        })
