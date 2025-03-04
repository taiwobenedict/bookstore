import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class StoreConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "orders"

        # Join the group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(
            text_data=json.dumps({
                "type": "connection_established",
                "message": "You are now connected"
            })
        )

    def disconnect(self, close_code):
        # Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        order_id = data.get("order_id")
        status = data.get("status")

        # Broadcast order update
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "order_status_update",
                "order_id": order_id,
                "status": status,
            }
        )

    def order_status_update(self, event):
        # Send updated status to WebSocket clients
        self.send(text_data=json.dumps({
            "order_id": event["order_id"],
            "status": event["status"]
        }))
