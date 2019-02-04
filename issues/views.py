from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework import status
from common.models import User
import datetime
from django.db.utils import *
from django.core.exceptions import *

@api_view(['GET'])
def issuesList(request):
    tickets = Ticket.objects.all()
    data = [{
        "id":issue.ticket_id,
        "title":issue.title,
        "detail":issue.detail,
        "status":issue.status,
        "creator":issue.reporter.username,
        "type":issue._type,
        "created":issue.created.strftime("%d %B %Y"),
        "assignee":issue.assigned_to.username if issue.assigned_to is not None else issue.assigned_to
    } for issue in tickets]

    return Response(data[::-1])

def generate_ticketid():
    time = datetime.datetime.now()
    tid = "TCK"+time.strftime("%m")+"-"+time.strftime("%s")
    return tid

@api_view(['POST'])
def createIssue(request):
    _reporter = User.objects.get(username = request.data.get('reporter'))
    _title = request.data.get('title')
    _detail = request.data.get('detail')
    _itype = request.data.get('type')
    _attemptedsol = request.data.get('attemptedsolution')

    try:
        newticket = Ticket.objects.create(
            ticket_id = generate_ticketid(),
            reporter = _reporter,
            title = _title,
            detail = _detail,
            _type = _itype,
            attempted_solution = _attemptedsol
        )
        newticket.save()
        
        return Response({"success":"Issue was created",
        "message":"Your issue has been created successfully",
        "tickid":newticket.ticket_id
        })

    except:
        return Response({"error":"Error while creating Issue"})


def checkifvoted(user,issue):
    hasvoted = False
    for vote in Vote.objects.filter(issue = _issue):
        if vote.voter == _voter:
            hasvoted = True
            break
        else:
            continue

@api_view(['POST'])
def issuedetail(request):
    user = User.objects.get(username = request.data.get('user'))
    # try:
    _issue = Ticket.objects.get(ticket_id = str(request.data.get('issue')))
    comments = [{
        "commentby":comment.commentor.username,
        "ref":comment.ref.ticket_id,
        "title":comment.ref.title,
        "detail":comment.detail,
        "created":comment.created,
    } for comment in Comment.objects.filter(ref = _issue )]

    hasvoted = False
    for vote in Vote.objects.filter(issue = _issue):
        if vote.voter == user:
            hasvoted = True
            break
        else:
            continue

    data = {
        "id":_issue.ticket_id,
        "title":_issue.title,
        "reporter":_issue.reporter.username,
        "detail":_issue.detail,
        "created":_issue.created,
        "type":_issue._type,
        "status":_issue.status,
        "urgency":_issue.urgency,
        "attemptedsolution":_issue.attempted_solution,
        "assignedto":_issue.assigned_to,
        "dateclosed":_issue.date_closed,
        "comments":comments,
        "votes":Vote.objects.filter(issue = _issue).count(),
        "voted":hasvoted
    }
    return Response(data)
    # except:
        # return Response({'error':'Ticket does not exist'})

@api_view(['POST'])
def postcomment(request):
    commentor = User.objects.get(username = request.data.get('user'))
    detail = request.data.get('detail')
    _ref = Ticket.objects.get(ticket_id = request.data.get('ref'))

    try:
        com = Comment.objects.create(
            ref = _ref,
            commentor = commentor,
            detail = detail
        )
        com.save()

        return Response({"success":"Submitted"})
    except:
        return Response({"error":"Comment not submitted!"})

@api_view(['POST'])
def upvoteissue(request):
    _voter = User.objects.get(username = request.data.get('user'))
    _issue = Ticket.objects.get(ticket_id = request.data.get('issue'))
    hasvoted = False
    for vote in Vote.objects.filter(issue = _issue):
        if vote.voter == _voter:
            hasvoted = True
            break
        else:
            continue
    if hasvoted:
        return Response({"error":"Has voted"})
    else:
        try:
            vote = Vote.objects.create(
                issue = _issue,
                voter = _voter
                )
            vote.save()
            return Response({"success":"Voted"})
        except:
            return Response({'error':"An error occured"})


@api_view(['POST'])
def closeissue(request):
    issue = Ticket.objects.get(ticket_id = request.data.get('issue'))
    issue.status = "CLOSED"
    issue.save(update_fields=['status'])

    return Response({"status":"CLOSED"})

@api_view(['POST'])
def reopenissue(request):
    issue = Ticket.objects.get(ticket_id =request.data.get('issue'))
    issue.status = "REOPEN"
    issue.save(update_fields=['status'])

    return Response({"status":"REOPEN"})

@api_view(['POST'])
def assignedtome(request):
    try:
        _user = User.objects.get(username = request.data.get('user'))
        _assignedtome = Ticket.objects.filter(assigned_to = _user)
        data = [{
            "title":issue.title,
            "reporter":issue.reporter.username,
            "created":issue.created.strftime("%d %B %Y"),
            "type":issue._type,
            "status":issue.status,
            "urgency":issue.urgency,
            "id":issue.ticket_id
        } for issue in _assignedtome]

        return Response(data[::-1])
    except:
        return Response({'error':'An error occured while fetching issues'})

@api_view(['POST'])
def myissues(request):
    print(request.data.get('user'))
    _user = User.objects.get(username = request.data.get('user'))
    my_issues = Ticket.objects.filter(reporter = _user)
    data = [{
        "title":issue.title,
        "assignee":issue.assigned_to.username if issue.assigned_to is not None else issue.assigned_to,
        "created":issue.created.strftime("%d %B %Y"),
        "type":issue._type,
        "status":issue.status,
        "id":issue.ticket_id
    } for issue in my_issues]

    return Response(data[::-1])