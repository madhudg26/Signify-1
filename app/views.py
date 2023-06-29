from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from app.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def Home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'Home.html',d)

    return render(request,'Home.html')



def Registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid() and PD.is_valid():
            pw=UD.cleaned_data['password']
            USO=UD.save(commit=False)
            USO.set_password(pw)
            USO.save()

            PFO=PD.save(commit=False)
            PFO.user=USO
            PFO.save()

            send_mail('User Registration',
            'Registration successfull',
            'madhudg26@gmail.com',
            [USO.email],
            fail_silently=False)
            return HttpResponse('Registration is successfull')


    return render(request,'Registration.html',d)



def Sign_In(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'Sign_In.html')



@login_required
def Sign_Out(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))



















    


