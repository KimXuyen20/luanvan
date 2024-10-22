from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from accounts.models import Account
from doctor.forms import DoctorForm
from .forms import RegistrationForm, UserProfileForm, UserForm, UserProfile
from django.contrib import messages, auth
# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration successful.')
            return redirect('login')

    else:        
        form = RegistrationForm
    context = {
        'form':form,
    }
      
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logoutPage(request):
    auth.logout(request)
    messages.success(request,"We are logged out")
    return redirect('login')

def dashboard(request):
    return render(request,'accounts/dashboard.html')


def edit(request):
    userprofile = get_object_or_404(UserProfile, user= request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('edit')
    else:
        user_form = UserForm(instance=request.user)
        profile_form= UserProfileForm(instance=userprofile)
    context ={
        'user_form': user_form,
        'profile_form': profile_form,
    }        
    return render(request,'accounts/edit.html',context)


def registerDoctor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        d_form = DoctorForm(request.POST, request.FILES)
        
        # Kiểm tra cả hai form
        if form.is_valid() and d_form.is_valid():  # Sửa lại is_valid()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")  # Lấy phần đầu của email làm username
            
            # Tạo đối tượng User
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = Account.Doctor
            user.save()
            
            # Tạo đối tượng Doctor từ d_form
            doctor = d_form.save(commit=False)
            doctor.user = user
            user_profile = UserProfile.objects.get(user=user)
            doctor.user_profile = user_profile
            doctor.save()
            
            messages.success(request, 'Registration successful.')
            return redirect('login')
        else:
            # In lỗi từ cả hai form
            print('Invalid form:')
            print(form.errors)
            print(d_form.errors)  # In thêm lỗi từ d_form
    else:        
        form = UserForm()
        d_form = DoctorForm()

    context = {
        'form': form,
        'd_form': d_form,
    }
    
    return render(request, 'doctor/registerDoctor.html', context)

