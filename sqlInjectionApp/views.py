from django.shortcuts import render
from django .http import HttpResponse
from django.http import HttpResponseRedirect
from . models import userLogin
from . forms import loginForm

# Create your views here.
def login(request):
    form = loginForm()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = userLogin.objects.raw('SELECT * FROM sqlInjectionApp_userLogin WHERE username = username and password = password')
        if user:
            return HttpResponse("successfully logged in")
    return render(request,'sqlInjectionApp/login.html',{'form':form})
