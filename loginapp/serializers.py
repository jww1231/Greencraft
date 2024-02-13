from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'address', 'phone', 'email', 'managercode', 'comcode', 'sex', 'birthdate']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # 비밀번호를 제외한 다른 필드 업데이트
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'address', 'phone', 'email', 'managercode', 'comcode', 'sex', 'birthdate']
        # 'password' 필드는 제외하여 읽기 전용으로 만듭니다.

class GoogleUserSerializer(serializers.Serializer):
    google_id = serializers.CharField()
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, data):
        # Google 토큰 검증
        try:
            # Google API를 사용하여 토큰 검증 (구글 클라이언트 ID 필요)
            idinfo = id_token.verify_oauth2_token(data['token'], requests.Request(), settings.GOOGLE_CLIENT_ID)

            if 'email' not in idinfo or idinfo['email'] != data['email']:
                raise serializers.ValidationError("Google 인증 실패")

        except ValueError:
            # 잘못된 토큰
            raise serializers.ValidationError("잘못된 토큰입니다")

        # 사용자 데이터베이스에 사용자가 존재하는지 확인
        user, created = CustomUser.objects.get_or_create(email=data['email'], defaults={'username': data['google_id']})

        if created:
            # 새로운 사용자 생성 시 필요한 추가 처리 (예: 프로필 정보 설정)
            pass

        return user

    def create(self, validated_data):
        # JWT 토큰 생성 및 반환
        user = validated_data
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
