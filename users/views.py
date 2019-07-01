
import json

from users.models import Expert
from users import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xlrd #excel读工具
# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import BaseUser,Student
from .forms import RegisterForm,LoginForm,ModifyPwdForm

class UserBackend(ModelBackend):
    """
    BaseUser authentication backend
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = BaseUser.objects.get(Q(username=username)|Q(email=username),Q(type=kwargs.get('user_type','')))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    """
    学生注册
    """
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{'register_form':register_form})

    def post(self,request):
        re_dict = dict()
        dataPOST = json.loads(request.body)
        dataPOST['birthdate'] = dataPOST['birthdate'][0:10]
        dataPOST['enroll_time'] = dataPOST['enroll_time'][0:10]
        register_form = RegisterForm(dataPOST)
        if register_form.is_valid():
            email = dataPOST.get('email','')
            if Student.objects.filter(user__email=email):
                re_dict['msg'] = False
                re_dict['detail'] = '该邮箱已注册'
                return JsonResponse(re_dict,safe=False)
                # return render(request, "register.html",{"register_form": register_form, "msg": "该邮箱已注册"})
            password = dataPOST.get('password','')

            #创建BaseUser对象
            baseuser = BaseUser()
            baseuser.username = dataPOST.get('stu_id','')
            baseuser.password = make_password(password)
            baseuser.type = 1
            baseuser.email = email
            baseuser.save()

            #创建Student对象
            student = Student()
            student.user = baseuser
            student.stu_id = dataPOST.get('stu_id','')
            student.name = dataPOST.get('name','')
            student.department = dataPOST.get('department','')
            student.major = dataPOST.get('major','')
            student.enroll_time = dataPOST.get('enroll_time','')
            student.phone = dataPOST.get('phone','')
            student.birthdate = dataPOST.get('birthdate','')
            student.degree = dataPOST.get('degree','')
            student.address = dataPOST.get('address','')
            student.save()
            re_dict['msg'] = True
            return JsonResponse(re_dict, safe=False, status=200)
            # return HttpResponse(status=200)
            # return render(request,'login.html')

        else:
            re_dict['msg'] = False
            re_dict['detail'] = '表单验证失败'
            return JsonResponse(re_dict,safe=False,status=200)
            # return render(request,'register.html',{"register_form":register_form})
            # return HttpResponse(status=403)


class LoginView(View):
    """
    用户登录
    """
    def get(self,request):
        return render(request,'login.html',{})

    def post(self,request):
        dataPOST = json.loads(request.body)
        login_form = LoginForm(dataPOST)
        re_dict = dict()
        if login_form.is_valid():
            username = dataPOST.get('username','')
            password = dataPOST.get('password','')
            user_type = dataPOST.get('type','')
            user = authenticate(username=username,password=password,user_type=user_type)
            if user is not None:
                login(request,user)
                re_dict['msg'] = True
                return JsonResponse(re_dict, safe=False, status=200)
            else:
                re_dict['msg'] = False
                return JsonResponse(re_dict,safe=False,status=200)
        else:
            re_dict['msg'] = False
            return JsonResponse(re_dict, safe=False, status=200)
            # return HttpResponse(status=400)
            # return render(request,'login.html',{'login_form':login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reversed('index'))

class UpdatePwdView(View):
    """
    用户在个人中心修改密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
           pwd1 = request.POST.get('pwd1','')
           pwd2 = request.POST.get('pwd2','')
           if pwd1 != pwd2:
               return HttpResponse("{'status':'fail','msg':'密码不一致'}",content_type='application/json')
           user = request.user
           user.password = make_password(pwd2)
           user.save()
           return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')


class SearchStudent(View):
    """
    模糊查找学生
    """
    def get(self,request):
        query = request.query_params.get('query_str','')
        query_set = Student.objects.filter(Q(stu_id__contains=query)|Q(name__contains=query))[:5]
        stu_dict = dict()
        stu_dict['stu'] = query_set
        return JsonResponse(stu_dict,safe=False)
class ExpertManage():
    @csrf_exempt
    # 展示专家列表，允许上传文件添加专家，当和数据库中的专家邮箱重复时跳过
    def list(request):
        experts = Expert.objects.all()
        total = len(experts)
        paginator = Paginator(experts, 15)  # 每页15条
        list = paginator.page(1)
        page = request.GET.get('page')
        try:
            list = paginator.page(page)  # list为Page对象！
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            list = paginator.page(paginator.num_pages)

        if request.method == 'POST':
            f = request.FILES.get('file')
            excel_type = f.name.split('.')[1]
            if excel_type in ['xlsx', 'xls']:
                # 开始解析上传的excel表格
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                table = wb.sheets()[0]
                rows = table.nrows  # 总行数
                # 要求导入的表必须是按照邮箱、姓名、领域的顺序存储，第一行是表头，不读入数据库
                for i in range(1, rows):
                    try:
                        # with transaction.atomic():  # 控制数据库事务交易
                        rowVlaues = table.row_values(i)
                        # major = models.Expert.objects.filter(name=rowVlaues[0]).first()
                        email = rowVlaues[0]
                        user = models.BaseUser.objects.create(type=3, email=email, username=email, password=email)
                        models.Expert.objects.create(user=user, name=rowVlaues[1], field=int(rowVlaues[2]))
                    except Exception as e:
                        print('解析excel文件或者数据插入错误')
                        print(e)
                        pass
                return render(request, 'expert-manage.html', {'message': '导入成功'})
            else:
                print('上传文件类型错误！')
                return render(request, 'expert-manage.html', {'message': '导入失败'})
        return render(request, "expert-manage.html", {'data': list, 'total':total})

    @csrf_exempt
    def expert_detail(request):
        # 修改专家信息时先获取原来的专家信息
        if request.method == 'POST':
            id = request.POST.get('id')
            print(id)
            expert_detail = models.Expert.objects.get(user_id=id)
            email = expert_detail.user.email
            name = expert_detail.name
            field = expert_detail.field

            return JsonResponse({'id': id, 'name': name, 'field': field, 'email':email})
        return JsonResponse({'message':"获取专家信息"})

    @csrf_exempt
    def change(request):
        # 修改专家信息
        if request.method == 'POST':
            id = request.POST.get('id')
            changed_email = request.POST.get('changed_email')
            changed_name = request.POST.get('changed_name')
            changed_field = request.POST.get('changed_field')
            try:
                expert = models.Expert.objects.get(user_id=id)
                user = models.BaseUser.objects.get(id=id)
                user.email = changed_email
                expert.name = changed_name
                expert.field = changed_field
                user.save()
                expert.save()
            except:
                return JsonResponse({'Message': "修改失败"})
            return JsonResponse({'Message': "修改成功"})
        return JsonResponse({'message': "修改专家信息"})

    @csrf_exempt
    def delete_expert(request):
        # 删除专家信息
        if request.method == 'POST':
            id = request.POST.get('id')
            try:
                models.Expert.objects.get(user_id=id).delete()
            except:
                return JsonResponse({'Message': "删除失败"})
            return JsonResponse({'Message': "删除成功"})
        return JsonResponse({'Message': "删除专家信息"})



def page_not_found(request,exception):
    """
    全局404处理函数
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

def page_error(request):
    """
    全局500处理函数
    :param request:
    :return:
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response