from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib import auth

# Create your views here.

class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
            #get user data
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            context = {
                'fieldValues' : request.POST
            }

            if not User.objects.filter(username=username).exists() :
                if not User.objects.filter(email=email).exists() :
                    if len(password)<8:
                        messages.error(request, 'Password should be minimum 8 characters')
                        return render(request, '/auth/register.html', context)
                    else: 
                        user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
                        user.set_password(password)
                        user.is_active = True
                        user.save()
                    
                        """
                        send_mail(
                            'Activate account',
                            'Please activate your accouunt. Do not reply!',
                            'noreply@project.com',
                            [email],
                            fail_silently=False,
                        )
                        """
                        #messages.success(request, 'Registration Successfull')
                        return render(request, 'auth/login.html')
                    
                else:
                    messages.info(request, 'Email already exists')
                    return render(request, 'auth/register.html', context)
            else:
                messages.info(request, 'Username already exists')
                return render(request, 'auth/register.html', context)
        

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    
    def post(self, request):
        #get user data
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome,   '+user.first_name +' you are now logged in')
                    return render(request, 'leads.html')
                messages.error(request, 'Account not found')
                return render(request, 'auth/login.html')
            messages.error(request, 'Invalid credentials, try again!')
            return render(request, 'auth/login.html')
        messages.warning(request, 'Please fill all the fields')
        return render(request, 'auth/login.html')

                

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric character'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username already tacken'}, status=409)
        return JsonResponse({'username_valid':'Username OK'})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email exapmle: xxxx@abc.com'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email already tacken'}, status=409)
        return JsonResponse({'email_valid':'Email OK'})
        
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('/auth/login')


class SetnewpassView(View):
    def get(self, request):
        return render(request, 'auth/setnewpass.html')

class ResetpassView(View):
    def get(self, request):
        return render(request, 'auth/reset-pass.html')

    def post(self, request):
        #get user data
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues' : request.POST
        }

        if User.objects.filter(email=email).exists() :
            if len(password)<8:
                messages.error(request, 'Password should be minimum 8 characters')
                return render(request, 'auth/reset-pass.html', context)
            else: 
                user = User.objects.get(email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, 'Password Change Successfull')
                return redirect('/auth/login/')
        else:
            messages.info(request, 'Email does not exists')
            return render(request, 'auth/reset-pass.html', context)

class SetNewpassView(View):
    def get(self, request):
        return render(request, 'auth/setnewpass.html')

    def post(self, request):
        #get user data
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues' : request.POST
        }
        if User.objects.filter(email=email).exists() :
            if len(password)<8:
                messages.error(request, 'Password should be minimum 8 characters')
                return render(request, 'auth/reset-pass.html', context)
            else: 
                user = User.objects.get(email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, 'Password Change Successfull')
                return redirect('/auth/login/')
        else:
                messages.info(request, 'Email does not exists')
                return render(request, 'auth/reset-pass.html', context)
