from rest_framework import generics
from .models import ImageWithText
from .serializers import ImageWithTextSerializer

class ImageWithTextCreateView(generics.CreateAPIView):
    queryset = ImageWithText.objects.all()
    serializer_class = ImageWithTextSerializer
