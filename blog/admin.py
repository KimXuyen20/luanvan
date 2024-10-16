from django.contrib import admin
from .models import Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = {'blog_name', ' description', 'images', 'create_date'}

admin.site.register(Blog)