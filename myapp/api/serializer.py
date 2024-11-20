from rest_framework import serializers

from core.models import Blogs

class BlogviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id', 'project', 'category', 'image', 'title', 'description')