from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import MyTokenObtainPairSerializer, UserSerializer


# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    """Token view"""

    serializer_class = MyTokenObtainPairSerializer

@method_decorator(name='list', decorator=swagger_auto_schema(
            operation_description="Retrieve a list of all User instances.",
            operation_summary="Get all Users"
        ))

@method_decorator(name='create', decorator=swagger_auto_schema(
            operation_description="Create User instance.",
            operation_summary="Register User"
        ))

@method_decorator(name='retrieve', decorator=swagger_auto_schema(
            operation_description="View User instance.",
            operation_summary="View User by id"
        ))

@method_decorator(name='update', decorator=swagger_auto_schema(
            operation_description="Update User instance.",
            operation_summary="Update User by id"
        ))

@method_decorator(name='partial_update', decorator=swagger_auto_schema(
            operation_description="Update some fields of User instance.",
            operation_summary="Update User attributes by id"
        ))

@method_decorator(name='destroy', decorator=swagger_auto_schema(
            operation_description="Delete User instance.",
            operation_summary="Delete User by id"
        ))

class UserViewSet(viewsets.ModelViewSet):
    """User REST"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class TestView(APIView):
    """Subscribe to course"""
    def post(self, request):
        return Response(
            {
                "message": "message",
                "payment_url": "session.url",
                "session_id": "session.id",
            }
        )
