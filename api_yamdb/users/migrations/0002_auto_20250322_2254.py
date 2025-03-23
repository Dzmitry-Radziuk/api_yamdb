# Generated by Django 3.2 on 2025-03-22 19:54

import django.core.validators
from django.db import migrations, models

import api.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Аутентифицированный пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=9, verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Пользователь с таким именем уже существует.'}, max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Введите корректное имя пользователя. Допустимы буквы, цифры и символы @/./+/-/_.', regex='^[\\w.@+-]+\\Z'), api.validators.username_not_me_validator], verbose_name='Имя пользователя'),
        ),
    ]
