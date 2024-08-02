import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UploadConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling image upload notifications.

    This consumer manages WebSocket connections for the image upload process,
    allowing real-time communication between the server and clients.

    Attributes:
        group_name (str): The name of the channel group for broadcast messages.
    """

    async def connect(self):
        """
        Handle new WebSocket connection.

        This method is called when a new WebSocket connection is established.
        It adds the connection to the 'upload_group' and sends a connection confirmation.
        """
        self.group_name = 'upload_group'
        # Join upload group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'You are connected!',
            'status': 'ok'
        }))

    async def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        This method is called when a WebSocket connection is closed.
        It removes the connection from the 'upload_group'.

        Args:
            close_code (int): The code indicating why the connection was closed.
        """
        # Leave upload group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages.

        This method processes messages received from the client and echoes them back.

        Args:
            text_data (str): The JSON-encoded message from the client.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    async def send_upload_notification(self, event):
        """
        Send upload notifications to the client.

        This method is called to send status updates about image uploads to the client.

        Args:
            event (dict): A dictionary containing notification details.
        """
        data = {
            'name': event['name'],
            'size': event['size'],
            'job_id': event['job_id'],
            'status': event['status'],
            'message': event['message'],
            'type': event['type'],
        }
        
        if 'image' in event and event['image']:
            data['image'] = event['image']
        if 'upload_time' in event and event['upload_time']:
            data['upload_time'] = event['upload_time']
       
        await self.send(text_data=json.dumps(data))
