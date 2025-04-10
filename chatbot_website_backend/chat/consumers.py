import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected with chatbot!"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data.get("message")

        # GPT-2 / DeepSeek
        bot_response = f"Response for: {user_msg}"

        await self.send(text_data=json.dumps({
            "message": bot_response
        }))