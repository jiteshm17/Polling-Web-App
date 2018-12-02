#simplebettethancomplex start

"""from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    STUDENT = 1
    TEACHER = 2
    SUPERVISOR = 3
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
        (SUPERVISOR, 'Supervisor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    """
#simplebettethancomplex end

from django.contrib.auth.models import User
from django.db import models

class UserProfileModel(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=(('M','Male'),('F','Female')), blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class QuestionTable(models.Model):
    question_text = models.CharField(max_length=100, blank=False)
    question_text_undrscr= models.CharField(max_length=100, blank=False)
    gender = models.CharField(max_length=1, choices=(('M','Male'),('F','Female'),('A','All')), blank=False, default='A')
    category = models.CharField(max_length=20, choices=(('ACADEMICS', 'ACADEMICS'), ('HOSTEL', 'HOSTEL'),('SPORTS','SPORTS'),('TIMETABLE','TIMETABLE'),('EVENTS','EVENTS'),('FESTIVAL','FESTIVAL'),('TRIP','TRIP'),('GENERAL','GENERAL')), default='GENERAL')
    yes_vote = models.PositiveIntegerField(default=0)
    no_vote =  models.PositiveIntegerField(default=0)
    dontcare_vote = models.PositiveIntegerField(default=0)
    confused_vote = models.PositiveIntegerField(default=0)
    dead_line = models.DateField()

    def __str__(self):
        return self.question_text

class ResponseTable(models.Model):
    question_id= models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    voter_id= models.PositiveIntegerField(blank=False)
    choice = models.PositiveIntegerField(blank=False)
    #choice 1 = yes, choice 2 = no, choice 3 = confused, choice 4 = dont care




#questions
    #text
    #text_underscore
    #deadline
    #yes
    #no
    #dont care
    #confused

#responses
    #q_id foreign key questions. on_delete. models.cascade
    #user_id
    #option (1,2,3,4)



#questions/q_id/vote
    #if request.post

        #res= responses(q_id=q_id, user_id=user.id)
        #if res is none:                               didnt vote
            #choice=request['choice']
            #append a row in responses with q_id as q.id and user_id as user.id

        #else:
            #q=questions.objectss.get(q_id=q_id)
            #if res.option==1
                #q.yes--

            #elif res.option==2/3/4:


            #if choice==yes
                #q.yes++
            #elif choice==no/confused/dont care
                #q.blah++

            #q.save

    #else:
        #render the template






