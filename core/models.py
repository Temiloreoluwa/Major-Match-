from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True, blank=True)
    number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    uni_year = models.CharField(max_length=60, blank=True)
    study_year = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=100, blank=True)
    skill  = models.CharField(max_length=100, blank=True)
    speciality = models.CharField(max_length=100, blank=True)
    goal = models.TextField(blank=True)

 
class CareerPath(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text
    

class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()  # True for Yes, False for No
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {'Yes' if self.answer else 'No'}"