from rest_framework import serializers
from .models import Paper


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ('id', 'title', 'abstract')