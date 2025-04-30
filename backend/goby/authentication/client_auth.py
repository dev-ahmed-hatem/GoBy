from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from clients.models import Client
from rest_framework.exceptions import AuthenticationFailed


class ClientJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = JWTAuthentication()
        try:
            header = request.headers.get('Authorization')
            if not header:
                raise exceptions.AuthenticationFailed()
            raw_token = auth.get_raw_token(request.headers.get('Authorization').encode())

            validated_token = auth.get_validated_token(raw_token)
            client_id = validated_token.get('client_id')

            if not client_id:
                raise exceptions.AuthenticationFailed("Invalid token payload.")

            try:
                client = Client.objects.get(id=client_id)
                return client, validated_token
            except Client.DoesNotExist:
                raise exceptions.AuthenticationFailed("Client not found.")

        except AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(f"Authentication error: {str(e)}")

        # except Exception as e:
        #     raise exceptions.AuthenticationFailed(f"Invalid Token")
