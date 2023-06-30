# Generated by Django 4.1.3 on 2023-01-31 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0024_rename_student_exam_students_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='collaborator',
            new_name='collaborators',
        ),
        migrations.CreateModel(
            name='ExamCollaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.collaborator')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.exam')),
            ],
        ),
    ]
