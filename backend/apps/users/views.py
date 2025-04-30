from apps.questions.serializers import QuestionSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer
from rest_framework.views import APIView, Response


class UserGetCreateView(APIView):
    @staticmethod
    def get(request, telegram_id: str):
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User does not exists"})
        serializer = UserSerializer(user)
        return Response({"success": True, "data": serializer.data})

    @staticmethod
    def post(request, telegram_id):
        try:
            request_telegram_id = request.data["telegram_id"]
        except KeyError:
            return Response(
                {
                    "success": False,
                    "message": "You must provide telegram_id in request body",
                },
            )
        if request_telegram_id != telegram_id:
            return Response(
                {
                    "success": False,
                    "message": "Telegram ids in request and in url are"
                    " different (two equals strings)",
                },
            )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})


class UserUpdateUsernameView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update_username(validated_data=request.data)
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})


class GetUserQuestions(APIView):
    @staticmethod
    def get(request, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User does not exists"})
        questions = user.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response({"success": True, "data": serializer.data})
