from django.shortcuts import render,redirect
from .models import Student
from django.http import HttpResponse
from django.urls import reverse
from urllib import urlencode


# Create your views here.
def landing(req):
    return render(req,'landing.html')

def register(req):
    if req.method=="POST":
        name =req.POST.get('name') 
        e = req.POST.get('email') 
        c = req.POST.get('contact') 
        i=req.FILES.get('image') 
        d= req.FILES.get("document") 
        p=req.POST.get('password')
        cp=req.POST.get('cpass')
        data=Student.objects.filter(email=e)
        if data:
            eme="email already exists"
            return render (req,'registration.html',{'eme':eme,'registration':'registration'})
        else:
            if p==cp:
                Student.objects.create(firstname=name,email=e,contact=c,image=i,document=d,password=p)
                rdn="Registration Done"
                return redirect('login')
            else:
                perr='password and confirm password not matched'
                return render(req,'registration.html',{'perr':perr})
    return render(req,'registration.html')

def login(req):
   
    if req.method=='POST':
        e=req.POST.get('email')
        p=req.POST.get('password')
        
        dataa=Student.objects.filter(email=e)
        if dataa:
            user=Student.objects.get(email=e)
            passs=user.password
            if passs==p:
                dataa={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
                # reverse method and url encode method for taking data of user to dashboard
                return redirect('dashboard') 
            else:
                err='email and pass do not match'
                return render(req,'login.html',{'err':err,'email':e})
        else:
            emr='email does not exist, kindly register'
            return render(req,'registration.html',{'emr':emr})
    else:
        return render(req,'login.html')
        
def dashboard(req):
    return render(req,'dashboard.html')

    # we use filter in login as we want empty output in order to print the error message if we take get then code will not be read and error will be displayed
        # print(name,e,c,i,d,sep=",")
        # Student.objects.create(firstname=name,email=e,contact=c,image=i,document=d)
        # return HttpResponse("registration done")

        