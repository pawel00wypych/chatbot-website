from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from models import MongoUser

class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get("user_id")

        if not user_id:
            raise InvalidToken("Token contained no recognizable user identification")

        user = MongoUser.objects(id=user_id).first()

        if not user:
            raise InvalidToken("User not found")

        return user
