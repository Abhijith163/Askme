from django.shortcuts import render,HttpResponse,redirect
from . forms import RegistrationForm,LoginForm,QuestionForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Like, Question, Answer
from django.http import JsonResponse
from django.contrib import auth

# Create your views here.
def index(request):
    return render(request,'index.html')


def registraion(request):
    if request.method == "POST":
        user_form=RegistrationForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            auth.login(request,user)
            return redirect('/home')
    else:
        user_form=RegistrationForm()
    return render(request,'registration.html',{'user_form':user_form})


def User_login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd["username"],password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return  redirect('h')
            else:
                return HttpResponse("<h1> user not found </h1>")
    else:
        form=LoginForm()
    return render(request,"login.html",{"form":form})


def home(request):
    questions = Question.objects.order_by('-created_at').all()
    context = {
        'questions': questions
    }
    return render(request,'home.html', context)
    

@login_required(login_url='/login/')
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Your question has been posted successfully!')
    else:
        form = QuestionForm()
    return render(request, 'question.html', {'form': form})
       

@login_required(login_url='/login/')
def answers(request, id):
    question = Question.objects.filter(id=id)
    if question:
        question = question.get()
        answers = question.answers.all()
        context = {
            'question': question,
            'answers': answers.order_by('-created_at'),
        }
    else:
        return JsonResponse({'error': 'Question not found'})
    
    if request.POST:
        answer = request.POST.get('answer')
        question.answers.create(body=answer, user=request.user)
        messages.success(request, 'Your answer has been posted successfully!')

    return render(request,'answers.html', context)


@login_required(login_url='/login/')
def like_answer(request, id):
    answer = Answer.objects.filter(id=id)
    if not answer:
        return JsonResponse({'error': 'Answer not found'})
    
    answer = answer.get()

    liked_by_user = Like.objects.filter(user=request.user, answer=answer)

    if liked_by_user:
        liked_by_user.delete()
    else:
        Like.objects.create(user=request.user, answer=answer)

    return redirect('/answers/'+str(answer.question.id))


def logout_user(request):
    logout(request)
    return redirect('/')