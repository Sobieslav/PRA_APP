# Generated by Django 4.2.5 on 2023-09-25 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pra_app', '0002_remove_game_genre_remove_movie_genre_game_genre_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='genre',
            new_name='genres',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
    ]