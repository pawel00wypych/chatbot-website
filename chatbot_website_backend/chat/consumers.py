import json
from channels.generic.websocket import AsyncWebsocketConsumer
from transformers import pipeline
import asyncio

# download pipeline once (outside the class so its not reloaded each time
model = pipeline("text2text-generation", model="google/flan-t5-small")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected with chatbot!"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user_msg = data.get("message")

            if not user_msg:
                await self.send(text_data=json.dumps({"error": "Empty message"}))
                return

            loop = asyncio.get_event_loop()

            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(
                        None,
                        lambda: model(user_msg, max_length=100, num_return_sequences=1)
                    ),
                    timeout=200
                )
            except asyncio.TimeoutError:
                await self.send(text_data=json.dumps({
                    "error": "Model took too long to respond. Try again later."
                }))
                return

            print(result)
            bot_response = result[0]['generated_text']

            await self.send(text_data=json.dumps({
                "message": bot_response
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": f"Error message: {str(e)}"
            }))