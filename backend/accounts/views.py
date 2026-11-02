from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

from .models import User
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user