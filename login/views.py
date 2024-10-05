from django.shortcuts import redirect, render,  HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages


            



# Create your views here.


    
def login_view(request):
    if request.method =='POST':
        username =request.POST.get("username")
        password =request.POST.get("pass")
        print(username, password)
        user = authenticate(request, username=username,password=password)
        print(user)
        if user is not None:
            
            login(request,user)
            print(request.user)
            if user.role =='Admin':
                return render (request,'startproject.html')
            elif user.role =='Client':
                return render(request,"startproject.html")
            elif user.role =='Qc':
                return render(request,"startproject.html")
            elif user.role =='Fitter':
                return render(request,"startproject.html")
        else:
            print("not auth")
            return render(request,'login.html',{"error":'Either username or password is incorrect'})
    return render (request,'login.html')
def logout_view(request):
    
    logout(request)
    # Redirect or perform actions after logout

    return redirect('login_view')
