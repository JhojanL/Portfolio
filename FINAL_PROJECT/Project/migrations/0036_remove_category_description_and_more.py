# Generated by Django 4.1.3 on 2023-03-08 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0035_examresult_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.RemoveField(
            model_name='subcategory',
            name='description',
        ),
    ]
