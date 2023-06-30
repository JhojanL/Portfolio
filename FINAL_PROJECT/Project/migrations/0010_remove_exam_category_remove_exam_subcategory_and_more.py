# Generated by Django 4.1.3 on 2022-12-23 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0009_remove_exam_categories_remove_exam_subcategories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='category',
        ),
        migrations.RemoveField(
            model_name='exam',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='exam',
            name='categories',
            field=models.ManyToManyField(blank=True, to='Project.category'),
        ),
        migrations.AddField(
            model_name='exam',
            name='subcategories',
            field=models.ManyToManyField(blank=True, to='Project.subcategory'),
        ),
    ]
