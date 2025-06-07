from models import MongoUser, ChatMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from mongo_JWT_authentication import MongoJWTAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)

        if MongoUser.objects(email=email).first():
            return Response({"error": "Email already registered"}, status=400)

        user = MongoUser(email=email)
        user.set_password(password)
        user.save()

        return Response({
            "message": "User registered successfully",
            "user_id": str(user.id),
            "email": user.email
        }, status=201)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = MongoUser.objects(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken()
            access = AccessToken()

            # Manually embed your user's identity
            refresh["user_id"] = str(user.id)
            refresh["email"] = user.email
            access["user_id"] = str(user.id)
            access["email"] = user.email

            return Response({
                "access": str(access),
                "refresh": str(refresh),
                "email": user.email
            })

        return Response({"error": "Invalid credentials"}, status=401)


class ChatHistory(APIView):
    authentication_classes = [MongoJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        messages = ChatMessage.objects(user=user).order_by('-timestamp')[:100]
        messages_data = [
            {"sender": msg.sender, "text": msg.text}
            for msg in reversed(messages)
        ]
        return Response(messages_data)
