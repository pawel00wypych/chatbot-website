import json
from channels.generic.websocket import AsyncWebsocketConsumer
import httpx

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected with chatbot!"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data.get("message")

        # Send prompt to vLLM running on port 9000
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:9000/v1/completions",
                json={
                    "model": "gpt2",
                    "prompt": user_msg,
                    "max_tokens": 50,
                },
                timeout=60.0
            )

        if response.status_code == 200:
            result = response.json()
            bot_response = result["choices"][0]["text"].strip()
        else:
            bot_response = "Oops! GPT-2 didn't respond."

        await self.send(text_data=json.dumps({
            "message": bot_response
        }))