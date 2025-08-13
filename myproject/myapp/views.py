from django.shortcuts import render,redirect
from .models import Student,queryy
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode


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
                # url=reverse('dashboard')
                # dataa=urlencode({'id':user.id})
                # return redirect(f'{url}?{dataa}')
                req.session['id']=user.id
                url=reverse('dashboard')
                return redirect(f'{url}')
                # reverse method and url encode method for taking data of user to dashboard
                # also using redirect to avoid showing data of user in url panel
                
            else:
                err='email and pass do not match'
                return render(req,'login.html',{'err':err,'email':e})
        else:
            emr='email does not exist, kindly register'
            return redirect('registration')
    else:
        return render(req,'login.html')
        
def dashboard(req):
    data=req.session.get('id',None )
    # pk=req.GET.get('id')
    if data:
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        return render(req,'dashboard.html',{'data':data})
        # we use filter in login as we want empty output in order to print the error message if we take get then code will not be read and error will be displayed
            # print(name,e,c,i,d,sep=",")
            # Student.objects.create(firstname=name,email=e,contact=c,image=i,document=d)
            # return HttpResponse("registration done")
    else:
        return redirect('login')

# delete: key
# flush: whole session
def logout(req):
    req.session.flush()
    return redirect('landing')

def query(req):
    data=req.session.get('id',None)
    if data:
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'password':user.password}
        return render(req,'dashboard.html',{'data':data,'query':'query'})
    else:
        return redirect('login')
    
def querydata(req):
    if req.method=='POST':
        n=req.POST.get('name')
        e=req.POST.get('email')
        q=req.POST.get('query')
        queryy.objects.create(name=n,email=e,query=q)
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        return render(req,'dashboard.html',{'data':data})
    
def showqueryy(req):
    print("Hello...")
    pk=req.session['id']
    user=Student.objects.get(id=pk)
    data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
    e=user.email    
    allqueryy=queryy.objects.filter(email=e)
    return render(req,'dashboard.html',{'data':data,'allqueryy':allqueryy}) 
# " " use this cautiously in using dict to transfer data as it may cause dowloading of file when button is clicked...

def delete(req,qpk):
    data=queryy.objects.get(id=qpk)
    data.delete()
    pk=req.session['id']
    user=Student.objects.get(id=pk)
    data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
    e=user.email
    allqueryy = queryy.objects.filter(email=e)
    return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy})

def edit(req,qpk):
    olddata=queryy.objects.get(id=qpk)
    pk=req.session['id']
    user=Student.objects.get(id=pk)
    e=user.email
    allqueryy=queryy.objects.filter(email=e)
    user=Student.objects.get(id=qpk)
    data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
    return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy})

    

def update(req,qpk):
    if req.method=='POST':
        oldata=queryy.objects.get(id=qpk)
        updated_query=req.POST.get('query')
        oldata.query=updated_query
        oldata.save()
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        e=user.email
        allqueryy=queryy.objects.filter(email=e)
        return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy})
def search(req):
    if req.method=='POST':
        search_value=req.POST.get('search')
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        e = user.email
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        # allqueryy=queryy.objects.filter(query__icontains=search_value,email__icontains=e) # (,) comma depicts and operations
        # for or operations we have imported Q from django.db.models
        allqueryy=queryy.objects.filter((Q(query__icontains=search_value)| Q(name__icontains=search_value)),email__icontains=e)
        # instead of icontains we can use iexact also to find the exact word 
        return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy,'sv':search_value})
    
def byname(req):
    if req.method=='POST':
        search_value=req.POST.get('search')
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        e = user.email
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        allqueryy=queryy.objects.filter(Q(name__iexact=search_value))
        return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy,'sv':search_value})
    
def byemail(req):
    if req.method=='POST':
        search_value=req.POST.get('search')
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        e = user.email
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        allqueryy=queryy.objects.filter(Q(email__iexact=search_value))
        return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy,'sv':search_value})

def byquery(req):
    if req.method=='POST':
        search_value=req.POST.get('search')
        pk=req.session['id']
        user=Student.objects.get(id=pk)
        e = user.email
        data={'name':user.firstname,'email':user.email,'contact':user.contact,'image':user.image,'document':user.document,'password':user.password}
        allqueryy=queryy.objects.filter(Q(query__iexact=search_value))
        return render(req, 'dashboard.html',{'data':data, 'allqueryy':allqueryy,'sv':search_value})




    

        
