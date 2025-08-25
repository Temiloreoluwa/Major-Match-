from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import User, Question, CareerPath, UserResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import QuestionForm
from collections import defaultdict


def career_quiz(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    questions = Question.objects.all()

    if request.method == 'POST':
        form = QuestionForm(request.POST, questions=questions)
        if form.is_valid():
            # Clear any previous responses by this user
            UserResponse.objects.filter(user=request.user).delete()

            for field_name, value in form.cleaned_data.items():
                question_id = int(field_name.split('_')[1])
                UserResponse.objects.create(
                    user=request.user,
                    question_id=question_id,
                    answer=value == 'True'
                )
            return redirect('career_result', request.user)  # No session_id needed
    else:
        form = QuestionForm(questions=questions)

    return render(request, 'core/career_quiz.html', {'form': form})


def career_result(request, user):
    responses = UserResponse.objects.filter(user=request.user)
    scores = defaultdict(int)
    
    for response in responses:
        if response.answer:
            scores[response.question.career_path] += 1

    if scores:
        best_path = max(scores, key=scores.get)
    else:
        best_path = None
    
    return render(request, 'core/career_result.html', {'best_path': best_path})


def index(request):

    return render(request, "core/index.html")



@login_required
def quiz_view(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        # Answer.objects.create(user=request.user, question=questions.first(), value=user_input)
        return redirect('quiz_results')  # Replace with your results view
   

    return render(request, 'core/quiz.html')




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def signup_step1(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        middlename = request.POST.get('middlename')
        lastname = request.POST.get('lastname')
        number = request.POST.get('number')
        email = request.POST.get('email')
        date = request.POST.get('date')

        # Save in session for step 2
        request.session['signup_step1'] = {
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'number': number,
            'email': email,
            'date': date,
        }

        return redirect('signup_step2')

    return render(request, 'core/signup_step1.html')

def signup_step2(request):
    step1_data = request.session.get('signup_step1')

    if not step1_data:
        return redirect('signup_step1')
    
    if request.method == 'POST':
        uniname = request.POST.get('uniname')
        studyyear = request.POST.get('studyyear')
        course = request.POST.get('course')
        skill = request.POST.get('skill')
        speciality = request.POST.get('speciality')
        goal = request.POST.get('goal')

        # Combine all data
        request.session['signup_step2'] = {
            **step1_data,
            'uniname': uniname,
            'studyyear': studyyear,
            'course': course,
            'skill': skill,
            'speciality': speciality,
            'goal': goal,

        }

        # Clear session and redirect
        del request.session['signup_step1']

        return redirect('register')

    return render(request, 'core/signup_step2.html')


def register(request):
    step2_data = request.session.get('signup_step2')

    if not step2_data:
        return redirect('signup_step2')
    
    full_data = {
            **step2_data
        }
    
    print(full_data)  # Debugging line to check data flow
    first_name = full_data.get('firstname', '')
    middle_name = full_data.get('middlename', '')
    last_name = full_data.get('lastname', '')
    number = full_data.get('number', '')
    date_of_birth = full_data.get('date', '')
    uni_year = full_data.get('studyyear', '')
    course = full_data.get('course', '')
    skill = full_data.get('skill', '')
    speciality = full_data.get('speciality', '')
    goal = full_data.get('goal', '')

    
    if request.method == "POST":
        username = request.POST["username"]
        email = full_data["email"]


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "core/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, 
                email, 
                password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                number=number,
                date_of_birth=date_of_birth,
                uni_year=uni_year,
                course=course,
                skill=skill,
                speciality=speciality,
                goal=goal
            )
            user.save()
        except IntegrityError:
            return render(request, "core/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "core/register.html")
    

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    # answers = Answer.objects.filter(user=user)
    # recommendations = AIRecommendation.objects.filter(user=user).order_by('-created_at')


    context = {
        'user': user,
        # 'answers': answers,
        # 'recommendations': recommendations,
    }
    
    return render(request, 'core/profile.html', context)