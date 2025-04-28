from django.shortcuts import render
from rest_framework.views import APIView, Response
from apps.users.serializers import UsersSerializer
from apps.users.models import Users


class UserGetCreateView(APIView):
    @staticmethod
    def get(request, telegram_id: str):
        try:
            user = Users.objects.get(telegram_id=telegram_id)
        except Users.DoesNotExist:
            return Response({"success": False, "message": "User does not exists"})
        serializer = UsersSerializer(user)
        return Response({"success": True, "data": serializer.data})

    @staticmethod
    def post(request, telegram_id):
        try:
            request_telegram_id = request.data["telegram_id"]
        except KeyError:
            return Response({"success": False, "message": "You must provide telegram_id in request body"})
        if request_telegram_id != telegram_id:
            return Response(
                {
                    "success": False,
                    "message": "Telegram ids in request and in url are different (two equals strings)",
                }
            )
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})


class UserUpdateUsernameView(APIView):
    @staticmethod
    def post(request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update_username(validated_data=request.data)
            return Response({"success": True, "data": serializer.data})
        return Response({"success": False, "message": serializer.errors})
