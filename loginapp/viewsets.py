from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView
from .models import CustomUser
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import GoogleUserSerializer
from django.http import JsonResponse
from .models import CustomUser
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'username': str(username),
                'is_superuser': user.is_superuser,
                'is_staff': user.is_superuser,
                'managercode': user.managercode,

            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # 현재 로그인한 사용자 반환
        return self.request.user


class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GoogleUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


