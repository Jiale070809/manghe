from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from app.models import Registeruser


# Create your views here.
def logins(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user=Registeruser.objects.get(reg_name=username)
            if password == user.reg_pwd:
                return redirect('/base/')
            else:
                error_msg3="密码错误"
                return render(request, 'login.html', {'error_msg3':error_msg3})
        except:
            error_msg4="用户名不存在"
            return render(request, 'login.html', {'error_msg4':error_msg4})
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        try:
            user=Registeruser.objects.get(reg_name=username)
            if user:
                msg="用户名已存在"
                return render(request,'register.html',{'msg':msg})
        except:
            if password != password2:
                error_msg="两次输入的密码不一样！"
                return render(request,'register.html',{'error_msg':error_msg})
            elif username == '':
                error_msg2="用户名不能为空"
                return render(request,'register.html',{'error_msg2':error_msg2})
            else:
                register=Registeruser()
                register.reg_name=username
                register.reg_pwd=password
                register.save()
                return redirect("/login/")
    else:
        return render(request,'register.html')


def base(request):
    return render(request,'base.html')