from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import logout as django_logout
# Rest framework imports
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework import status
from  django.http import JsonResponse

from django.db.utils import *
import operator

from rest_framework.decorators import authentication_classes, permission_classes


from issues.models import *

class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key,"username":user.username,"loggedIn":True})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)



def logout(request):
    django_logout(request)
    return JsonResponse({"success":"Log out success","loggedIn":False})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password') 

    try:
        user = User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            email = email,
            username = username,
            password = password
        )

        user.save()
        new_user = authenticate(username=username,password=password)
        if new_user:
            return Response({"token": new_user.auth_token.key,"username":new_user.username,"loggedIn":True})
    except IntegrityError as e:
        return Response({"error": "A username with that name already exists"}, status=status.HTTP_400_BAD_REQUEST)



# Dashboard
@api_view(['GET'])
def dashboard(request):
    totalissues = Ticket.objects.all().count()
    bugs = Ticket.objects.filter(_type ="BUG").count()
    featurerequests = Ticket .objects.filter(_type = "FEATURE").count()
    community = User.objects.all().count()
    solved = Ticket.objects.filter(status = "CLOSED").count()
    today = datetime.date.today()
    # recentlysolved = [{} for issue in Ticket.objects.filter(status ="CLOSED").filter(date_closed__day__lte = int(today.strftime("%d") - 30) )]

    newestissues =[{
        "title":issue.title,
        "type":issue._type,
        "created":issue.created
    } for issue in Ticket.objects.all().order_by('-created')[:10]]

    topfeatures = []
    featuresdict = {}
    allfeaturerequests = Ticket.objects.filter(_type = "FEATURE")
    for feature in allfeaturerequests:
        votes = Vote.objects.filter(issue__ticket_id = feature.ticket_id).count()
        featuresdict[str(feature.title)] = votes 

    f_sort = sorted(featuresdict.items(),key = operator.itemgetter(1),reverse = True)
    d = dict(f_sort)
    for key in d:
        topfeatures.append({'title':key,"votes":d[key]})

    data = {
        'totalissues':totalissues,
        'bugs':bugs,
        "featurerequests":featurerequests,
        "community":community,
        "solved":solved,
        "latestissues":newestissues,
        "topfeatures":topfeatures[:4]
    }
    return Response(data)