from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)

        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login efetuado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email e/ou Senha incorretos!')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    messages.success(request, 'Logout efetuado com sucesso!')
    auth.logout(request)
    return redirect('login')