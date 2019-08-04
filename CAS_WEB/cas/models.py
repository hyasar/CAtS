from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django_mysql.models import SetTextField


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
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    # control = models.ManyToManyField(Control)

    def __str__(self):
        # return 'Project(id=' + str(self.id) + ', name=' + str(self.name) + ')'
        return self.name

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now=True)

class CSVIssue(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=False)
    updated_time = models.DateTimeField(auto_now=False)
    severity = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    cwe = models.IntegerField(blank=True)
    rule = SetTextField(
        base_field=models.CharField(max_length=32),
    )
    tool = models.CharField(max_length=32)
    location = models.TextField()
    element = models.CharField(max_length=32)
    path = models.TextField()
    line = models.IntegerField()

class XMLIssue(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=False)
    sourcefile = models.TextField()
    startLine = models.IntegerField()
    endLine = models.IntegerField()
    group = models.CharField(max_length=20)
    code = models.TextField()
    severity = models.CharField(max_length=10)
    rule = SetTextField(
        base_field=models.CharField(max_length=32),
    )

class ControlConfigure(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)
    keywords = SetTextField(
        base_field=models.CharField(max_length=32),
    )
