from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import *
from .models import *
from django.contrib import messages
from .models import *

# def test_db(request):
#     objects = Users.objects.all()
#     return HttpResponse(objects)



# Create your templates here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        #print(email, password)

        user = authenticate(request, email=email, password=password)
        #print(user)
        if user:
            #print("user exists")

            auth_login(request, user)
            if user.usertype == 1:
                return redirect(home)
            else:
                return redirect(manager)
        else:
            #print("user does not exist")
            messages.error(request, "wrong password or email")
            return redirect(login)

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
                return redirect(registerSuccess)
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
    # 假设你的用户模型是Users，并且你已经实现了用户认证
    user = request.user
    print(user.username, user.wallet)
    try:
        context = {
            'username': user.username,
            'wallet': user.wallet,
        }
    except Users.DoesNotExist:
        context = {
            'userid': None,
            'wallet': None,
        }
    return render(request, 'homePage.html', context)

@login_required
def manager(request):
    users = Users.objects.all()
    items = Items.objects.all()
    user = request.user
    print(user.username, user.wallet)
    try:
        context = {
            'username': user.username,
            'wallet': user.wallet,
            'items': items,
            'users': users,
        }
    except Users.DoesNotExist:
        context = {
            'userid': None,
            'wallet': None,
        }
    return render(request, 'managerPage.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect(login)

def registerSuccess(request):
    return render(request, 'registerSuccessPage.html')

@login_required
def deleteUser(request, userid):
    user = Users.objects.get(userid=userid)
    #print(user)
    user.delete()
    return redirect(manager)

@login_required
def updateUser(request, userid):
    if request.method == 'POST':
        user = get_object_or_404(Users, userid=userid)
        username = request.POST.get('username')
        email = request.POST.get('email')
        username_exists = Users.objects.exclude(userid=userid).filter(username=username).exists()
        email_exists = Users.objects.exclude(userid=userid).filter(email=email).exists()

        if username_exists or email_exists:
            # 如果username或email已经存在，返回错误消息
            error_message = "Username or email already exists."
            return JsonResponse({'status': 'error', 'message': error_message})
        else:
            # 如果username和email都是唯一的，更新用户信息
            user.username = username
            user.email = email
            user.save()
            # 可以重定向到一个确认页面或者用户列表页面
            return redirect('manager')  # 确保'manager'是你的URL名称

    else:
        # 如果请求方法不是POST，返回错误
        return JsonResponse({'status': 'error', 'message': 'wrong method'})
        # user.save()
        # 重定向到某个页面，例如用户列表页面
        # return redirect(manager)
    # return JsonResponse({'status': 'error', 'message': 'wrong method'})

@login_required
def deleteItem(request, itemid):
    item = Items.objects.get(itemid=itemid)
    #print(item)
    item.delete()
    return redirect(manager)

@login_required
def updateItem(request, itemid):
    if request.method == 'POST':
        item = get_object_or_404(Items, itemid=itemid)
        itemname = request.POST.get('itemname')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        itemname_exists = Items.objects.exclude(itemid=itemid).filter(itemname=itemname).exists()

        if itemname_exists:
            # 如果username或email已经存在，返回错误消息
            error_message = "Username already exists."
            return JsonResponse({'status': 'error', 'message': error_message})
        else:
            # 如果username和email都是唯一的，更新用户信息
            item.itemname = itemname
            item.price = price
            item.quantity = quantity
            item.save()
            # 可以重定向到一个确认页面或者用户列表页面
            return redirect('manager')  # 确保'manager'是你的URL名称

    else:
        # 如果请求方法不是POST，返回错误
        return JsonResponse({'status': 'error', 'message': 'wrong method'})

@login_required
def additem(request):
    if request.method == 'POST':
        itemname = request.POST.get('itemname')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        # 创建并保存新项目
        item = Items(itemname=itemname, price=price, quantity=quantity)
        item.save()
        return JsonResponse({"message": "Item added successfully"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def updateProfileAndWallet(request):
    if request.method == 'POST':
        user = request.user
        # 使用get方法从POST中获取username和email，如果不存在则使用当前值
        username = request.POST.get('username', user.username)
        email = request.POST.get('email', user.email)

        # 更新用户名和邮箱
        user.username = username
        user.email = email

        # 检查是否需要更新密码
        new_password = request.POST.get('new_password')
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # 更新session以防用户被登出

        user.save()
        return JsonResponse({"message": "Profile updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def verifyPassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        # print(old_password)
        email = request.user.email
        user = authenticate(email=email, password=old_password)
        # print(user)
        if user is not None:
            # print("1")
            return JsonResponse({'is_password_correct': True})
        else:
            # print("2")
            return JsonResponse({'is_password_correct': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def topUp(request):
    if request.method == 'POST':
        user = request.user
        add = request.POST.get('money')
        if add:
            user.wallet = user.wallet + Decimal(add)
            user.save()
            return JsonResponse({'message': 'Top-up successful'})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Items, pk=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, "Item added to cart!")
    return redirect('item_list')  # Redirect to the page where the items are listed


