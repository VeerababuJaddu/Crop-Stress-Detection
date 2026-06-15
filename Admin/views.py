from django.shortcuts import render
from django.contrib import messages
from Users.models import UserRegistrationModel

# Create your views here.

def adminHome(request):
    return render(request,'admin/adminHome.html')

def adminLoginCheck(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        if username=='admin' and password=='admin':
            return render(request,'admin/adminHome.html')
        else:
            messages.error(request,'Invalid credintials')
            return render(request,'adminLogin.html')
def userDetails(request):
    data=UserRegistrationModel.objects.all()
    return render(request,'admin/userView.html',{'data':data})

def activateUser(request):
    id=request.GET['uid']
    usu=UserRegistrationModel.objects.get(id=id)
    if usu.status=='waiting':
        usu.status="activated"
        usu.save()

        data=UserRegistrationModel.objects.all()
        return render(request,'admin/userView.html',{'data':data})
def deleteUser(request):
    id=request.GET['uid']
    usu=UserRegistrationModel.objects.get(id=id)
    usu.delete()

    data=UserRegistrationModel.objects.all()
    return render(request,'admin/userView.html',{'data':data})

    