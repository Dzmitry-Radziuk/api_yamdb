from rest_framework import status
from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Пользователь не найден."
    default_code = "user_not_found"


class InvalidConfirmationCode(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Неверный код подтверждения."
    default_code = "invalid_confirmation_code"
