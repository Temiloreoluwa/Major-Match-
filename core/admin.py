

# Register your models here.
from django.contrib import admin
from .models import Question, User, CareerPath, UserResponse

admin.site.register(Question)
admin.site.register(CareerPath)
admin.site.register(User)
admin.site.register(UserResponse)