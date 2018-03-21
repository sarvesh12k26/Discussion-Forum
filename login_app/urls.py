from django.conf.urls import url
from . import views

app_name='login_app'

urlpatterns=[
    url(r'^$',views.register,name='register'),
    url(r'^login/',views.user_login,name='login'),
    url(r'^profile/',views.profile_info,name='profile_info'),
    url(r'^question/',views.question_list,name='question_list'),
    url(r'^answer/(?P<questions_id>\d+)',views.answer_list,name='answer_list'),
]
