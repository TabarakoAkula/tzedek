from django.shortcuts import render
from rest_framework.views import APIView, Response
from apps.questions.serializers import QuestionSerializer


class CreateQuestionView(APIView):
    @staticmethod
    def post(request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})
