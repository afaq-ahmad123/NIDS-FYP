from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from django.core.mail import send_mail
from django.apps import apps
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User

from django.core.mail import EmailMessage


userInfo = apps.get_model('login' , 'user')
# Create your views here.
# def login_view(request):
#     print("in login user")
#     login_form = LoginForm(request.POST or None)
#     if login_form.is_valid() and request.method == 'post':
#         # if not request.POST.get('email') or not request.POST.get('password'):
#         #     print("not Valid")
#         #     messages.add_message(request, messages.ERROR, 'Email or Password Invalid!')
#         #     return render(request, 'login/login.html', {'loginForm': login_form})
#         print("valid")
#         if login_form.authenticate_data(request.POST.get('email'), request.POST.get('password')):
#             user = User.objects.get(email=request.POST.get('email'))
#             if user.is_active:
#                 print("user activated")
#                 email = request.POST.get("email")
#                 request.session["email"] = email
#                 messages.add_message(request, messages.SUCCESS, 'Login Successfully!')
#                 return redirect("dash-url")
#             else:
#                 messages.error(request, 'You account is not activated by admin.')
#                 return render(request, 'login/login.html', {'loginForm': login_form})
#         else:
#             print("not Valid")
#             messages.error(request,'Email or Password Invalid!')
#             return redirect("dash-url", {'loginForm': login_form})
#             #return render(request, 'login/login.html', {'loginForm': login_form})
#
#     return render(request, 'login/login.html', {'loginForm': login_form})


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    print("check form")
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=username)
        if not user:
            raise forms.ValidationError('This user does not exist')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Check user credentials')
        print("user authenticated")
        if user.is_active:
            print("user activated")
            login(request, user)
        if next:
            print("in next")
            return redirect(next)
        # context = {
        #     'user': username,
        # }
        return redirect("dash-url")

    context = {
        'loginForm': form,
    }
    return render(request, "login/login.html", context)

# def activate(request,email):
#     print(email)
#     print(request.GET.get('email',''))
#     if not email:
#         messages.add_message(request,messages.ERROR,'Link not valid')
#         return render(request,'login/register.html')
#     user = userInfo.objects.filter(email=email)
#     if not user:
#         messages.add_message(request, messages.ERROR, 'Account does not exists.')
#         return render(request, 'login/register.html')
#     if user.app == False:
#         user.app = True
#         messages.add_message(request,messages.SUCCESS, 'Account activated successfully!!')
#     else:
#         messages.add_message(request,messages.ERROR,'Account already activated')
#     return render(request,'login/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

# def register(request):
#     form= UserForm(request.POST or None)
#     print(request.method)
#     if form.is_valid() and request.method == 'POST':
#         print("Valid Form")
#         if form.authenticate_data(request.POST.get('email')):
#             print("Form authenticated!")
#             final = form.save(commit=False)
#             # final.save()
#             subject = 'Request Submitted'
#             message= 'Thank you for registration. Your request is being processed. You can login after confirmation from Admin.'\
#                      +str(form.__getitem__('name').value())+str(form.__getitem__('email').value())+str(form.__getitem__('password').value())
#             from_email= settings.EMAIL_HOST_USER
#             to_email = ['afaqahmadmalik970@gmail.com']
#             send_mail(subject, message, from_email,to_email,fail_silently=False)
#             messages.add_message(request, messages.SUCCESS, 'Email sent to admin successfully.')
#             #messages.success(request,'Email sent successfully.')
#             print('Email sent successfully.')
#             return redirect("activate-url")
#             #return render(request,'login/register.html')
#         elif form.clean_password():
#             print('Password not same.')
#             messages.error(request,'Password not same.')
#         else:
#             print('User already exist.')
#             messages.error(request,'User already exist.')
#
#     return render(request,'login/register.html',{'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        #print(User.objects.all().delete())
        if form.is_valid():
            print(User.objects.all())
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('login/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'login/register.html', {'form': form})

def forgot(request):

    return render(request,'login/forgot-password.html')

def log(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    print("log out")
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    count = User.objects.filter(id__in=user_id_list).count()
    print(count)
    print("In Logout"+ str(User.objects.filter(id__in=user_id_list)))
    #print(len(Session.objects.all()))
    if count < 2:
       return HttpResponse('<h1>Please Login with another account first.</h1>')
    logout(request)
    return redirect('login-url')
#Session.objects.filter(expire_date__gte=timezone.now())