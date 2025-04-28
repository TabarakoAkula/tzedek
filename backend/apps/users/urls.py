from django.urls import path
import apps.users.views as views

urlpatterns = [
    path("update_username", views.UserUpdateUsernameView.as_view()),
    path("<str:telegram_id>", views.UserGetCreateView.as_view()),
]
