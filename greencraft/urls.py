"""
URL configuration for greencraft project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loginapp.viewsets import MyModelViewSet  # loginapp에서 뷰를 직접 임포트
from loginapp.viewsets import LoginAPIView
from loginapp.viewsets import GoogleLoginView
from loginapp.viewsets import CurrentUserProfileView  # UserProfileView 임포트
from use_model.views import ImageProcessView
from django.conf import settings
from django.conf.urls.static import static
from manager.views import BusinessCodeViewSet
from car.views import CarViewSet


router = DefaultRouter()
router.register(r'users', MyModelViewSet)
router.register(r'businesscodes', BusinessCodeViewSet, basename='businesscode')  # BusinessCode 뷰셋을 router에 등록
router.register(r'cars', CarViewSet, basename='car')

urlpatterns = [
    path('admin/', admin.site.urls),  # 관리자 페이지 경로 추가
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),  # 사용자 프로필 조회 경로 추가
    path('api/process-image/', ImageProcessView.as_view(), name='process_image'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('api/', include('raspi.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # 정적 파일 URL 패턴 설정

# 개발환경에서 미디어 파일을 서빙하기 위한 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)