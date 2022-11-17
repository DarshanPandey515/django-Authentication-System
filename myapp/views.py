from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.http import HttpResponseRedirect
from myapp.forms import ProfileForm
from myapp.models import Profile
# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request,'index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request,'Login Successfully.')
                return redirect('/')
            else:
                messages.success(request,'Invalid Credential.')
                return redirect('login')
        return render(request,'login.html')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            user_obj = User.objects.filter(username=username,email=email)

            if user_obj.exists():
                messages.error(request,"User already exists. If it's you than go to login page.")
                return HttpResponseRedirect(request.path)

            if password1 != password2:
                messages.error(request,"Both password should match.")
                return HttpResponseRedirect(request.path)

            if len(password1) < 8:
                messages.error(request,"Password must be atleast 8 characters.")
                return HttpResponseRedirect(request.path)

            User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
            return redirect('/')
        return render(request,'register.html')

@login_required(login_url='login')
def logout_user(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('login')
    else:
        return redirect('login')



@login_required(login_url='login')
def profile(request):
    obj = get_object_or_404(Profile,user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=obj)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            return redirect('/')
    else:
        obj = get_object_or_404(Profile,user=request.user)
        form = ProfileForm(instance=obj)
    context = {
        'form':form,
    }
    return render(request,'profile.html',context)