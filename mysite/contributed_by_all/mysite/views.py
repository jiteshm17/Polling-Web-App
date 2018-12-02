from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import HttpResponseRedirect
from .models import UserProfileModel, QuestionTable, ResponseTable
from django.shortcuts import get_object_or_404
from datetime import datetime
from django import forms
from django.utils import timezone
from .forms import UserRegistrationForm, login_form, editprofile
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

import string
from django.contrib.auth.decorators import login_required
#start
#from .forms import UserForm, ProfileForm

#end
# Create your views here.

"""
{% if user.is_authenticated %}
    <h1>u need to <a href="{% url: 'login' %}">login first</h1>
{% else %}

{% endif %}

"""
def loggedin(request):
    if not request.user.is_authenticated():
        return redirect('/')

def your_view(request):
    profile = request.user.get_profile()
    return profile


def owners(request):
    return render(request, 'owners.html')

'''def questions(request):

    if not request.user.is_authenticated():
        return redirect('/')
    return render(request, 'mysite/questions.html',)
    '''


def home(request):
    if not request.user.is_authenticated():
        return render(request, 'mysite/home.html')
   # user1=request.user.id
    return render(request, 'mysite/home.html',{'gender':UserProfileModel.objects.get(user=request.user).gender})



#old home
"""def home(request):

    return render(request, 'mysite/home.html')

"""

def change_password2():
    return redirect('/change-password/')

