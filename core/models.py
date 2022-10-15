from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length = 128, blank = True, null = True)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    phonenumber = models.CharField(max_length = 13, blank = True, null = True)


    def __str__(self):
        return f"{self.name}"


class Role(models.Model):
    rolename = models.CharField(max_length = 128, blank = True, null = True)

    def __str__(self):
        return f"{self.rolename}"


class SenderMessage(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete = models.CASCADE)
    latitude = models.FloatField(blank = True, null = True)
    longitude = models.FloatField(blank = True, null = True)
    country = models.CharField(max_length = 128, blank = True, null = True)
    street = models.CharField(max_length = 128, blank = True, null = True)
    name = models.CharField(max_length = 128, blank = True, null = True)
    area = models.CharField(max_length = 128, blank = True, null = True)
    message = models.CharField(max_length = 128, blank = True, null = True)
    isactive = models.BooleanField(default = True)
    phonenumber = models.CharField(max_length = 13, blank = True, null = True)
    
    class Types(models.TextChoices):
        High = "High", "High"
        Medium = "Medium", "Medium"
        Low = "Low", "Low"

    default_severity_level = Types.High

    severity_level = models.CharField(
        _("severity_level"), max_length=50, choices=Types.choices, default=default_severity_level
    )

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete = models.CASCADE, related_name = "users_profile")
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    sendermessage = models.ForeignKey(SenderMessage, on_delete = models.CASCADE, related_name = "user_message", blank = True, null = True)

    def __str__(self):
        return f"{self.user.username}"


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)
    sendermessage = models.ForeignKey(SenderMessage, on_delete = models.CASCADE, related_name = "sender_message", blank = True, null = True)
    numberplate = models.CharField(max_length = 128, blank = True, null = True)
    isactive = models.BooleanField(default=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=True, null=True, related_name = 'hospital_user')

    def __str__(self):
        return f"{self.drivername}"
    
    




    
    