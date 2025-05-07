import apps.questions.views as views
from django.urls import path


urlpatterns = [
    path("create_question", views.CreateQuestionView.as_view()),
    path("<pk>", views.GetQuestionView.as_view()),
]
