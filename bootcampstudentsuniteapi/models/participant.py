from django.db import models


class Participant(models.Model):

    bootcamp_graduate = models.ForeignKey(
        "BootcampGraduate", on_delete=models.CASCADE
    )
    group_project = models.ForeignKey(
        "GroupProject", on_delete=models.CASCADE
    )
