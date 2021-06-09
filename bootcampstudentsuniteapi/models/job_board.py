from django.db import models


class JobBoard(models.Model):

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    job_link = models.CharField(max_length=150)
    poster = models.ForeignKey(
        "BootCampGraduate", on_delete=models.CASCADE)
