from rest_framework import viewsets
from .serializers import PaperSerializer
from .models import Paper


class PaperViewset(viewsets.ModelViewSet):
    serializer_class = PaperSerializer
    queryset = Paper.objects.all()
    
