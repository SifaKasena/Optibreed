from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

app_name = "optibreed"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout',auth_views.LogoutView.as_view(template_name='logged_out.html'),name='logout'),
    path("home/", views.home, name="home"),
    path('add_room/', views.add_room, name='add_room'),
    path("rooms/<int:room_id>/", views.room_conditions, name="rooms"),
    path('endpoint/', views.receive_data, name='receive_data'),
    path('edit_room/<int:room_id>/',views.edit_room, name='edit_room'),
]