# Generated by Django 4.1.2 on 2022-11-13 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_tag_question_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerrating',
            old_name='question_id',
            new_name='answer_id',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='question',
            name='rating',
        ),
    ]