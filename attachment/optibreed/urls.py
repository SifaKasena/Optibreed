from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

app_name = "optibreed"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("home/", views.home, name="home"),
    # path("rooms/new/", views.new, name="new"),
    # path("rooms/<int:room_id>/", views.detail, name="detail"),
]