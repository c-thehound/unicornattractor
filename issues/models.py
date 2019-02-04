from django.db import models
from common.models import User,Technician
import datetime

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=200,blank=True,primary_key=True)
    reporter = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000,blank=False)
    detail = models.TextField(blank=False)
    created = models.DateField(blank=False,default=datetime.date.today)
    ISSUE_TYPES = (
        ("BUG","BUG"),
        ("FEATURE","FEATURE")
    )

    _type = models.CharField(max_length=200,choices=ISSUE_TYPES,blank=False,default="BUG")
    STATUSES = (
        ("OPEN","OPEN"),
        ("REOPEN","REOPEN"),
        ("CLOSED","CLOSED")
    )

    status = models.CharField(max_length=100,choices=STATUSES,blank=False,default="OPEN")
    URGENCY_TYPES = (
        ("LOW","LOW"),
        ("MEDIUM","MEDIUM"),
        ("HIGH","HIGH")
    )
    urgency = models.CharField(choices=URGENCY_TYPES,blank=False,max_length=200,default="MEDIUM")
    attempted_solution = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="Assignee")
    date_closed = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    commentor = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    ref = models.ForeignKey(Ticket,on_delete=models.CASCADE,null=True)
    detail = models.TextField(blank=False)
    created = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.ref.title

class Vote(models.Model):
    issue = models.ForeignKey(Ticket,on_delete=models.CASCADE,null=True)
    voter = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.issue.title





