from apps.questions.serializers import QuestionSerializer
from rest_framework.views import APIView, Response


class CreateQuestionView(APIView):
    @staticmethod
    def post(request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})
