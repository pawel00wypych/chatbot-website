import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


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
                        lambda: model.generate_content(user_msg,
                                                  stream=True)
                    ),
                    timeout=200
                )
            except asyncio.TimeoutError:
                await self.send(text_data=json.dumps({
                    "error": "Model took too long to respond. Try again later."
                }))
                return

            print(result)
            text_chunks = []
            for chunk in result:
                if chunk.text:
                    text_chunks.append(chunk.text)

            bot_response = "".join(text_chunks)

            await self.send(text_data=json.dumps({
                "message": bot_response
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": f"Error message: {str(e)}"
            }))