from models import MongoUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny


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

