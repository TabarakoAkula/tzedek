import asyncio

from apps.questions.models import Question
from apps.questions.notifier import edit_message, send_message
from apps.questions.utils import ask_question
from celery import shared_task
from django.conf import settings

USE_CELERY = settings.USE_CELERY


def manager_send_message(telegram_id: int, data: dict) -> None:
    if USE_CELERY:
        return celery_send_message.delay(telegram_id, data)
    return celery_send_message(telegram_id, data)


@shared_task
def celery_send_message(telegram_id: int, data: dict) -> None:
    return asyncio.run(send_message(telegram_id, data))


def manager_edit_message(telegram_id: int, data: dict) -> None:
    if USE_CELERY:
        return celery_edit_message.delay(telegram_id, data)
    return celery_edit_message(telegram_id, data)


@shared_task
def celery_edit_message(telegram_id: int, data: dict) -> None:
    return asyncio.run(edit_message(telegram_id, data))


def manager_ask_question(data: dict) -> None:
    if USE_CELERY:
        return celery_ask_question.delay(data)
    return celery_ask_question(data)


@shared_task()
def celery_ask_question(data: dict) -> None:
    data["edit_message_func"] = edit_message
    data["send_message_func"] = send_message
    answer = asyncio.run(ask_question(data))

    question_obj = Question.objects.get(message_id=data["message_id"])
    question_obj.answer_text = answer["text"]
    question_obj.chat_session_id = answer["chat_session_id"]
    question_obj.success = answer["success"]
    question_obj.save()

    answer_text = answer["text"]
    return asyncio.run(
        edit_message(
            data["telegram_id"],
            {
                "message": answer_text,
                "message_id": data["message_id"],
            },
        ),
    )
