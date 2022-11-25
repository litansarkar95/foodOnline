from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages


# Create your views here.
def registerUser(request):
    if request.method=='POST':
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

    if request.method == "POST":
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



def login(request):

    return render(request,'accounts/login.html')


def logout(request):
    return

def dashboard(request):
    return            