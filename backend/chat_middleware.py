from urllib.parse import parse_qs


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth.models import AnonymousUser
        from models import MongoUser


        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token.get("user_id")
                if user_id:
                    user = MongoUser.objects.get(id=user_id)
                    scope["user"] = user
                else:
                    scope["user"] = AnonymousUser()
            except Exception as e:
                print(f"[WS AUTH ERROR] {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
