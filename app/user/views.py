from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    '''create a new user in the system'''
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    '''Create a new token for user'''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    '''manage the authenticated user'''
    serializer_class = UserSerializer
    # authentication and permission using token authentication and level of permissions

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    # get object function to our API view

    def get_object(self):
        '''retrieve and returns authenticated user'''
        return self.request.user



