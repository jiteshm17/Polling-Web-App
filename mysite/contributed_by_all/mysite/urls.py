from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register,results, result_detail, result_festival, result_trip, result_timetable, result_events ,result_sports, result_hostel, result_academics, result_general, owners,question_events,question_timetable,question_trip,question_festival, question_academics,question_sports,question_hostel, questions, question_add, question_detail, question_general

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^owners/', owners, name='owners'),
    url(r'^register/', register, name='regist',),
url(r'^questions/$', questions, name='questions',),
url(r'^results/$', results, name='results',),


url(r'^question-add/$', question_add, name='questions-add',),
url(r'^questions/(?P<q_id>[0-9]+)/$', question_detail, name='questions-detail',),
url(r'^results/(?P<q_id>[0-9]+)/$', result_detail, name='result-detail',),


url(r'^questions/general/$', question_general, name="general"),
url(r'^results/general/$', result_general, name="general2"),

url(r'^questions/academics/$', question_academics, name="academics"),
url(r'^results/academics/$', result_academics, name="academics2"),

url(r'^questions/hostel/$', question_hostel, name="hostel"),
url(r'^results/hostel/$', result_hostel, name="hostel2"),

url(r'^questions/sports/$', question_sports, name="sports"),
url(r'^results/sports/$', result_sports, name="sports2"),

url(r'^questions/events/$', question_events, name="events"),
url(r'^results/events/$', result_events, name="events2"),

url(r'^questions/timetable/$', question_timetable, name="timetable"),
url(r'^results/timetable/$', result_timetable, name="timetable2"),

url(r'^questions/trip/$', question_trip, name="trip"),
url(r'^results/trip/$', result_trip, name="trip2"),

url(r'^questions/festival/$', question_festival, name="festival"),
url(r'^results/festival/$', result_festival, name="festival2"),
]