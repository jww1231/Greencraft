from rest_framework import viewsets
from .models import BusinessCode
from .serializers import BusinessCodeSerializer

class BusinessCodeViewSet(viewsets.ModelViewSet):
    queryset = BusinessCode.objects.all()
    serializer_class = BusinessCodeSerializer
