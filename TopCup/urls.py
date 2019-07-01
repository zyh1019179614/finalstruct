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
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.csrf import csrf_exempt

from users.views import LoginView,LogoutView,UpdatePwdView,RegisterView

from users.views import ExpertManage

import competition.views as Cpt
urlpatterns = [
    path('admin/', admin.site.urls),
    path('competitiondetail/', Cpt.CompetitionDetail),
    path('competitionlist/', Cpt.CompetitionList),
    path('expert/', ExpertManage.list),
    path('expert_detail/', ExpertManage.expert_detail),
    path('expert_change/', ExpertManage.change),
    path('expert_delete/', ExpertManage.delete_expert),

    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',csrf_exempt(RegisterView.as_view()),name='register'),
    path('update/pwd/',UpdatePwdView.as_view(),name='update_pwd'),
    #re_path(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),
]

#urlpatterns += staticfiles_urlpatterns()


#全局404&500页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
