"""TopCup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
import competition.views as Cpt
import techworks.views as Tch
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('competitiondetail/', Cpt.CompetitionDetail),
    path('competitionlist/', Cpt.CompetitionList),
    path('techworklist/', Tch.TechWorkListView.as_view()),
    path('techworksubmit/', Tch.TechWorkView.as_view()),
    re_path(r'^favicon.ico',RedirectView.as_view(url=r'/static/favicon.ico')),
]
