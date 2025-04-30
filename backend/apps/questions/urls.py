import apps.questions.views as views
from django.urls import path


urlpatterns = [
    path("", views.CreateQuestionView.as_view()),
]
