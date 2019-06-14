from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Control(models.Model):
    parent_id = models.IntegerField()

    def __str__(self):
        return 'Project(id=' + str(self.id) + ', content=' + str(self.text) + ')'


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project")
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    control = models.ManyToManyField(Control)

    def __str__(self):
        return 'Project(id=' + str(self.id) + ', name=' + str(self.name) + ')'

