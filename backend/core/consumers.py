import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import os
import google.generativeai as genai
from models import ChatMessage

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY is not set!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")
        if self.user is None or not self.user.is_authenticated:
            await self.close()
        else:
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

            await save_message(self.user, "user", user_msg)

            # Run blocking Gemini API in executor
            loop = asyncio.get_event_loop()
            try:
                result = await asyncio.wait_for(
                    loop.run_in_executor(None, lambda: model.generate_content(user_msg, stream=True)),
                    timeout=200
                )
            except asyncio.TimeoutError:
                await self.send(text_data=json.dumps({
                    "error": "Model took too long to respond. Try again later."
                }))
                return

            text_chunks = []
            for chunk in result:
                if chunk.text:
                    text_chunks.append(chunk.text)

            bot_response = "".join(text_chunks)
            await save_message(self.user, "bot", bot_response)

            await self.send(text_data=json.dumps({"message": bot_response}))

        except Exception as e:
            await self.send(text_data=json.dumps({"error": f"Error: {str(e)}"}))

async def save_message(user, sender, text):

    from asgiref.sync import sync_to_async

    @sync_to_async
    def _save():
        ChatMessage(user=user, sender=sender, text=text).save()
        count = ChatMessage.objects(user=user).count()
        if count > 100:
            old_msgs = ChatMessage.objects(user=user).order_by('timestamp')[:count - 100]
            for msg in old_msgs:
                msg.delete()
    await _save()