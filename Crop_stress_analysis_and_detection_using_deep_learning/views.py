

from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def userRegister(request):
    return render(request,'userRegister.html')

def userLogin(request):
    return render(request,'userLogin.html')

def adminLogin(request):
    return render(request,'adminLogin.html')