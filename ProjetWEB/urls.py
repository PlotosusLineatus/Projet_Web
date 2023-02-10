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
from genomeBact import views

urlpatterns = [

    path('admin_django/', admin.site.urls),

    path('', views.user_login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.user_logout, name = 'logout'),
    path('home/', views.home, name = 'home'),
    path('results/', views.results, name='results'),

    # USERS #
    path('admin/', views.admin, name = 'admin'),
    path('user/<int:user_id>/', views.user_detail, name = 'user-detail'),
    path('workspace/', views.workspace, name = 'workspace'),

    # BD #
    path('sp/add/', views.genome_create, name='genome-create'),
    path('sp/<str:specie>/', views.genome_detail, name='genome-detail'),
    path('transcripts/add/', views.transcript_create, name='transcript-create'),
    path('sp/<str:specie>/<str:transcript>/', views.transcript_detail, name='transcript-detail'),
    path('download/', views.download_csv, name='download_csv'),
]
