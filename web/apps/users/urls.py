import apps.users.views as views
from django.urls import path


urlpatterns = [
    path("update_username", views.UserUpdateUsernameView.as_view()),
    path("change_language", views.ChangeLanguageView.as_view()),
    path("<str:telegram_id>", views.UserGetCreateView.as_view()),
    path("get_questions/<str:telegram_id>", views.GetUserQuestions.as_view()),
]
