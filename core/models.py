from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('user', 'user'),
        ('admin', 'admin')
    ]
    
    email =  models.EmailField(unique=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICE, default= 'user')

    class Meta:
        verbose_name_plural = 'Users'

    def clean_username(self, username):
        if CustomUser.objects.filter(username=self.username).exists():
            raise ValidationError('Username already exists')
        return username
    
class Project(TimestampModel):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

class Blogs(TimestampModel):
    CATEGORY_CHOICES = [
        ('general', 'general'),
        ('construction', 'construction')
    ]
    # PROJECT_CHOICE = [
    #     ('vrx terrace', 'vrx terrace'),
    #     ('vrx 360', 'vrx 360')
    # ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name= 'blogs', null = True, blank = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name='blogs_project')
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default= 'general')
    image = models.ImageField(upload_to='blogs/')
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)