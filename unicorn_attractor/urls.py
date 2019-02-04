from django.contrib import admin
from django.urls import path,re_path,include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/',include('common.urls')),
    path('issues/',include('issues.urls')),
    path('payments/',include('payments.urls'))
]
