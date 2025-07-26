from django.shortcuts import render
from .models import Student
from django.http import HttpResponse


# Create your views here.
def landing(req):
    return render(req,'landing.html')
def register(req):
    return render(req,'landing.html',{'register1':'register'})
def registerdata(req):
    if req.method=="POST":
        name =req.POST.get('name') 
        e = req.POST.get('email') 
        c = req.POST.get('contact') 
        i=req.FILES.get('image') 
        d= req.FILES.get("document") 
        p=req.POST.get('pass')
        cp=req.POST.get('cpass')
        data=Student.objects.filter(email=e)
        if data:
            msg="email already exists"
            return render (req,'landing.html',{'msg':msg,'registration':'registration'})
        else:
            if p==cp:
                Student.objects.create(firstname=name,email=e,contact=c,image=i,document=d,password=p)
                msg="Registration Done"
                return render(req,'login.html',{'login':'login'})
            else:
                msg='password and confirm password not matched'
                return render(req,'landing.html',{'msg':msg})
def login(req):
    if req.method=='POST':
        e=req.POST.get('email')
        p=req.POST.get('pass')
        dataa=Student.objects.filter(email=e)
        if dataa:
            user=Student.objects.get(email=e)
            passs=user.password
            if passs==p:
                dataa={'name':user.firstname,'email':user.email,'conatct':user.contact,'image':user.image,'document':user.document,'password':user.password}
                return render(req,'dashboard.html',{'dataa':dataa})
            else:
                err='email and pass do not match'
                return render(req,'login.html',{'err':err})
        else:
            emr='email does not exist, kindly register'
            return render(req,'registration.html',{'emr':emr})
        
def dashboard(req):
    return render(req,'dashboard.html')

    # we use filter in login as we want empty output in order to print the error message if we take get then code will not be read and error will be displayed
        # print(name,e,c,i,d,sep=",")
        # Student.objects.create(firstname=name,email=e,contact=c,image=i,document=d)
        # return HttpResponse("registration done")

        