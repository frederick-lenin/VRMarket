from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError as JWTTokenError
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils.urls import replace_query_param

from core.models import Blogs
from myapp.api.serializer import BlogviewSerializer


class Blog(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        data = Blogs.objects.all().order_by('-updated_at')[:9]

        serializer = BlogviewSerializer(data, many=True)
        return Response({'details': "Data Fetched Sucessfully", "data": serializer.data}, status= status.HTTP_200_OK)


class BlogsPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    # max_page_size = 100

    def get_first_link(self):
        if self.page.paginator.num_pages == 0:
            return None
        return replace_query_param(self.request.build_absolute_uri(), self.page_query_param, 1)

    def get_last_link(self):
        if self.page.paginator.num_pages == 0:
            return None
        return replace_query_param(self.request.build_absolute_uri(), self.page_query_param, self.page.paginator.num_pages)

    def get_paginated_response(self, data):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages

        window_size = 5
        # start_page = max(1, current_page - (window_size // 2))
        # end_page = min(total_pages, start_page + window_size - 1)

        # if (end_page - start_page + 1) < window_size:
        #     start_page = max(1, end_page - window_size + 1)

        # page_range = list(range(start_page, end_page + 1))

        return Response({
            'total_pages': total_pages,
            'current_page': current_page,
            'total_items': self.page.paginator.count,
            'page_size': self.page_size,
            'first': self.get_first_link(),
            'last': self.get_last_link(),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            # 'page_range': page_range,
            'results': data
        }, status= status.HTTP_200_OK)

class Blogspaginationview(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        
        data = Blogs.objects.all().order_by('-updated_at')


        paginator = BlogsPagination()
        paginated_properties = paginator.paginate_queryset(data, request)
        
        serializer = BlogviewSerializer(paginated_properties, many=True)
        
        return paginator.get_paginated_response(serializer.data)
