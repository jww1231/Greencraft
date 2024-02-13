from django.urls import path
from .views import ImageWithTextCreateView

urlpatterns = [
    path('image-with-text/', ImageWithTextCreateView.as_view(), name='image-with-text'),
    # Add other URLs if needed
]
