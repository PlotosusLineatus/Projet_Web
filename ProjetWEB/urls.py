"""ProjetWEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from genomeBact.views.home import *
from genomeBact.views.users import *
from genomeBact.views.results import *
from genomeBact.views.transcripts import *

urlpatterns = [

    path('admin_django/', admin.site.urls),

    path('', user_login, name = 'login'),
    path('register/', register, name = 'register'),
    path('logout/', user_logout, name = 'logout'),
    path('home/', home, name = 'home'),
    path('results/', results, name='results'),

    # USERS #
    path('admin/', admin_, name = 'admin'),
    path('user/<int:user_id>/', user_detail, name = 'user-detail'),
    path('workspace/', workspace, name = 'workspace'),

    # BD #
    path('sp/add/', genome_create, name='genome-create'),
    path('sp/<str:specie>/', genome_detail, name='genome-detail'),
    path('transcripts/add/', transcript_create, name='transcript-create'),
    path('sp/<str:specie>/<str:transcript>/', transcript_detail, name='transcript-detail'),
]
