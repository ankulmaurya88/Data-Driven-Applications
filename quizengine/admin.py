

from django.contrib import admin
from .models import Questiondb  # Use the correct model name

@admin.register(Questiondb)
class QuestiondbAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_title', 'category', 'difficulty_level', 'right_answer')
    search_fields = ('question_title', 'category')
    list_filter = ('category', 'difficulty_level')

# If you have more models, register them here
