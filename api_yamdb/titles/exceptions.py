from rest_framework.exceptions import MethodNotAllowed


class MethodNotAllowedException(MethodNotAllowed):
    """Исключение для запрета метода (405)."""

    def __init__(self, method="GET"):
        super().__init__(method=method, detail=f"Метод {method} не разрешён.")
