from django.urls import path

from myapp.api.apis import Blog, Blogspaginationview

urlpatterns = [
    path('blogs', Blog.as_view()),
    path('Blogspaginationview', Blogspaginationview.as_view())
]