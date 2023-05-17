from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenserializer


""" Create new user """
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


""" Update the user """
class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


""" Crate auth token """
class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenserializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES