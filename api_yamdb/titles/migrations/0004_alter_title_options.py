# Generated by Django 3.2 on 2025-03-21 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0003_title_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]
