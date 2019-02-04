from django.urls import path
from .views import *

app_name = "issues"

urlpatterns = [
    path('list/',issuesList,name="Issues list"),
    path('create/',createIssue,name="Create issue"),
    path('issuedetail/',issuedetail,name="Issues detail"),
    path('postcomment/',postcomment,name="Post comment"),
    path('upvote/',upvoteissue,name="Upvote issue"),
    path('closeissue/',closeissue,name="Close issue"),
    path('reopenissue/',reopenissue,name="Reopen issue"),
    path('assignedtome/',assignedtome,name="Assigned to me"),
    path('myissues/',myissues,name="My issues")
]