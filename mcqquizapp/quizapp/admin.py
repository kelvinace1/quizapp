from django.contrib import admin
from .models import Course, Quiz, Section, Question, UserProgress

admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(UserProgress)
