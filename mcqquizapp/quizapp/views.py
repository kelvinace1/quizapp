from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Quiz, Section, Question, UserProgress, Course
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CourseForm,QuizForm, SectionForm, QuestionForm, QuizFormSet, SectionFormSet, QuestionFormSet
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm


passing = 0
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'quizapp/course_list.html', {'courses': courses})


@login_required
def quiz_list(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    quizzes = Quiz.objects.filter(course=course)

    
    easy_sections = Section.objects.filter(quiz__in=quizzes, difficulty='easy')
    medium_sections = Section.objects.filter(quiz__in=quizzes, difficulty='medium')
    hard_sections = Section.objects.filter(quiz__in=quizzes, difficulty='hard')

    return render(request, 'quizapp/quiz_list.html', {
        'course': course,
        'easy_sections': easy_sections,
        'medium_sections': medium_sections,
        'hard_sections': hard_sections,
    })


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Only check sections that exist
    difficulties = ['easy', 'medium', 'hard']
    existing_sections = quiz.section_set.filter(difficulty__in=difficulties)
    existing_difficulties = set(existing_sections.values_list('difficulty', flat=True))

    for level in difficulties:
        if level not in existing_difficulties:
            
            continue

        section = existing_sections.get(difficulty=level)
        latest_attempt = UserProgress.objects.filter(user=request.user, section=section).order_by('-attempted_at').first()

        if not latest_attempt or not latest_attempt.passed:
            return redirect('take_section', section_id=section.id)

    return render(request, 'quizapp/completed.html', {'course': section.quiz.course})

@login_required
def take_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    questions = section.question_set.all()
    quiz = section.quiz

    if request.method == 'POST':
        total = questions.count()
        correct = 0
        

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected and selected.lower() == question.correct_option.lower():
                correct += 1

        score = (correct / total) * 100
        passed = score >= 50

        # Save attempt even if one exists before
        UserProgress.objects.create(
            user=request.user,
            section=section,
            score=score,
            passed=passed
        )
        

        next_section = None
        if passed:
            passing = passing + 1
            for level in ['easy', 'medium', 'hard']:
                for s in quiz.section_set.filter(difficulty=level):
                    if not UserProgress.objects.filter(user=request.user, section=s, passed=True).exists():
                        next_section = s
                        break
                if next_section:
                    break

        return render(request, 'quizapp/result.html', {
            'section': section,
            'score': score,
            'passed': passed,
            'next_section': next_section,
            'course': section.quiz.course,
            'passing': passing,
        })

        #Retake current section on fail
        messages.warning(request, "You did not pass this section. Please try again.")
        return redirect('take_section', section_id=section.id)

    return render(request, 'quizapp/take_section.html', {'section': section, 'questions': questions})

@login_required
def submit_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    questions = section.question_set.all()
    score = 0

    for question in questions:
        user_answer = request.POST.get(f'question_{question.id}')
        if user_answer == question.correct_option:
            score += 10

    passed = score >= 50

    UserProgress.objects.create(
        user=request.user,
        section=section,
        score=score,
        passed=passed
    )

    return render(request, 'quizapp/result.html', {
        'section': section,
        'score': score,
        'passed': passed
    })

@login_required
def user_progress(request):
    progress = UserProgress.objects.filter(user=request.user)
    return render(request, 'quizapp/progress.html', {'progress': progress, 'passing':passing})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect('login')  
        else:
            messages.error(request, "Please correct the errors below.") 
    else:
        form = CustomUserCreationForm()

    return render(request, 'quizapp/register.html', {'form': form})

@login_required
def create_course_quizzes_sections(request):
    course_form = CourseForm(request.POST or None, request.FILES or None)
    quiz_formset = QuizFormSet(request.POST or None, queryset=Quiz.objects.none())
    section_formset = SectionFormSet(request.POST or None, queryset=Section.objects.none())
    question_formset = QuestionFormSet(request.POST or None, queryset=Question.objects.none())

    if request.method == 'POST':
        if all([course_form.is_valid(), quiz_formset.is_valid(), section_formset.is_valid(), question_formset.is_valid()]):
            course = course_form.save()

            for quiz_form in quiz_formset:
                quiz = quiz_form.save(commit=False)
                quiz.course = course
                quiz.save()

            for section_form in section_formset:
                section = section_form.save(commit=False)
                section.save()

            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.save()

            return redirect('home')  

    context = {
        'course_form': course_form,
        'quiz_formset': quiz_formset,
        'section_formset': section_formset,
        'question_formset': question_formset,
    }
    return render(request, 'quizapp/forms/create_all.html', context)