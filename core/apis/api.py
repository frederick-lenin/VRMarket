from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError as JWTTokenError
from rest_framework.pagination import PageNumberPagination

from core.apis.serializer import BlogsGetPostSerializer, BlogsRetrievePatchSerializer, ProjectGetPostSerializer, UserRegistrationSerializer

from core.models import Blogs, CustomUser, Project
from vrmarket.permissions import IsAuthenticatedAndAdmin



'''
    USER REGISTERATION API(USER SHOULD REGISTER WITH EMAIL , USERNAME AND PASSWORD)
'''
class UserRegistrationApiView(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]
    def post(self, request):
        datas = request.data
        serializer = UserRegistrationSerializer(data = datas)
        if serializer.is_valid():
            serializer.save(role = 'admin')
            return Response ({'message': 'Registration Sucessfull'}, status = status.HTTP_200_OK)  
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)  


'''
    User can Login using respective email and password
'''

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Invalid email.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password.")
        
        if not user.is_active:
            raise AuthenticationFailed("User account is not active.")
        
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    

''' 
    GET POST: => Projects Name
'''

class ProjectNamegetPostApiview(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]
        
    def get(self, request):
        data = Project.objects.filter(is_deleted = False).order_by('-updated_at')
        serializer =  ProjectGetPostSerializer(data , many = True)
        
        return Response({'details': 'Data Fetched Sucessfully', 'data': serializer.data}, status= status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectGetPostSerializer( data= request.data )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'details': 'data added sucessfully',
                'data': serializer.data
            }, status = status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
class ProjectsNameRetrieveUpdateDestory(APIView):
    permission_classes=[IsAuthenticatedAndAdmin]

    def get(self, request):
        data_id = request.GET.get('id')
        try:
            data = Project.objects.get(id = data_id)
        except Project.DoesNotExist:
            return Response({
                'error' : 'Invalid Id'
            }, status= status.HTTP_400_BAD_REQUEST)
        serializer = ProjectGetPostSerializer(data)
        return Response({'details': 'data fetch sucessfully', 'data': serializer.data}, status = status.HTTP_200_OK)
    def patch(self, request):
        data_id = request.GET.get('id')
        try:
            data = Project.objects.get(id = data_id)
        except Project.DoesNotExist:
            return Response({
                'error' : 'Invalid Id'
            }, status= status.HTTP_400_BAD_REQUEST)
        serializer = ProjectGetPostSerializer(data, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'details': 'data Updated sucessfully'}, status = status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data_id = request.GET.get('id')
        try:
            data = Project.objects.get(id = data_id)
        except Project.DoesNotExist:
            return Response({
                'error' : 'Invalid Id'
            }, status= status.HTTP_400_BAD_REQUEST)
        data.is_deleted=True
        data.save()
        return Response({'details': 'Data Deleted Sucessfully'}, status=  status.HTTP_200_OK)


class BlogGetPostApiView(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]

    def get(self, request):
        
        blogdata = Blogs.objects.filter(is_deleted = False)

        serializer = BlogsGetPostSerializer(blogdata, many = True)

        return Response({
            'details': 'Data fetched sucessfully',
            'data' : serializer.data
        }, status= status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = BlogsGetPostSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response ({
                'details' : 'data created sucessfully',
                'data' : serializer.data
                }, status= status.HTTP_200_OK
            )
        
        return Response({'error': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)
    
class BlogRetrievePatchDeleteApi(APIView):
    permission_classes = [IsAuthenticatedAndAdmin]

    def get(self, request):

        data_id = request.GET.get('id')
        
        try:
            data = Blogs.objects.get(id = data_id)
        except Blogs.DoesNotExist:
            return Response({'error' : 'Invalid ID'}, status= status.HTTP_400_BAD_REQUEST)
        
        serializer = BlogsRetrievePatchSerializer(data)

        return Response({'details': "Data Fetched Sucessful", 'data': serializer.data}, status= status.HTTP_200_OK)
    
    def patch (self, request):
        data_id = request.GET.get('id')
        
        try:
            data = Blogs.objects.get(id = data_id)
        except Blogs.DoesNotExist:
            return Response({'error' : 'Invalid ID'}, status= status.HTTP_400_BAD_REQUEST)
        
        if data.is_deleted == True:
            return Response({
                'error' : 'This data is unavailable'
            }, status = status.HTTP_400_BAD_REQUEST)
        
        project_id = request.data.get('project')
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                data.project = project
            except Project.DoesNotExist:
                return Response({'error': 'Invalid project ID'}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = BlogsRetrievePatchSerializer(data , data = request.data, partial= True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'details' : 'data updated sucessfully',
                'data': serializer.data
            }, status= status.HTTP_200_OK)
        
        return Response({
            'error': serializer.error
        }, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request):
        data_id = request.GET.get('id')

        try:
            data = Blogs.objects.get(id = data_id)  
        except Blogs.DoesNotExist:
            return Response({'error' : 'Invalid Blogs'}, status= status.HTTP_400_BAD_REQUEST)
        
        data.is_deleted = True
        data.save()
        return Response({'details': 'Data Deleted Sucessfully'}, status= status.HTTP_200_OK)