# Generated by Django 2.1.7 on 2019-03-01 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foro_user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thread',
            old_name='boardId',
            new_name='board',
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='lastUserId',
            new_name='lastUser',
        ),
        migrations.RenameField(
            model_name='thread',
            old_name='userId',
            new_name='user',
        ),
    ]