from django.contrib import admin
from .models import *

admin.site.register(Ticket)
admin.site.register(Vote)
admin.site.register(Comment)