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

    path('', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('home/', views.home, name = 'home'),
    path('results/', views.results, name='results'),

    # USERS #
    path('admin_django/', admin.site.urls),
    path('admin/', views.admin, name = 'admin'),
    path('settings/', views.settings, name = 'user_settings'),
    path('validator/', views.validator, name='validator'),
    path('validator/assign', views.assign_transcript, name='assign-transcript'),
    path('validator/transcripts', views.transcript_list_state, name='transcript-state'),
    path('validator/validation', views.transcript_to_validate, name='transcript-validation'),

    path('annotator/', views.annotator, name='annotator'),
    path('annotator/transcripts', views.transcript_to_annot, name='annot-list'),

    # BD #
    path('<str:specie>/', views.genome_detail, name='genome-detail'),
    path('<str:specie>/transcripts', views.transcript_list, name='transcript-list'),
    path('<str:specie>/transcripts/add', views.transcript_create, name='transcript-create'),
    path('<str:specie>/<str:transcript>', views.transcript_detail, name='transcript-detail'),
    path('<str:specie>/<str:transcript>/annotations', views.transcript_annot, name='transcript-annot'),
]
