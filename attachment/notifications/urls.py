from django.urls import path
from . import views

app_name = "notifications"
urlpatterns = [
    path("list/", views.notifications_list, name="list"),
    path("details/<int:notification_id>", views.notification_details, name="details"),
    path("delete/<int:notification_id>", views.notification_delete, name="delete"),
    path("update-status/<int:notification_id>", views.notification_update_status, name="update-status"),
]
