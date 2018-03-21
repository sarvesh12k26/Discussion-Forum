from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm
from .models import UserProfileInfo,Questions,Answers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import datetime
# Create your views here.

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    return render(request,'index.html')

def register(request):
    registered=False
    if request.method == 'POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
            login(request,user)
            return HttpResponseRedirect(reverse('login_app:profile_info'))
        else:
            print(user_form.errors,profile_form.errors)
            return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
        return render(request,'register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):

    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        #print(username,password)
        user=authenticate(username=username,password=password)
        print("Hello")
        #print(str(user))
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('login_app:profile_info'))
        else:
            print('Username: {} and Password: {}'.format(username,password))
            return HttpResponse("Invalid ID and Password.")
    else:
        return render(request,'login.html',{})

def profile_info(request):
    if request.user.is_authenticated:
        user=request.user
        question=Questions.objects.all().filter(question_user=user.profile)
        answer=Answers.objects.all().filter(answer_user=user.profile)
        return render(request,'profile_page.html',{'user':user,'question':question,'answer':answer})
    else:
        return HttpResponseRedirect(reverse('login_app:login'))


def question_list(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            if request.POST['action']=='Delete':
                identity=request.POST.get('identity')
                Questions.objects.filter(id=identity).delete()
                print("Question Deletion Done")
            else:
                ques=request.POST.get("Quest")
                ques_object=Questions.objects.create(question_user=request.user.profile,
                                                    question=ques,question_time=datetime.datetime.now())
            return HttpResponseRedirect(reverse('login_app:profile_info'))
        else:
            current_user=request.user
            question=Questions.objects.all().reverse()
            return render(request,'ht3.html',{'current_user':current_user,'question':question})
    else:
        return HttpResponseRedirect(reverse('login_app:login'))

def answer_list(request,questions_id):
    print(questions_id)
    if request.user.is_authenticated:
        question=Questions.objects.get(id=questions_id)

        if request.method=='POST':
            if request.POST['action']=='Delete':
                identity=request.POST.get('identity')
                Answers.objects.filter(id=identity).delete()
                print("Answer Deletion Done")
            else:
                answe=request.POST.get("Answer")
                ans_object=Answers.objects.create(answer_user=request.user.profile,
                                                answer_to_question=question,answer=answe,answer_time=datetime.datetime.now())
            return HttpResponseRedirect(reverse('login_app:profile_info'))
        else:
            current_user=request.user
            print(current_user.username)
            print(question.question_user.user.username)
            answer=Answers.objects.all().filter(answer_to_question=question)
            answer=list(answer)
            answer=answer
            return render(request,'ht4.html',{'current_user':current_user,'question':question,'answer':answer})