def change_password(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method=='POST':
        #form=UserChangeForm(request.POST, instance=request.user)
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
            #return HttpResponseRedirect('/')
        else:
            #return HttpResponseRedirect('change-password/')
            form1 = PasswordChangeForm(user=request.user)
            return render(request, 'mysite/change-password.html', {'form': form1,'error':"Invalid entry!"})
    else:

        form= PasswordChangeForm(user=request.user) #inbuilt
        return render(request, 'mysite/change-password.html', {'form': form, })



def edit_profile(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method=='POST':
        #form=UserChangeForm(request.POST, instance=request.user)
        form = editprofile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form=editprofile(instance=request.user)
        return render(request, 'mysite/edit-profile.html',{'form':form,})


def question_detail(request, q_id):
    if not request.user.is_authenticated():
        return redirect('/')
    q = QuestionTable.objects.filter(id=q_id, dead_line__gte=timezone.now())
    if q.count() == 0:
        return redirect('/results/' + q_id + '/')
    question = get_object_or_404(QuestionTable, pk=q_id)
    user_gender = UserProfileModel.objects.get(user=request.user).gender
    if request.method=='POST':
        if 'choice' in request.POST:
            choice1 = request.POST['choice']
        else:
            choice1 = False

        if not choice1:
            return render(request, "mysite/question/detail.html", {"question": question,'message':'you need to select an option first'})



        else:
            choice=int(choice1)

            respones=question.responsetable_set.filter(voter_id=request.user.id)
            if respones.count()==0:

                new_response=ResponseTable(question_id=question, voter_id=request.user.id, choice=choice)
                new_response.save()

                if choice == 1:
                    question.yes_vote = question.yes_vote + 1

                elif choice == 2:
                    question.no_vote = question.no_vote + 1

                elif choice == 3:
                    question.confused_vote = question.confused_vote + 1

                elif choice == 4:
                    question.dontcare_vote = question.dontcare_vote + 1
                question.save()
                return render(request, "mysite/question/detail.html",
                              {"question": question, 'message': 'response added'})



            else:
                respones2 = question.responsetable_set.get(voter_id=request.user.id)
                prev_choice=respones2.choice
                if prev_choice==1:
                    question.yes_vote=question.yes_vote - 1

                elif prev_choice==2:
                    question.no_vote = question.no_vote - 1

                elif prev_choice==3:
                    question.confused_vote = question.confused_vote - 1

                elif prev_choice==4:
                    question.dontcare_vote = question.dontcare_vote - 1



                if choice == 1:
                    question.yes_vote = question.yes_vote + 1

                elif choice == 2:
                    question.no_vote = question.no_vote + 1

                elif choice == 3:
                    question.confused_vote = question.confused_vote + 1

                else:
                    question.dontcare_vote = question.dontcare_vote + 1

                respones2.choice=choice
                respones2.save()
                question.save()
                return render(request, "mysite/question/detail.html", {"question": question,'message':'response changed', 'form':1})

    else:
        form=0
        
        #if form ==0, then result will be seen
        #if form==1 then voting option will be seen

        if question.dead_line:
            form=1

            yes_vote=question.yes_vote
            no_vote=question.no_vote
            confused_vote=question.confused_vote
            dontcare_vote=question.dontcare_vote
            return render(request, "mysite/question/detail.html", {'user_gender':user_gender,'dontcare':dontcare_vote,'confused':confused_vote,'no':no_vote,'yes':yes_vote,'message':'form is','form':form,"question": question})
        else:
            return render(request, "mysite/question/detail.html",{'user_gender':user_gender ,'form':form})
def result_detail(request, q_id):
    if not request.user.is_authenticated():
        return redirect('/')
    q = QuestionTable.objects.filter(id = q_id, dead_line__lt=timezone.now())
    if q.count() == 0:
        return redirect('/questions/'+q_id+'/')

    question = get_object_or_404(QuestionTable, pk=q_id)
    user_gender = UserProfileModel.objects.get(user=request.user).gender
    return render(request, 'mysite/question/detail2.html',{'question':question, 'user_gender':user_gender })


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            gender=request.POST['gender']
            age=request.POST['age']
            password2=request.POST['password2']
            #otp_typed=request.POST['otp']

            password =  userObj['password']
            if password==password2:

                if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                    #1 send an otp to the user
                    #2 check if the email already has an otp
                        # if yes : update the otp, dat and all the other details that he has changed
                        # if no : simply append a new row with all his detail with otp and date
                    # render otp.html (action : some other url), and pass the email in disabled email input
                        # ask him/her to input the otp
                        # check the row with that email as the pk
                        # then check the time. redirect to register
                        # else check the otp
                            # if wrong : delete the row. redirect ot register
                            # if right : # create the user of that email of the otp database and delete the table row
                            # redirect to home
                    #create user
                    User.objects.create_user(username, email, password)
                    user = authenticate(username=username, password=password)
                    UserProfileModel.objects.create(user=user, age=age, gender=gender)
                    login(request, user)
                    return HttpResponseRedirect('/')
                    #end create user
                else:
                    return render(request, 'mysite/register.html', {'form': form,
                                                                    'error_message': 'the account with this email or username already exists, please try another one', })

            else:
                return render(request, 'mysite/register.html', {'form': form, 'error_message': 'the two passwords are not the same'})


    else:
        form = UserRegistrationForm()
    return render(request, 'mysite/register.html', {'form' : form})



def questions(request):

    if not request.user.is_authenticated():
        return redirect('/')
    g= UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count() + all_questions2.count()
    return render(request, 'mysite/questions.html', {'c':c,'all_questions':all_questions, 'all_questions2':all_questions2,})


def results(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g= UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count() + all_questions2.count()
    return render(request, 'mysite/questions2.html', {'c':c,'all_questions':all_questions, 'all_questions2':all_questions2,})


def question_general(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='GENERAL', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='GENERAL', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='GENERAL', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_general(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='GENERAL', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='GENERAL', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='GENERAL', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_academics(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='ACADEMICS', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='ACADEMICS', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='ACADEMICS', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_academics(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='ACADEMICS', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='ACADEMICS', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='ACADEMICS', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_hostel(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='HOSTEL', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='HOSTEL', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='HOSTEL', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_hostel(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='HOSTEL', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='HOSTEL', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='HOSTEL', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_sports(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='SPORTS', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='SPORTS', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='SPORTS', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_sports(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='SPORTS', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='SPORTS', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='SPORTS', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_events(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='EVENTS', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='EVENTS', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='EVENTS', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_events(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='EVENTS', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='EVENTS', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='EVENTS', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_festival(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='FESTIVAL', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='FESTIVAL', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='FESTIVAL', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_festival(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='FESTIVAL', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='FESTIVAL', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='FESTIVAL', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })


def question_trip(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='TRIP', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='TRIP', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='TRIP', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_trip(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='TRIP', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='TRIP', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='TRIP', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })




def question_timetable(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='TIMETABLE', dead_line__gte=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='TIMETABLE', dead_line__gte=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='TIMETABLE', dead_line__gte=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })
def result_timetable(request):
    if not request.user.is_authenticated():
        return redirect('/')
    g = UserProfileModel.objects.get(user=request.user).gender
    if g =="A":
       all_questions = QuestionTable.objects.filter(gender='A', category='TIMETABLE', dead_line__lt=timezone.now())

    else:
        all_questions = QuestionTable.objects.filter(gender='A', category='TIMETABLE', dead_line__lt=timezone.now())
        all_questions2= QuestionTable.objects.filter(gender=g, category='TIMETABLE', dead_line__lt=timezone.now())
        #QuestionTable.objects.all()
    c = all_questions.count()+all_questions2.count()
    return render(request, 'mysite/question/all2.html',{'c':c,'all_questions': all_questions, 'all_questions2': all_questions2, })




def login_procedure(request):
    if request.user.is_authenticated():
        return redirect('/')
    #form = login_form()
    placeholder = ""
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        placeholder = username
        if not username or not password:
            return render(request, 'registration/login.html',{'error1':'both fields are required'})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/login.html', {'error1': 'invalid information','placeholder':placeholder})
    else:
        return render(request, 'registration/login.html',{'placeholder':placeholder})
#start


#end
def purify(my_str):
	punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~|+='''
	x=my_str.lower()
	no_punct = ""
	for char in x:
	   if char not in punctuations:
		   no_punct = no_punct + char
	return(no_punct)


def question_add(request):
    if not request.user.is_authenticated():#has to be authenticated
        return redirect('/')
    if not request.user.username == "admin":#if he is authenticated, he has to be the admin
        return redirect('/')
    if request.method == 'POST':
        question_text=request.POST['question_text']
        question_text_undrscr=purify(question_text)
        gender= request.POST['gender']
        category=request.POST['category']
        yes_vote=0
        no_vote =0
        dontcare_vote = 0
        confused_vote = 0
        dead_line = request.POST['dead_line']

        if question_text=='' or gender=='' or category=='' or dead_line=='':
            return render(request, 'mysite/add-question.html',{'error':'all fields are required'})
        else:
            t = QuestionTable(gender=gender, question_text=question_text, question_text_undrscr=question_text_undrscr,category=category,yes_vote=yes_vote,no_vote=no_vote,confused_vote=confused_vote, dontcare_vote=dontcare_vote, dead_line=dead_line)
            t.save()
            return HttpResponseRedirect('/')

    else:
        return render(request, 'mysite/add-question.html')