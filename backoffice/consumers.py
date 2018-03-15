from asgiref.sync import async_to_sync

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
        print("RECEIVE")
        message = ""
        # Subscribe / Unsubscribe to influencers groups
        subscribe = content.get("subscribe")
        unsubscribe = content.get("unsubscribe")

        if subscribe:
            async_to_sync(self.channel_layer.group_add)(
                subscribe,
                self.channel_name
            )
            message += "Subscribed to " + subscribe
        if unsubscribe:
            async_to_sync(self.channel_layer.group_discard)(
                unsubscribe,
                self.channel_name
            )
            message += "Unsubscribed to " + unsubscribe

        self.send_json({
            'message': message
        })

    def influencer_broadcast(self, event):
        print("INFLUENCER BROADCAST")
        self.send_json({
            'message': event.get('text', '')
        })
