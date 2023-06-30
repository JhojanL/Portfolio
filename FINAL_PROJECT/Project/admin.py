from django.contrib import admin
from .models import User, Student, Collaborator, Country, University, CarrerType, Career, SocialMedia, Exam, Explanation, ExamQuestion, MultipleChoiceOption, StudentAnswer, ExamSession, Category, Subcategory, ExamResult

class ExamAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories', 'subcategories', 'collaborators', 'students')

class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer', 'exam')

class ExplanationAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question_id')

    def question_id(self, obj):
        return obj.question.id

class MultipleChoiceOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'option', 'is_correct', 'question_id')

    def question_id(self, obj):
        return obj.question.id
    
    def option(self, obj):
        if obj.option_image:
            return obj.option_image
        else:
            return obj.option_text

class ExamResultAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('answers__option', 'answers__option__question')
        # Muestra solo las respuestas del examen seleccionado
        exam_id = request.GET.get('exam')
        if exam_id:
            qs = qs.filter(exam_id=exam_id)
        return qs

    def answers_display(self, obj):
        return ", ".join([str(answer.option.id) for answer in obj.answers.all()])
    answers_display.short_description = 'Answers'

    list_display = ['id', 'student', 'exam', 'score', 'date', 'duration', 'answers_display']
    list_filter = ['exam']

class CarrerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'university')
    list_filter = ('university',)

class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'carrer_type')
    list_filter = ('carrer_type', 'university')

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'university')
    list_filter = ('university',)

class UniversityAdmin(admin.ModelAdmin):
    filter_horizontal = ('carrer_types', 'careers', 'social_media', 'exams')

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Collaborator)
admin.site.register(Country)
admin.site.register(University, UniversityAdmin)
admin.site.register(CarrerType, CarrerTypeAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Explanation, ExplanationAdmin)
admin.site.register(ExamQuestion, ExamQuestionAdmin)
admin.site.register(MultipleChoiceOption, MultipleChoiceOptionAdmin)
admin.site.register(StudentAnswer)
admin.site.register(ExamSession)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)