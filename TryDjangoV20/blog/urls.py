from django.urls import path
from .views import blog_create
from .views import BlogListView, BlogDetailView, BlogDelete
from .views import (BlogClassApiView, BlogDetailUpdateDeleteClassView,
                    BlogGenericListApiView,
                    BlogGenericUpdateDeleteDetailApiView
                    )

app_name = "blogapp"
urlpatterns = [
    path('', BlogListView.as_view(), name="blog_list"),
    # path('', blog_list, name="blog_list"),



    path('api/', BlogGenericListApiView.as_view(), name="blog_api_list"),
    path('api/<int:pk>/', BlogGenericUpdateDeleteDetailApiView.as_view(), name="blog_api_detail"),





    path('delete/<str:slug>/', BlogDelete.as_view(), name="blog_delete"),
    # path('delete/<str:slug>/', blog_delete, name="blog_delete"),

    # path('create/', BlogCreateView.as_view(), name="blog_create"),
    path('create/', blog_create, name="blog_create"),

    path('<str:slug>/', BlogDetailView.as_view(), name="blog_detail"),
    # path('<str:slug>/', blog_detail, name="blog_detail"),
    # path('<int:primarykey>/',blog_detail),
]
