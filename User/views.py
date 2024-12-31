from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, extend_schema_view

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаём нового пользователя
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={},
        responses={200: UserSerializer},
    )
    def get(self, request):
        user = request.user  # Получаем текущего аутентифицированного пользователя
        return Response({
            "nickname": user.nickname,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer},
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)

        return Response({"message" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        responses={204: {"message": "User deleted successfully"}},
    )
    def delete(self, request):
        user = request.user  # Получаем текущего пользователя
        user.delete()  # Удаляем пользователя из базы данных
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)