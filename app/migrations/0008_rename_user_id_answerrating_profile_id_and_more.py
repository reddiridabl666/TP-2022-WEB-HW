# Generated by Django 4.1.2 on 2022-11-13 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_question_id_answerrating_answer_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answerrating',
            old_name='user_id',
            new_name='profile_id',
        ),
        migrations.RenameField(
            model_name='questionrating',
            old_name='user_id',
            new_name='profile_id',
        ),
    ]
