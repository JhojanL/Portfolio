# Generated by Django 4.1.3 on 2023-01-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0020_rename_date_of_birth_collaborator_birthday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='time',
        ),
        migrations.AddField(
            model_name='exam',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
