from django.urls import path

# Third party imports
from rest_framework_simplejwt.views import TokenRefreshView

from core.apis.api import BlogGetPostApiView, BlogRetrievePatchDeleteApi, LoginAPIView, ProjectNamegetPostApiview, ProjectsNameRetrieveUpdateDestory, UserRegistrationApiView

urlpatterns = [
    path('registration', UserRegistrationApiView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('refresh', TokenRefreshView.as_view()),

    #Project
    path('project', ProjectNamegetPostApiview.as_view()),
    path('projectupdate', ProjectsNameRetrieveUpdateDestory.as_view()),

    path('blogcreatepost', BlogGetPostApiView.as_view()),
    path('blogretrievepatchdestory', BlogRetrievePatchDeleteApi.as_view()),
]