from mongoengine import Document, EmailField, StringField, ReferenceField, DateTimeField
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

class MongoUser(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True


class ChatMessage(Document):
    user = ReferenceField(MongoUser, required=True)
    sender = StringField(required=True, choices=["user", "bot"])
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'ordering': ['-timestamp'],  # newest messages first
    }
