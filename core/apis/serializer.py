from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from core.models import Blogs, CustomUser, Project


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email')

    def create(self, data):
        try:    
            username = data['username']
            email = data['email']
            password = data['password']
            hashedpassword = make_password(password) 
            user= CustomUser.objects.create(
                username = username,
                email = email,
                password = hashedpassword
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        
class ProjectGetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')
        
class BlogsGetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id', 'image', 'title', 'description', 'project', 'category', 'updated_at')

class BlogsRetrievePatchSerializer(serializers.ModelSerializer):
    # project = ProjectGetPostSerializer()
    project = serializers.SerializerMethodField()
    class Meta:
        model = Blogs
        fields = ('id', 'image', 'title', 'description','project', 'category')

    def get_project(self, obj):
        return obj.project.name