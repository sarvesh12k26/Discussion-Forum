from django.contrib import admin
from .models import UserProfileInfo,Questions,Answers
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Questions)
admin.site.register(Answers)
