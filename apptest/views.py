from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from .models import *
import json

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
        if user is not None and user:
            #print("user exists")

            auth_login(request, user)
            if user.usertype == 1:
                return redirect(home)
            else:
                return redirect(manager)
        else:
            #print("user does not exist")
            # messages.error(request, "wrong password or email")
            # return redirect(login)
            messages.error(request, "Wrong password or email")
            return render(request, 'loginPage.html', {})

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
                messages.error(request, "User already exists")
                return redirect(register)  # 假设'register'是注册页面的URL名称
                # msg = "User already exists"
                # return render(request, 'registerPage.html', {'msg':msg})
        except:
            if password != password2:
                messages.error(request, "Different passwords")
                return redirect(register)
                # msg = "different passwords"
                # return render(request, 'registerPage.html', {'msg':msg})
            else:
                Users.objects.create_user(
                    username=username, email=email, password=password)
                return redirect(registerSuccess)
    else:
        form = UserRegisterForm()
        return render(request, 'registerPage.html', {'form': form})

# def login(request):
#     return HttpResponse("Hello")
@login_required
def home(request):
    # 假设你的用户模型是Users，并且你已经实现了用户认证
    user = request.user
    items = Items.objects.all()  # 或者您的查询
    # print(items)  # 打印查询结果，看是否如预期
    # print(user.username, user.wallet)
    try:
        context = {
            'username': user.username,
            'wallet': user.wallet,
            'items': items,
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
    # print(user.username, user.wallet)
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
def addToCart(request, itemid):
    # print('1')
    # print(request.body)
    # print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        numofitem = data.get('quantity', 1)
        item = get_object_or_404(Items, pk=itemid)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += int(numofitem)
        else:
            cart_item.quantity = int(numofitem)

        cart_item.save()
        return JsonResponse({'message': 'Item added to cart successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    # item = get_object_or_404(Items, pk=itemId)
    # cart, created = Cart.objects.get_or_create(user=request.user)
    # cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    # if not created:
    #     cart_item.quantity += int(quantity)
    # cart_item.save()
    # return JsonResponse({'message': 'Add to cart successful'})
#    return redirect('homePage.html')  # Redirect to the page where the items are listed


# @login_required
# def search(request):
#     #print(111111)
#     if request.method == 'GET':
#         keyword = request.GET.get('keyword')
#     # 获取商品信息，这里假设您已经有了商品的数据
#     items = Items.objects.all()
#     #print(keyword)
#     # items = [
#     #     {'itemname': 'Item 1', 'price': 10, 'quantity': 5},
#     #     {'itemname': 'Item 2', 'price': 20, 'quantity': 3},
#     #     # 其他商品信息
#     # ]
#     if keyword:
#         items = Items.objects.filter(itemname__icontains=keyword)
#         #print(items)
#         return render(request, 'homePage.html', {'items': items})
#
#     return render(request, 'homePage.html', {'items': items})

@login_required
def searchItem(request):
    if request.method == 'POST':
        search_keyword = request.POST.get('searchKeyword')
        # print(search_keyword)
        # 根据关键词搜索 Items 模型
        if search_keyword:  # Ensure search_keyword is not None
            items = Items.objects.filter(itemname__icontains=search_keyword)
            items_data = list(items.values('itemid', 'itemname', 'price', 'quantity'))
            # print(items_data)
            return JsonResponse({'items': items_data})
        else:
            return JsonResponse({'error': 'No search keyword provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cartItems(request):
    if request.method == 'POST':
        # print('1')
        items = CartItem.objects.filter(cart__user=request.user).select_related('item')
        items_data = []
        total_price = 0
        for item in items:
            item_data = {
                'itemname': item.item.itemname,
                'itemid': item.item.itemid,
                'quantity': item.quantity,
                'price': float(item.item.price),
                'total_item_price': float(item.get_total_price()),
            }
            # print(item_data)
            items_data.append(item_data)
            total_price += item.get_total_price()
        return JsonResponse({'items': items_data, 'total_price': float(total_price)})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def removeFromCart(request, itemid):
    # 确保只处理POST请求
    if request.method == 'POST':
        user = request.user
        try:
            # 根据当前用户和商品ID找到CartItem实例
            cart_item = CartItem.objects.get(cart__user=user, item__itemid=itemid)
            cart_item.delete()  # 删除该CartItem实例
            return JsonResponse({'success': 'Item removed successfully'})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# @login_required
# def payDirect(request, payment):
#     if request.method == 'POST':
#
#     else:
#         return JsonResponse({'error': 'Invalid request'}, status=400)
#


# @login_required
# def payCart(request):
#     if request.method == 'POST':
#         user = request.user
#         cart_items = CartItem.objects.filter(cart__user=user).select_related('item')
#         total_price = sum(item.quantity * item.item.price for item in cart_items)
#
#         # 检查库存
#         out_of_stock_items = [
#             item for item in cart_items if item.quantity > item.item.quantity
#         ]
#         if out_of_stock_items:
#             return JsonResponse({'error': 'Out of stock'}, status=400)
#
#         # 检查钱包余额
#         if user.wallet < total_price:
#             return JsonResponse({'error': 'Insufficient funds'}, status=400)
#
#         # 扣款并更新库存
#         user.wallet -= total_price
#         user.save()
#         for item in cart_items:
#             product = Items.objects.get(itemid=item.item.itemid)
#             product.quantity -= item.quantity
#             product.save()
#             item.delete()  # Optionally remove the item from the cart after purchase
#
#         return JsonResponse({'success': 'Payment completed successfully'})
#     else:
#         return JsonResponse({'error': 'invalid request'}, status=400)


@login_required
def checkWallet(request):
    if request.method == 'GET':
        user = request.user
        item_price = request.GET.get('price', None)

        if item_price is None:
            return JsonResponse({'error': 'invalid request'}, status=400)
        try:
            item_price = float(item_price)
        except ValueError:
            return JsonResponse({'error': 'invalid'}, status=400)

        if user.wallet < item_price:
            return JsonResponse({'can_afford': False})
        else:
            return JsonResponse({'can_afford': True})
    else:
        return JsonResponse({'error': 'invalid request'}, status=400)


@login_required
def addressPage(request):
    items_data = []
    total_price = 0
    for key in request.GET.keys():
        if key.startswith('items[') and 'itemid' in key:
            index = key.split('[')[1].split(']')[0]
            itemid = request.GET[key]
            quantity = request.GET.get(f'items[{index}][quantity]', 0)
            price = request.GET.get(f'items[{index}][price]', '0')
            total_price += Decimal(price) * int(quantity)  # 累加每个物品的价格乘以数量
            items_data.append({'itemid': itemid, 'quantity': quantity, 'price': price})
    items_data_json = json.dumps(items_data)
    # print(items_data)
    context = {
        'items': items_data,
        'items_data_json': items_data_json,  # JSON字符串，用于隐藏字段
        'total_price': total_price,
        'username': request.user.username,
        'wallet': request.user.wallet,
    }
    return render(request, 'address.html', context)


@login_required
def payTheBill(request):
    if request.method == 'POST':
        user = request.user
        try:
            items_data = json.loads(request.POST.get('items_data', '[]'))
            # print(items_data)
            total_price = Decimal('0.00')
            for item_data in items_data:
                itemid = item_data['itemid']
                quantity = int(item_data['quantity'])
                price = Decimal(item_data['price'])

                item = get_object_or_404(Items, pk=itemid)
                if item.quantity >= quantity:
                    item.quantity -= quantity  # 减去库存
                    item.save()
                    total_price += price * quantity
                else:
                    return JsonResponse({'error': f'Not enough stock for item {itemid}'}, status=400)
            # print(total_price)
            if user.wallet >= total_price:
                user.wallet -= total_price  # 更新用户钱包
                user.save()
                return JsonResponse({'success': 'Payment successful'})
            else:
                return JsonResponse({'error': 'Not enough money'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# @login_required
# def payDirect(request):
#     if request.method == 'POST':
#         user = request.user
#     else:
#         return JsonResponse({'error': 'invalid request'}, status=400)
