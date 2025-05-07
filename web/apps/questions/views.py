from apps.questions.constants import TR_TG_TEXT
from apps.questions.models import Question
from apps.questions.serializers import QuestionSerializer
import apps.questions.tasks as tasks
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView, Response


class CreateQuestionView(APIView):
    @staticmethod
    def post(request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            question_author = serializer.instance.author
            tasks.manager_edit_message(
                serializer.instance.author.telegram_id,
                {
                    "message": TR_TG_TEXT["accepted"][question_author.language],
                    "message_id": serializer.instance.message_id,
                    "inline_reply_markup": [],
                },
            )
            tasks.manager_ask_question(
                {
                    "telegram_id": question_author.telegram_id,
                    "message_id": serializer.instance.message_id,
                    "question": serializer.instance.question_text,
                    "language": question_author.language,
                },
            )
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})


class GetQuestionView(RetrieveAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
