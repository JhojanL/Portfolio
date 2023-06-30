from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.user.username}"


class Collaborator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.user.username}"


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class University(models.Model):
    name = models.CharField(max_length=80)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    carrer_types = models.ManyToManyField('CarrerType', blank=True, related_name='carrer_types')
    careers = models.ManyToManyField('Career', blank=True, related_name='careers')
    social_media = models.ManyToManyField('SocialMedia', blank=True, related_name='social_media')
    admision_link = models.URLField(blank=True, null=True)
    exams = models.ManyToManyField('Exam', blank=True, related_name='exams')

    def __str__(self):
        return f"{self.name} - {self.country}"


class CarrerType(models.Model):
    name = models.CharField(max_length=80)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True, related_name='carrer_types_university')

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Career(models.Model):
    name = models.CharField(max_length=80)
    carrer_type = models.ForeignKey(CarrerType, on_delete=models.CASCADE, blank=True, null=True, related_name='careers_carrer_type')
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True, related_name='careers_university')

    def __str__(self):
        return f"{self.name} - {self.carrer_type.name} - {self.university.name}"


class SocialMedia(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True, related_name='social_media_university')

    def __str__(self):
        return f"{self.name} - {self.university.name} - {self.url}"


class Exam(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True)
    # The duration of the exam is in seconds
    duration = models.IntegerField(blank=True, null=True)
    students = models.ManyToManyField(Student, blank=True)
    collaborators = models.ManyToManyField(Collaborator, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    # Add the posibility to select multiple categories and subcategories
    categories = models.ManyToManyField('Category', blank=True)
    subcategories = models.ManyToManyField('Subcategory', blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        # Return the title and show the if the exam is active or not
        return f"{self.title} - Active: {self.is_active}"


class ExamCollaborator(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(Collaborator, on_delete=models.CASCADE)

class ExamStudent(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Explanation(models.Model):
    text = models.TextField()
    # Add image and video (URL) fields as optional
    image = models.URLField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    question = models.ForeignKey('ExamQuestion', on_delete=models.CASCADE, blank=True, null=True,related_name='explanations_question')
    # exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='explanations')

    def __str__(self):
        return f"{self.text}"

class Category(models.Model):
    name = models.CharField(max_length=50)
    # exams = models.ManyToManyField(Exam, blank=True)

    def __str__(self):
        return f"{self.name}"

class Subcategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # exams = models.ManyToManyField(Exam, blank=True)

    def __str__(self):
        return f"{self.name} - {self.category.name}"


class ExamCategory(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class ExamSubcategory(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)


class ExamQuestion(models.Model):
    question = models.TextField()
    # Add image field as url
    image = models.URLField(blank=True, null=True)
    answer = models.TextField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE, blank=True, null=True, related_name="explanations")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    orden = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.question}: {self.answer}"


class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    option_text = models.TextField()
    option_image = models.URLField(blank=True, null=True)
    is_correct = models.BooleanField()

    def __str__(self):
        if self.option_image:
            return f"{self.question.question} - {self.option_image} - {self.is_correct} ({self.id})"
        else:
            return f"{self.question.question} - {self.option_text} - {self.is_correct} ({self.id})"


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    option = models.ForeignKey(MultipleChoiceOption, on_delete=models.CASCADE)
    exam_result = models.ForeignKey('ExamResult', on_delete=models.CASCADE, blank=True, null=True, related_name='student_answers')

    def __str__(self):
        return f"{self.student}: {self.option}"

class ExamSession(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.exam} - {self.student} - {self.start_time}"
    
    def time_left(self):
        time_left = self.exam.duration - (timezone.now() - self.start_time).total_seconds()
        return time_left

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    # Don´t delete the exam if the ExamResult is deleted
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    score = models.IntegerField(default=0)
    # Add the date of the exam
    date = models.DateField(auto_now_add=True)
    duration = models.FloatField(default=0)
    answers = models.ManyToManyField(StudentAnswer, blank=True)

    def __str__(self):
        return f"{self.exam} - {self.student} - {self.score} - {self.date} - {self.duration}"