from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import *
from .models import *
from django.contrib import messages
from .models import Users
from django.contrib.auth.models import User

# def test_db(request):
#     objects = Users.objects.all()
#     return HttpResponse(objects)



# Create your templates here.

def login(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            print("user exists")

            # If credentials are correct, log the user in
            auth_login(request, user)
            if user.usertype == 1:
                return redirect(home)
            else:
                return HttpResponse('u r staff')
        else:
            print("user does not exist")
            # If credentials are not correct, return an error message
            messages.error(request, "wrong password or email")
            return redirect(login)

        # Render the login page with the form
    return render(request, 'loginPage.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('suemail')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            user = Users.objects.get(email=email)
            if user:
                msg = "User already exists"
                return render(request, 'registerPage.html', {'msg':msg})
        except:
            if password != password2:
                msg = "different passwords"
                return render(request, 'registerPage.html', {'msg':msg})
            else:
                Users.objects.create_user(
                    username=username, email=email, password=password)
                return redirect(registersuccess)
        # form = UserCreationForm(request.POST)
        # isexist = Users.objects.filter(email=request.POST.get('email'))
        # if isexist:
        #     messages.error(request, 'email already exists')
        #     return render(request, 'registerPage.html', {'error': messages.error})
        # elif (request.POST['password1'] != request.POST['password2']):
        #     messages.error(
        #         request, 'password confirmation doesn\'t match please try again')
        #     return render(request, 'registerPage.html', {'error': messages.error})
        #
        # if form.is_valid():
        #     print("valid")
        #     suusername = request.POST.get('username')
        #     supassword = request.POST.get('password1')
        #     suemail = request.POST.get('email')
        #
        #     Users.objects.create(
        #         username=suusername, email=suemail, password=supassword)
        #
        #     user = Users.objects.create_user(
        #         username=suusername, password=supassword, email=suemail)
        #     user.save()
        #     messages.success(request, 'Now you have an account, try to login!!!')
        #     return redirect('login')
        # else:
        #     print("invalid")
        #     return render(request, 'registerPage.html', {'form': form})

    else:
        form = UserRegisterForm()
        messages.error(
            request, 'Unknown Error....')
        return render(request, 'registerPage.html', {'form': form})

# def login(request):
#     return HttpResponse("Hello")
@login_required
def home(request):
    return render(request, 'homePage.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect(login)

def registersuccess(request):
    return render(request, 'registerSuccessPage.html')