from django.urls import path
from .views import *

app_name = "common"

urlpatterns = [
    path('login/',LoginView.as_view(),name="Login"),
    path('logout/',logout,name="Log out"),
    path('signup/',signup,name="Sign up"),
    path('dashboard/',dashboard,name="Dashboard")
]