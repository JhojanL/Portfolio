# Generated by Django 4.1.7 on 2023-05-09 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0054_examquestion_orden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
