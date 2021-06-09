from django.db import models


class GroupProject(models.Model):

    title = models.CharField(max_length=50)
    number_of_graduates_signed_up = models.IntegerField()
    description = models.CharField(max_length=150)
    project_manager = models.ForeignKey(
        "BootCampGraduate", on_delete=models.CASCADE)
    estimated_time_to_completion = models.CharField(max_length=50)
    github_link = models.CharField(max_length=150)
