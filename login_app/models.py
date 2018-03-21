from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user=models.OneToOneField(User, related_name='profile')
    age=models.PositiveSmallIntegerField()
    profile_pic=models.ImageField(blank=True)

    def __str__(self):
        return self.user.username

class Questions(models.Model):
    question_user=models.ForeignKey(UserProfileInfo,related_name='questions',on_delete=models.CASCADE)
    question=models.CharField(max_length=256)
    question_time=models.DateTimeField()

    def __str__(self):
        return str(self.id)

class Answers(models.Model):
    answer_user=models.ForeignKey(UserProfileInfo,related_name='answers',on_delete=models.CASCADE)
    answer_to_question=models.ForeignKey(Questions)
    answer=models.CharField(max_length=256)
    answer_time=models.DateTimeField()

    def __str__(self):
        return str(self.id)
