from django.db import models

# Create your models here.
from accounts.models import Account, UserProfile  # Import UserProfile nếu bạn đã có model này

class Doctor(models.Model):
    user = models.OneToOneField(Account, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=50)
    doctor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doctor_name