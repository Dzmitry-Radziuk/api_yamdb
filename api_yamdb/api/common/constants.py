MIN_REVIEW_SCORE = 1
MAX_REVIEW_SCORE = 10
MAX_LENGTH_TEXT = 250
MAX_LENGTH_NAME = 150
MAX_LENGTH_SLUG = 50
MAX_LENGTH_STR = 50
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_CONFIRM_CODE = 10
FORBIDDEN_NAME = 'me'
SLUG_REGEX_PATTERN = r'^[-a-zA-Z0-9_]+$'

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]

MAX_LENGTH_ROLE = max(len(role[0]) for role in ROLE_CHOICES)
FORBIDDEN_USERNAMES = {"me"}

PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

MIN_REVIEW_SCORE_MSG = f'Минимальная оценка — {MIN_REVIEW_SCORE}'
MAX_REVIEW_SCORE_MSG = f'Максимальная оценка — {MAX_REVIEW_SCORE}'

USER_ROLES_ALLOWED_TO_EDIT = ['moderator', 'admin']

USERNAME_REGEX = r'^[\w.@+-]+\Z'
