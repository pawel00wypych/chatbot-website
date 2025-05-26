from mongoengine import Document, EmailField, StringField
from django.contrib.auth.hashers import make_password, check_password

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
