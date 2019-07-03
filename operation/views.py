from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from competition.views import GetUserIdentitiy
from techworks.models import WorkInfo
from users.models import Expert
from .models import Review


# Create your views here.
class ReviewWorkListView(View):
    # @login_required(login_url='/login/')
    def get(self, request):
        # if request.GET.get('workid', None) is None:
        #     WorkInfo.objects.create()
        worklist_origin = WorkInfo.objects.all()[:10]
        # work = WorkInfo.objects.get(work_id='1').wo
        WORKTYPE_MAP = {
            1: "科技发明制作",
            2: "调查报告和学术论文"
        }
        FIELD_MAP = {
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
        }
        worklist_ret = []
        for work in worklist_origin:
            worklist_ret.append({
                'work_id': work.work_id,
                'first_author': work.registration.first_auth.name,
                'title': work.title,
                'work_type': WORKTYPE_MAP[work.work_type],
                'field': FIELD_MAP[work.field],
                'competition': work.registration.competition.title,
                'submitted': "已提交" if work.submitted else "暂存",
            })

        user_name, user_identity = GetUserIdentitiy(request)
        return render(request, 'reviewwork_list.html', {'worklist': worklist_ret,'useridentity':user_identity})

class ExpertReviewView():
    def list(request):
        return render(request, 'work-list.html')

    @csrf_exempt
    def show(request):
        user_name, user_identity = GetUserIdentitiy(request)
        work_id = request.GET.get('work_id')
        work = WorkInfo.objects.get(work_id=work_id)
        expert = Expert.objects.get(user__email=request.user.username)
        expert_id = expert.user.id
        # expert_id = request.GET.get('expert_id')
        try:
            review = Review.objects.filter(work=work, expert=expert)
            if len(review) > 0:
                review = review[0]
                if review.review_status == 0:  # 还没评过
                    return render(request, 'judgeWork.html',
                                  {'status': 0, 'score': 50, 'expert_id': expert_id, 'work_id': work_id,
                                   'useridentity': user_identity})
                else:  # 暂存或评价过
                    return render(request, 'judgeWork.html',
                                  {'status': review.review_status, 'score': review.score, 'comment': review.comment,
                                   'expert_id': expert_id, 'work_id': work_id, 'useridentity': user_identity})
            else:
                Review.objects.create(work=work, expert=expert, score=50, comment='', review_status=0,
                                      add_time='2019-07-02')
                return render(request, 'judgeWork.html',
                              {'status': 50, 'score': 0, 'expert_id': expert_id, 'work_id': work_id,
                               'useridentity': user_identity})
        except Exception as e:
            print(e)
            pass
    @csrf_exempt
    def judge(request):
        if request.method == 'POST':
            try:
                expert_id = request.POST.get('expert_id')
                print(expert_id)
                work_id = request.POST.get('work_id')
                score = request.POST.get('score')
                comment = request.POST.get('comment')
                status = request.POST.get('status')
                expert = Expert.objects.get(user__email=request.user.username)
                work = WorkInfo.objects.get(work_id=work_id)
                review = Review.objects.get(expert=expert, work=work)
                review.score = score
                review.comment = comment
                review.review_status = status
                review.save()
            except:
                print('评价失败')
        return render(request, 'judgeWork.html')


    def get(request):
        work_id = request.GET.get('work_id')
        expert_id = request.GET.get('expert_id')
        print(work_id, expert_id)
        try:
            review = Review.objects.get(work_id=work_id, expert_id=expert_id)
            if review.review_status == 0: #还没评过
                return JsonResponse({'status':0}, safe=False)
                # return render(request, 'judgeWork.html', {'status': 0})
            else: #暂存或评价过
                return JsonResponse({'status':review.review_status, 'score':review.score, 'comment':review.comment}, safe=False)
        except:
            Review.objects.create(work_id=work_id, expert_id=expert_id, score=0, comment='', review_status=0, add_time='2019-07-02')
            return JsonResponse({'status': 0}, safe=False)

class AssignWorkListView(View):
    """
    展示待分配作品列表
    """
    def get(self,request):
        cpt_id = request.GET.get('cpt_id','')
        worklist_origin = WorkInfo.objects.all()
        WORKTYPE_MAP = {
            1: "科技发明制作",
            2: "调查报告和学术论文"
        }
        FIELD_MAP = {
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
        }
        worklist_ret = []
        for work in worklist_origin:
            worklist_ret.append({
                'work_id':work.work_id,
                'title':work.title,
                'work_type':WORKTYPE_MAP[work.work_type],
                'field':FIELD_MAP[work.field],
            })

        expertlist_origin = Expert.objects.all()
        expertlist_ret = []
        for expert in expertlist_origin:
            expertlist_ret.append({
                'expert_id':expert.user.id,
                'name':expert.name,
                'field':FIELD_MAP[expert.field],
                'email':expert.user.email,
            })

        user_name,user_identity = GetUserIdentitiy(request)
        return render(request,'assignwork_list.html',{'expertlist':expertlist_ret,'worklist':worklist_ret,'useridentity':user_identity,'username':user_name})

class AssignExpertView(View):
    """
    待分配专家
    """
    def get(self,request):
        pass

    def post(self,request):
        work_list = request.POST.get('')