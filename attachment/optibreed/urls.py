from django.urls import path
from . import views

app_name = "optibreed"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.CustomSignupView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("rooms/", views.rooms, name="rooms"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("rooms/add_room/", views.add_room, name="add_room"),
    path("rooms/<int:room_id>/", views.room_conditions, name="room_conditions"),
    path("notifications_list/", views.notifications_list, name = "notifications_list"),
    path("notification_details/", views.notification_details, name="notification_details"),
    path("endpoint/", views.receive_data, name="receive_data"),
    path("edit_room/<int:room_id>/", views.edit_room, name="edit_room"),
    path("generate_report/", views.generate_report, name="generate_report"),
    path("api/latest-condition/<int:room_id>/", views.LatestConditionView.as_view(), name="latest-condition"),
]
