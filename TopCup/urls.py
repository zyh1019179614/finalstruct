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
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

import competition.views as Cpt
import operation.views as Opt
import techworks.views as Tch
from TopCup import settings
from operation.views import AssignWorkListView, AssignExpertView, DefenseWorkListView, InvitationView
from operation.views import ExptreviewListView, ExptTreetableView
from operation.views import ReassignExpertView
from users.views import ExpertManage, ExpertInitPasswd
from users.views import LoginView, LogoutView, UpdatePwdView, RegisterView

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path('competitiondetail/', Cpt.CompetitionDetail),
    path('', Cpt.CompetitionList),
    path('index/', Cpt.CompetitionList),
    path('competitionlist/', Cpt.CompetitionList),
    path('workdefensechange/',Cpt.WorkdefenseChange),
    path('techworklist/', Tch.TechWorkListView.as_view()),
    path('techworksubmit/', Tch.TechWorkView.as_view()),
    path('generatepdf/',Tch.generatePdf),
    path('stusearch/',Tch.searchstu),
    path('deletework/',Tch.deletework),
    re_path(r'^favicon.ico',RedirectView.as_view(url=r'/static/favicon.ico')),
    path('competitionlist/?selected=0', Cpt.CompetitionList,name='competitionlist'),
    path('deletecpt/',Cpt.DeleteCompetition),

    path('expert/', ExpertManage.list),
    path('expert_detail/', ExpertManage.expert_detail),
    path('expert_change/', ExpertManage.change),
    path('expert_delete/', ExpertManage.delete_expert),

    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/',RegisterView.as_view(),name='register'),
    path('update/pwd/',UpdatePwdView.as_view(),name='update_pwd'),
    path('cptinit/', Cpt.CompetitionInit),
    path('cptinit/cptformpost/',Cpt.CompetitionFormPost),
    path('cptchange/', Cpt.CompetitionChange),
    path('cptchange/cptchangepost/', Cpt.CompetitionChangePost),
    # path('expert_review/',ExpertReviewView.as_view(),name='expertReview_View'),

    path('reviewworklist/', Opt.ExpertReviewListView.as_view()),
    path('downloadZip/', Opt.DownLoadZip),
    path('downloadBatchZip/',Opt.DownloadBatchZip),
    path('judge/', Opt.Judge),
    path('submitReview/',Opt.sumbitReview),
    path('nextReviewWork/',Opt.NextReviewWork),


    path('work_list/', Opt.ExpertReviewListView.as_view()),
    path('work_review/', Opt.ExpertReviewView.as_view()),
    #re_path(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    path('check_work/', Opt.CheckWorkListView.as_view()),
    path('check_work/work_info/', Tch.work_info),
    path('check_work/check_info/', Tch.checkWork),

    path('assign_work/', AssignWorkListView.as_view()),
    path('assign_expert/', AssignExpertView.as_view()),

    path('defense_work/', DefenseWorkListView.as_view()),
    path('exptreview_list/', ExptreviewListView.as_view()),
    path('review_exptree/', ExptTreetableView.as_view()),

    path('final_result/', Cpt.CompetitionFinalResult.as_view()),
    path('reassign_expet/', ReassignExpertView.as_view()),
    path('expertpasswdinit/', ExpertInitPasswd),

    path('invitation/', InvitationView.as_view())
]

#urlpatterns += staticfiles_urlpatterns()


#全局404&500页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
