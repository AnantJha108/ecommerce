from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from store.forms import CustomUserForm
from django.contrib import messages

def register(request):
    form = CustomUserForm
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registered Successfully ! Login to Continue ")
            return redirect('login')
    context = {'form':form}
    return render(request,"store/accounts/signup.html",context)

def loginPage(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already loged in ")
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd= request.POST.get('password')

            user = authenticate(request,username=name,password=passwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Log in successfull !")
                return redirect('/')
            else:
                messages.error(request,"Invalid username and Password")
                return redirect("login")
        return render(request,"store/accounts/login.html")

def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout successfull !")
    return redirect('/')