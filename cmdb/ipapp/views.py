from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

import json, re

from django import forms
from ipapp import models
from django.core.exceptions import ValidationError


def ip_validate(value):
    ip_re = re.compile(r'^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])'
                           r'\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)'
                           r'\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)'
                           r'\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$')
    if not ip_re.match(value):
        raise ValidationError('ip地址格式错误')


class LoginForm(forms.Form):
    user = forms.CharField(required=True,min_length=6,error_messages={'required': '用户名不能为空',
                                                                      'min_length': '最小长度不能小于6'})
    pwd = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空',
                                                                     'min_length':'最小长度不能小于6'})


class RegisterForm(forms.Form):
    user_r = forms.CharField(required=True,min_length=6,max_length=10,error_messages={'required': '用户名不能为空',
                                                                        'min_length': '最小长度不能小于6','max_length': '最大长度不能大于10'})
    pwd_r = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空',
                                                                       'min_length':'最小长度不能小于6'})
    pwd_rr = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空',
                                                                          'min_length': '最小长度不能小于6'})


class AddForm(forms.Form):
    ip = forms.CharField(validators=[ip_validate,],required=True,error_messages={'required': 'ip地址不能为空'},
                         widget=forms.TextInput(
                             attrs={'placeholder': 'Ip地址', 'class': 'form-control', 'id': 'inputEmail3'}))
    hostname = forms.CharField(required=True,min_length=3,error_messages={'required':'主机名不能为空',
                                                                          'min_length':'最小长度不能小于3'},
                               widget=forms.TextInput(
                                   attrs={'placeholder': '主机名称', 'class': 'form-control', 'id': 'inputEmail3'}))
    fn = forms.CharField(required=True, min_length=2, error_messages={'required': '主机功能不能为空',
                                                                                      'min_length': '最小长度不能小于2'},
                         widget=forms.TextInput(attrs={'placeholder':'主机功能','class':'form-control','id':'inputEmail3'}))


def auth(func):
    def inner(request, *args, **kwargs):
        user = request.session.get('user', None)
        if not user:
            return redirect('/home/')
        return func(request, *args, **kwargs)
    return inner


def auth1(func):
    def inner(request, p1, *args, **kwargs):
        user = request.session.get('user', None)
        if not user:
            return redirect('/home/')
        return func(request, p1, *args, **kwargs)
    return inner


def home(request):
    user = request.session.get('user',None)
    return render(request, 'home.html',{'user':user})


def auth_login(request):
    if request.POST:
        obj = LoginForm(request.POST)
        result = {'status': False, 'message': None, 'pwd_status': True}
        if obj.is_valid():
            user = request.POST.get('user')
            pwd = request.POST.get('pwd')
            ret = models.UserInfo.objects.filter(user=user)
            if user == ret[0].user and pwd == ret[0].passwd:
                result['status'] = True
                request.session['user'] = 'sunyang'
            else:
                result['message'] = '用户名或密码错误'
                result['pwd_status'] = False
        else:
            result['message'] = json.loads(obj.errors.as_json())
        return HttpResponse(json.dumps(result))
    return redirect('/home/')


@auth
def logout(request):
    del request.session['user']
    print('aaaaa')
    return redirect('/home/')


@auth
def add(request):
    user = request.session.get('user', None)
    if request.POST:
        obj = AddForm(request.POST)
        if obj.is_valid():
            result = obj.clean()
            ret = models.IpInfo.objects.filter(ip=result['ip'])
            if ret:
                message = 'ip已经存在，请重新输入'
                return render(request,'add.html',{'user': user,'obj': obj, 'error':message})
            else:
                obj = AddForm()
                models.IpInfo.objects.create(ip=result['ip'],hostname=result['hostname'],fn=result['fn'],user_id=models.UserInfo.objects.get(user=user))
                message = '[%s] 主机添加成功'%result['ip']
        return render(request,'add.html',{'user':user,'obj': obj, 'error': message})
    else:
        obj = AddForm()
        return render(request,'add.html',{'user':user,'obj':obj})


@auth
def modify(request, p1):
    user = request.session.get('user', None)
    if request.POST:
        obj = AddForm(request.POST)
        result = {'status': False, 'message': None, 'pwd_status': True}
        if obj.is_valid():
            result = obj.clean()
            print(obj)
            models.IpInfo.objects.filter(ip=result['ip']).update(hostname=result['hostname'], fn=result['fn'],
                                         user_id=models.UserInfo.objects.get(user=user))
            result['status'] = True
        else:
            result['message'] = json.loads(obj.errors.as_json())
        return HttpResponse(json.dumps(result))
    else:
        ip_list = models.IpInfo.objects.all().values('ip','hostname','fn','user_id__user')
        print(ip_list)
        fy_num = divmod(len(ip_list),8)
        if fy_num[1] == 0:
            num = fy_num[0]
        else:
            num = fy_num[0]+1
        p1 = int(p1)
        start = (p1 - 1 ) * 8
        end = p1 * 8
        user_list = ip_list[start:end]
        return render(request,'modify.html',{'user_list':user_list,'fy_num':list(range(1,num+1)),'user':user})
    # return render(request,'modify.html',{'user':user})


@auth
def select(request):
    user = request.session.get('user', None)
    return render(request,'select.html',{'user':user})


def auth_register(request):
    if request.POST:
        obj = RegisterForm(request.POST)
        result = {'status': False, 'message': None, 'pwd_status': True}
        if obj.is_valid():
            user_r = request.POST.get('user_r')
            pwd_r = request.POST.get('pwd_r')
            pwd_rr = request.POST.get('pwd_rr')
            ret = models.UserInfo.objects.filter(user=user_r)
            if ret:
                result['message'] = '用户已存在'
                result['pwd_status'] = False
            else:
                if pwd_r == pwd_rr:
                    models.UserInfo.objects.create(user=user_r, passwd=pwd_r)
                    result['status'] = True
                    request.session['user'] = user_r
                else:
                    result['message'] = '两次输入的密码不一致'
                    result['pwd_status'] = False
        else:
            result['message'] = json.loads(obj.errors.as_json())
        return HttpResponse(json.dumps(result))
    return redirect('/home/')