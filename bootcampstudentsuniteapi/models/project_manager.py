from django.db import models


class ProjectManager(models.Model):

    boot_camp_graduate = models.ForeignKey(
        "BootCampGraduate", on_delete=models.CASCADE
    )
    group_project = models.ForeignKey(
        "GroupProject", on_delete=models.CASCADE
    )
