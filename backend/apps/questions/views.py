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
            tasks.manager_edit_message(
                serializer.instance.author.telegram_id,
                {
                    "message": "✅ Request accepted",
                    "message_id": serializer.instance.message_id,
                    "inline_reply_markup": [],
                },
            )
            tasks.manager_ask_question(
                {
                    "telegram_id": serializer.instance.author.telegram_id,
                    "message_id": serializer.instance.message_id,
                    "question": serializer.instance.question_text,
                },
            )
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})


class GetQuestionView(RetrieveAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
