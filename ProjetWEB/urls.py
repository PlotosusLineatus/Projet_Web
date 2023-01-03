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
    path('admin/', admin.site.urls),
    path('genomes/', views.genome_list, name = 'genome-list'),
    path('genomes/add/', views.genome_create, name='genome-create'),
    path('genomes/<str:specie>/', views.genome_detail, name='genome-detail'),
    path('genomes/<str:specie>/delete', views.genome_delete, name='genome-delete'),
    path('genomes/<str:specie>/cds', views.cds_list, name='cds-list'),
    path('genomes/<str:specie>/cds/add', views.cds_create, name='cds-create'),

]
