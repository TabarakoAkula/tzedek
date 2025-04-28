from django.urls import path
import apps.questions.views as views

urlpatterns = [
    path("", views.CreateQuestionView.as_view()),
]
