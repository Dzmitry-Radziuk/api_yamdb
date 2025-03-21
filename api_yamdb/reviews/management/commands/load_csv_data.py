import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User

DATA_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    """Загружает данные из CSV-файлов в базу данных."""

    def load_csv(self, model, file_name, field_mapping=None):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл {file_name} не найден!"))
            return

        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            objects = []
            for row in reader:
                if field_mapping:
                    row = {field_mapping.get(k, k): v for k, v in row.items()}
                if model == Title:
                    cat_id = row.get('category') or row.get('category_id')
                    row['category'] = Category.objects.get(id=cat_id)
                if model == Review:
                    auth_id = row.get('author') or row.get('author_id')
                    row['author'] = User.objects.get(id=auth_id)
                    title_value = row.get('title') or row.get('title_id')
                    row['title'] = Title.objects.get(id=title_value)
                if model == Comment:
                    auth_id = row.get('author') or row.get('author_id')
                    row['author'] = User.objects.get(id=auth_id)
                    review_value = row.get('review') or row.get('review_id')
                    row['review'] = Review.objects.get(id=review_value)
                objects.append(model(**row))
            model.objects.bulk_create(objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(
                f"Успешно загружено {len(objects)} записей в {model.__name__}"
            ))

    def handle(self, *args, **kwargs):
        model_files = {
            Category: 'category.csv',
            Genre: 'genre.csv',
            User: 'users.csv',
            Title: 'titles.csv',
            Review: 'review.csv',
            Comment: 'comments.csv',
        }

        for model, filename in model_files.items():
            self.load_csv(model, filename)
