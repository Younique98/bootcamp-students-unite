from django.db import models
from django.contrib.auth.models import User


def upload_to(instance, filename):
    print(instance)
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"users/13/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class BootCampGraduate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    bootcamp_graduate_image = models.ImageField(
        upload_to=upload_to, blank=True)
