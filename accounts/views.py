from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from . utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test

from django.core.exceptions import PermissionDenied

#Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied  

#Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied  


# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')
    elif request.method=='POST':
        print(request.POST)
        form =UserForm(request.POST)
        if form.is_valid():
            #password =form.cleaned_data['password']
            #user=form.save(commit=False)
            #user.set_password(password)
            #user.role=User.CUSTOMER
            #user.save()


            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.CUSTOMER
            user.save()

            # send verification email
            send_verification_email(request,user)

            messages.success(request,'Your Account has been registered successfuly!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)    

    else:
        form =UserForm()
    context ={
        'form':form
    }

    return render(request,'accounts/registerUser.html',context)


def registerVender(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('dashboard')

    elif request.method == "POST":
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)

        if form.is_valid()  and v_form.is_valid():
            #user 
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user =user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()

             # send verification email
            send_verification_email(request,user)
            
            messages.success(request,'Your Account has been registered successfuly!, please wait for the approval !')
            return redirect('registerVender')


        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    
    context ={
        'form':form,
        'v_form':v_form,
        
    }

    return render(request,'accounts/registerVender.html',context)    


def activate(request,uidb64,token):
    return

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are already logged in')
        return redirect('myAccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,"you are logged in.")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')
    

    return render(request,'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request,'you are logged out')
    return redirect('login')

     
@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)      

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cusDashboard(request):
    return render(request,'accounts/cusDashboard.html') 

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')       