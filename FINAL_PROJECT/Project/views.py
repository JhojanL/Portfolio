import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.utils import timezone
from django.middleware.csrf import get_token
from django.contrib import messages

from .models import User, Student, Collaborator, Country, University, Exam, Explanation, ExamQuestion, MultipleChoiceOption, StudentAnswer, ExamSession, ExamResult, Category, Subcategory

def index(request):
    return render(request, "Project/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("exams"))
        else:
            messages.warning(request, 'Invalid username and/or password.')
            return render(request, "Project/login.html")
    else:
        return render(request, "Project/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.warning(request, 'Passwords must match.')
            return render(request, "Project/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # Create student
            student = Student(user=user, birthday=birthday)
            student.save()
        except IntegrityError:
            messages.warning(request, 'Username already taken.')
            return render(request, "Project/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("exams"))
    else:
        return render(request, "Project/register.html")


def get_exams(request):
    # Get all universities
    universities = University.objects.all().order_by('name')

    # Check if the user is a student
    if request.user.is_authenticated:
        is_student = Student.objects.filter(user=request.user).exists()
    else:
        is_student = False

    # Paginate universities
    paginator = Paginator(universities, 10) # Show 10 universities per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Project/exams.html", {
        "is_student": is_student,
        "page_obj": page_obj,
    })

@login_required(login_url='login')
def start_exam(request, exam_id):
    student = Student.objects.get(user=request.user)
    exam = Exam.objects.get(pk=exam_id)
    exam_session, created = ExamSession.objects.get_or_create(exam=exam, student=student, defaults={'start_time': timezone.now()})
    if not created:
        exam_session.start_time = timezone.now()
        exam_session.save()
    return HttpResponseRedirect(reverse_lazy("exam", args=(exam_id,)))

@login_required(login_url='login')
def exam_view(request, exam_id):
    # Get exam
    exam = Exam.objects.get(pk=exam_id)

    # Get exam questions
    exam_questions = ExamQuestion.objects.filter(exam=exam).order_by('orden')

    # Get exam questions and options
    exam_questions_options = []
    for exam_question in exam_questions:
        exam_question_options = MultipleChoiceOption.objects.filter(question=exam_question)
        exam_questions_options.append([exam_question, exam_question_options])

    # Get the last exam session
    exam_session = ExamSession.objects.filter(exam=exam, student=Student.objects.get(user=request.user)).last()
    end_time = exam_session.start_time + timezone.timedelta(minutes=exam.duration)
    exam_session.end_time = end_time
    exam_session.save()
    end_time_iso = end_time.isoformat()

    return render(request, "Project/exam.html", {
        "exam": exam,
        "exam_questions_options": exam_questions_options,
        "end_time": end_time_iso,
    })

@login_required(login_url='login')
def save_exam(request, exam_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get exam
    exam = Exam.objects.get(pk=exam_id)
    questions = ExamQuestion.objects.filter(exam=exam)
    student = Student.objects.get(user=request.user)

    # Get form data
    data = json.loads(request.body)
    answers = data.get("answers", "")
    student_answers = []

    exam_result = ExamResult.objects.create(exam=exam, student=student)

    for key, value in answers.items():
        question = questions.filter(pk=key).first() # get the question corresponding to the answer
        if question is not None: # if the question is in the exam
            # Check if the option of MultipleChoiceQuestion is option_text or option_image
            options = MultipleChoiceOption.objects.filter(question=question)
            if options.first().option_image:
                option = MultipleChoiceOption.objects.get(question=question, option_image=value)
            else:
                option = MultipleChoiceOption.objects.get(question=question, option_text=value)
                
            student_answer = StudentAnswer(student=student, option=option, exam_result=exam_result)
            student_answer.save()
            student_answers.append(student_answer)
            exam_result.answers.add(student_answer)

    # Calculate score
    score = calculate_exam_score(student_answers)

    # Save exam result
    duration = timezone.now() - ExamSession.objects.filter(exam=exam, student=student).last().start_time
    exam_result.score = score
    duration_seconds = duration.total_seconds()
    duration_minutes = round(duration_seconds / 60, 2)
    exam_result.duration = float(duration_minutes)
    exam_result.save()

    # return JsonResponse({"message": "Exam saved successfully."}, status=201)
    data = {"message": "Exam saved successfully.", "exam_result_id": exam_result.id}
    return JsonResponse(data, status=201)

def calculate_exam_score(student_answers):
    score = 0
    for student_answer in student_answers:
        if student_answer.option.is_correct:
            score += 1
    return score


@login_required(login_url='login')
def exam_edit(request, exam_id, filter):
    csrf_token = get_token(request)
    exam = Exam.objects.get(pk=exam_id)
    if filter == "fecha":
        exam_questions = ExamQuestion.objects.filter(exam=exam).order_by('creation_date')
    elif filter == "categoria":
        exam_questions = ExamQuestion.objects.filter(exam=exam).order_by('category', 'subcategory', 'orden')
    elif filter == "orden":
        exam_questions = ExamQuestion.objects.filter(exam=exam).order_by('orden')
        
    exam_questions_options = []
    for exam_question in exam_questions:
        exam_question_options = MultipleChoiceOption.objects.filter(question=exam_question)
        exam_questions_options.append([exam_question, exam_question_options])

    # Categories and subcategories, filter by exam
    categories = Category.objects.filter(exam=exam)
    subcategories = Subcategory.objects.filter(exam=exam)

    return render(request, "Project/exam_edit.html", {
        "exam": exam,
        "exam_questions_options": exam_questions_options,
        "categories": categories,
        "subcategories": subcategories,
        "csrf_token": csrf_token
    })


@login_required(login_url='login')
def question_update(request, question_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    # Get question
    question = ExamQuestion.objects.get(pk=question_id)

    # Get form data
    data = json.loads(request.body)
    question_text = data.get("questionText", "")
    question_image = data.get("questionImage", "")
    category_id = data.get("questionCategoryId", "")
    subcategory_id = data.get("questionSubcategoryId", "")
    question_orden = data.get("questionOrden", "")
    is_image = data.get("questionSwitch", "") # if the options of the question are text or image
    options = data.get("options", "")
    answer = data.get("answer", "")
    explanation_id = data.get("explanationId", "")
    explanation_text = data.get("explanationText", "")
    explanation_image = data.get("explanationImage", "")
    explanation_video = data.get("explanationVideo", "")

    # Update question
    question.question = question_text
    question.image = question_image
    question.answer = answer
    question.category = Category.objects.get(id=category_id)
    question.subcategory = Subcategory.objects.get(id=subcategory_id)
    question.orden = int(question_orden)
    question.save()

    # Update explanation but if doesn't exist create it
    if explanation_id == "":
        explanation = Explanation.objects.create(text=explanation_text, image=explanation_image, video=explanation_video, question=question)
        question.explanation = explanation
        question.save()
    else:
        explanation = Explanation.objects.get(id=explanation_id)
        explanation.text = explanation_text
        explanation.image = explanation_image
        explanation.video = explanation_video
        explanation.save()

    # Update text options
    if is_image:
        for key, value in options.items():
            option = MultipleChoiceOption.objects.get(id=key)
            option.option_image = value
            option.option_text = ""
            option.is_correct = value == answer
            option.save()
    # Update image options
    else:
        for key, value in options.items():
            option = MultipleChoiceOption.objects.get(id=key)
            option.option_text = value
            option.option_image = ""
            option.is_correct = value == answer
            option.save()
    return JsonResponse({"message": "Question updated successfully."}, status=201)


@login_required(login_url='login')
def new_question(request, exam_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get exam
    exam = Exam.objects.get(pk=exam_id)

    # Get form data
    data = json.loads(request.body)
    question_text = data.get("questionText", "")
    question_image = data.get("questionImage", "")
    category_id = data.get("questionCategoryId", "")
    subcategory_id = data.get("questionSubcategoryId", "")
    question_orden = data.get("questionOrden", "")
    is_image = data.get("questionSwitch", "") # if the options of the question are text or image
    options = data.get("options", "")
    answer = data.get("answer", "")
    explanation_text = data.get("explanationText", "")
    explanation_image = data.get("explanationImage", "")
    explanation_video = data.get("explanationVideo", "")

    # Create question
    question = ExamQuestion.objects.create(question=question_text, image=question_image, answer=answer, exam=exam, category=Category.objects.get(id=category_id), subcategory=Subcategory.objects.get(id=subcategory_id), orden=int(question_orden))

    # Create explanation
    explanation = Explanation.objects.create(text=explanation_text, image=explanation_image, video=explanation_video, question=question)
    question.explanation = explanation
    question.save()

    # Create text options
    if is_image:
        for value in options.values():
            option = MultipleChoiceOption.objects.create(option_text="", option_image=value, question=question, is_correct=value==answer)
            option.save()
    # Create image options
    else:
        for value in options.values():
            option = MultipleChoiceOption.objects.create(option_text=value, option_image="", question=question, is_correct=value==answer)
            option.save()

    return JsonResponse({"message": "Question created successfully."}, status=201)


@login_required(login_url='login')
def question_delete(request, question_id, exam_id):    
    # Check if question exists
    try:
        question = ExamQuestion.objects.get(pk=question_id)
    except ExamQuestion.DoesNotExist:
        messages.warning(request, "La pregunta no existe.")
        return redirect("exam_edit", exam_id=exam_id)
    
    # Check if the user is a collaborator of the exam
    if not request.user.is_staff:
        exam = question.exam
        if not exam.collaborators.filter(user=request.user).exists():
            messages.warning(request, "Tu no eres colaborador de este examen.")
            return redirect("exam_edit", exam_id=exam_id, filter="fecha")
    

    # Delete question
    question.delete()
    messages.success(request, "Pregunta eliminada correctamente.")
    return redirect("exam_edit", exam_id=exam_id, filter="fecha")


@login_required(login_url='login')
def profile(request, username):
    # Check if user exists
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "Project/404.html", status=404)
    
    is_student, is_collaborator = False, False

    # Check if the user is a collaborator or student of the exam
    if Student.objects.filter(user=user).exists():
        student = Student.objects.get(user=user)
        exams = ExamResult.objects.filter(student=student).order_by('-date')
        is_student = True
    
    if Collaborator.objects.filter(user=user).exists():
        collaborator = Collaborator.objects.get(user=user)
        exams = Exam.objects.filter(collaborators=collaborator).order_by('university')
        is_collaborator = True

    # Pagination
    paginator = Paginator(exams, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Project/profile.html", {
        "user": user,
        "page_obj": page_obj,
        "is_student": is_student,
        "is_collaborator": is_collaborator
    })


@login_required(login_url='login')
def exam_result(request, result_id):
    # Check if result exists
    try:
        results = ExamResult.objects.get(pk=result_id)
    except ExamResult.DoesNotExist:
        return render(request, "Project/404.html", status=404)

    student_answers = StudentAnswer.objects.filter(exam_result=results)
    # Get exam questions
    exam_questions = []
    for exam_question in student_answers:
        exam_questions.append(exam_question.option.question)

    # Get exam questions and options
    exam_questions_options = []
    for exam_question in exam_questions:
        exam_question_options = MultipleChoiceOption.objects.filter(question=exam_question)
        exam_questions_options.append([exam_question, exam_question_options])

    answers = []
    for student_answer in student_answers:
        answers.append(student_answer.option)

    return render(request, "Project/exam_result.html", {
        "results": results,
        "exam_questions_options": exam_questions_options,
        "answers": answers
    })