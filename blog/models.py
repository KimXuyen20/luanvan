from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    images = models.ImageField(upload_to='photos/blog')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_name
