from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .forms import RegistrationForm
from .models import Account
from portfolio.models import Portfolio
from django.contrib import messages
from django.template.loader import render_to_string

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login efetuado com sucesso!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email e/ou Senha incorretos!')
            return redirect('login')
    else:
        if request.user.id:
            return redirect('dashboard')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    messages.success(request, 'Logout efetuado com sucesso!')
    auth.logout(request)
    return redirect('login')

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            base_username = email.split('@')[0]
            username = base_username
            count = 1
            while Account.objects.filter(username=username).exists():
                username = f"{base_username}{count}"
            try: 
                user =  Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()

                # Create Portfolio:
                portfolio = Portfolio()
                portfolio.user_id = user.id
                portfolio.save()

                # User Activation:
                current_site = get_current_site(request)
                mail_subject = 'Portfolio Track - Ative sua conta!'
                message = render_to_string('accounts/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                messages.success(request, f'Obrigado pelo cadastro em nosso site! Enviamos o link de ativação para {email}')
            except Exception as e:
                messages.error(request, f'Erro: {str(e)}')
                print(f'Erro: {str(e)}')
            return redirect('register')
    else:
        if request.user.id:
            return redirect('dashboard')
    
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Sua conta foi ativada com sucesso!')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido!')
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Account.objects.get(email=email)
            
            # Recuperar conta:
            current_site = get_current_site(request)
            mail_subject = 'Recuperação de Conta!'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, f'Enviamos o link de recuperação de conta para {email}!')
            return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, f'Conta inexistente: "{email}"')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Por favor, defina uma nova senha!')
        return redirect('reset_password')
    else:
        messages.error(request, 'Link de ativação inválido!')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        if password == repeat_password:
            uid = request.session.get('uid')
            if uid is None:
                messages.error(request, 'Operação proibida!')
                return redirect('login')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Senha redefinida com sucesso!')
            return redirect('login')
        else:
            messages.error(request, 'As senhas não conferem!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

@login_required(login_url='login')
def profile(request):
    url = request.path
    context = {
        'url': url,
    }
    return render(request, 'accounts/profile.html', context)
