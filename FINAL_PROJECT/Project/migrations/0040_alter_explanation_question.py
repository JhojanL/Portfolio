# Generated by Django 4.1.7 on 2023-03-19 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0039_remove_explanation_exam_explanation_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='explanations_question', to='Project.examquestion'),
        ),
    ]
