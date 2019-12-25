from django.urls import path
from .views import login_view, logout_view, register_view, all_user_view, detail_user_view, delete_user_view, \
    update_user_view
from django.views.generic import TemplateView

app_name = "loginapp"
urlpatterns = [
    path('', TemplateView.as_view(template_name="mainlogin/main.html"), name="main"),
    path('home/', TemplateView.as_view(template_name="mainlogin/home.html"), name="home"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    path('users/', all_user_view, name="user_list"),
    path('users/<int:id>/', detail_user_view, name="users_detail"),
    path('delete/<int:id>/', delete_user_view, name="delete"),
    path('update/<int:id>/', update_user_view, name="update"),

]
