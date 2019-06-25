from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Control(models.Model):
    id = models.IntegerField(primary_key=True)
    cid = models.CharField(unique=True, max_length=10)
    gid = models.CharField(max_length=5)
    title = models.CharField(max_length=100)
    parameters = models.TextField(blank=True, null=True)  # This field type is a guess.
    properties = models.TextField(blank=True, null=True)  # This field type is a guess.
    links = models.TextField(blank=True, null=True)  # This field type is a guess.
    parts = models.TextField(blank=True, null=True)  # This field type is a guess.
    classinfo = models.CharField(max_length=32, blank=True, null=True)
    pid = models.CharField(max_length=10, blank=True, null=True)
    high = models.BooleanField()
    moderate = models.BooleanField()
    low = models.BooleanField()

    class Meta:
        managed = False ## This means that Django won't manage the lifecycle of this table
        db_table = 'controls'

    def __str__(self):
        return self.title

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="project")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=600)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    control = models.ManyToManyField(Control)

    def __str__(self):
        # return 'Project(id=' + str(self.id) + ', name=' + str(self.name) + ')'
        return self.name