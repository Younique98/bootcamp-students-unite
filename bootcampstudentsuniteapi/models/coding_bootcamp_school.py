from django.db import models


class CodingBootcampSchool(models.Model):

    school_name = models.CharField(max_length=50)
