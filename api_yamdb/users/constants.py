USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]

USERNAME_REGEX = r'^[\w.@+-]+\Z'

FORBIDDEN_USERNAMES = {"me"}

MAX_LENGTH_NAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_ROLE = max(len(role[0]) for role in ROLE_CHOICES)
MAX_LENGTH_CONFIRM_CODE = 10
MAX_LENGTH_STR = 30

PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
