from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import pymysql
import datetime
from django.db.models import Max, F, IntegerField
from django.db.models.functions import Cast

max_dish_id = Dish.objects.aggregate(max_dish_id=Cast(Max('dish_id'), output_field=IntegerField()))['max_dish_id']


# Create your views here.

def toLogin_view(request):
    return render(request, 'login.html')


# 渲染注册界面
def toRegister_view(request):
    return render(request, 'register.html')


def Register_view(request):
    uid = request.POST.get('userID', '')
    un = request.POST.get('username', '')
    pwd = request.POST.get('password', '')
    tel = request.POST.get('tel', '')
    addr_id = request.POST.get('addr_id', '')
    if un and pwd and tel and addr_id:
        if uid[0] == 'b':
            gst = Guest(guest_id=uid, guest_name=un, guest_pwd=pwd, guest_tel=tel,
                        addr_id=addr_id)
            gst.save()
        elif uid[0] == 's':
            slr = Seller(seller_id=uid, canteen_id=1, seller_name=un, seller_pwd=pwd)
            slr.save()
        elif uid[0] == 'm':
            mgr = CanteenManager(manager_id=uid, manager_name=un, manager_pwd=pwd, manager_tel=tel)
            mgr.save()
        return redirect('/testapp/')
    else:
        return HttpResponse('请输入完整')


# 展现顾客登录的界面
def toguestLogin_view(request):
    return render(request, 'guestlogin.html')


# 顾客登录的后端逻辑
def guestLogin_view(request):
    gid = request.POST.get('guest_id', '')
    pwd = request.POST.get('password', '')

    if gid and pwd:
        # 用户id+密码有匹配项则登录成功
        c = Guest.objects.filter(guest_id=gid, guest_pwd=pwd).count()
        if c >= 1:
            messages.success(request, '登录成反对反对三十分功')
            request.session['gid'] = gid  # 将 gid 存储到会话中
            return redirect('/testapp/toguestbusiness/')  # 重定向
        else:
            return redirect('/testapp/toguestlogin/')
    else:
        return HttpResponse('请输入正确的账号和密码')


# 展现商家登录的界面
def tosellerLogin_view(request):
    return render(request, 'sellerlogin.html')


# 商家登录的后端逻辑
def sellerLogin_view(request):
    sid = request.POST.get('seller_id', '')
    pwd = request.POST.get('password', '')

    if sid and pwd:
        # 用户id+密码有匹配项则登录成功
        c = Seller.objects.filter(seller_id=sid, seller_pwd=pwd).count()
        if c >= 1:
            request.session['sid'] = sid  # 将 sid 存储到会话中备用
            return redirect('/testapp/tosellerbusiness/')
        else:
            return HttpResponse('账号或密码错误')
    else:
        return HttpResponse('请输入正确的账号和密码')


# 展现食堂管理员登录的界面
def tomanagerLogin_view(request):
    return render(request, 'managerlogin.html')


# 食堂管理员登录的后端逻辑
def managerLogin_view(request):
    mid = request.POST.get('manager_id', '')
    pwd = request.POST.get('password', '')

    if mid and pwd:
        # 用户id+密码有匹配项则登录成功
        c = CanteenManager.objects.filter(manager_id=mid, manager_pwd=pwd).count()
        if c >= 1:
            request.session['mid'] = mid  # 将 mid 存储到会话中备用
            return redirect('/testapp/tomanagerbusiness/')
        else:
            return HttpResponse('账号或密码错误')
    else:
        return HttpResponse('请输入正确的账号和密码')


def toguestbusiness_view(request):
    # 从数据库中获取视图的数据
    menu_items = WhatToEat.objects.all()

    context = {
        'menu_items': menu_items
    }

    return render(request, 'guestmenu.html', context)


# 顾客下订单的辅助函数
def get_dish_id_by_name(dish_name):
    # 实现根据菜品名称查询dish表获取dish_id的逻辑
    # 这里假设有一个名为"dish"的表，包含"id"和"name"字段
    # 在实际情况下，你需要根据你的数据库结构和查询语句来实现该函数
    # 下面是一个简单的示例：
    query = f"SELECT dish_id FROM dish WHERE dish_name = '{dish_name}'"
    result = execute_query(query)
    if result:
        return result[0][0]
    return None


def get_dish_price(dish_id):
    # 实现根据菜品ID查询dish表获取菜品单价的逻辑
    # 这里假设有一个名为"dish"的表，包含"id"和"price"字段
    # 在实际情况下，你需要根据你的数据库结构和查询语句来实现该函数
    # 下面是一个简单的示例：
    query = f"SELECT dish_price FROM dish WHERE dish_id = '{dish_id}'"
    result = execute_query(query)
    if result:
        return result[0][0]
    return None


def update_orders_table(dish_id, guest_id, quantity, order_time, order_amount):
    # 实现更新数据库中orders表的逻辑
    # 这里假设有一个名为"orders"的表，包含"id"、"dish_id"、"guest_id"、"order_dish_num"、"order_time"、"order_amount"和"order_status"字段
    # 在实际情况下，你需要根据你的数据库结构和插入语句来实现该函数
    # 下面是一个简单的示例：
    query = "INSERT INTO orders (dish_id, guest_id, order_dish_num, order_time, order_amount, order_status) " \
            "VALUES ('{}', '{}', {}, '{}', {}, '已下单') "
    query = query.format(dish_id, guest_id, quantity, order_time, order_amount)
    execute_query(query)
    # 获取插入的订单ID
    query = "SELECT LAST_INSERT_ID() AS order_id"
    result = execute_query(query)
    if result:
        return result[0][0]
    return None

def insert_new_addr(guest_id, area, building, room):
    # 获取已有记录中最大的 dish_id
    max_addr_id = Addr.objects.aggregate(max_addr_id=Max(Cast(F('addr_id'), output_field=IntegerField()))).get(
        'max_addr_id')
    # 计算新记录的 addr_id
    new_addr_id = str(int(max_addr_id) + 1) if max_addr_id else '1'  # 如果没有记录，从 1 开始

    # 创建新的addr记录
    new_addr = Addr(addr_id=new_addr_id, area=area, building=building, room=room)
    # 执行数据库更新操作
    new_addr.save()

    # 同步更新这名顾客的地址信息
    guest=get_object_or_404(Guest,guest_id=guest_id)
    guest.addr_id=new_addr_id
    guest.save()


def update_guest_tel(guest_id, tel):
    guest=get_object_or_404(Guest, guest_id=guest_id)
    guest.guest_tel=tel
    guest.save()

def execute_query(query):
    # 执行数据库查询的逻辑
    # 这里假设你使用的是某个数据库连接库，例如MySQLdb或psycopg2等
    # 在实际情况下，你需要根据你的数据库选择相应的库并编写执行查询的代码
    # 下面是一个简单的示例：
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='roOt_Pw0574',
                           database='order_system',
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def place_order_step2(dish_name, quantity, guest_id):
    # 根据菜品名称查询dish表获取dish_id
    dish_id = get_dish_id_by_name(dish_name)

    # 计算订单金额
    dish_price = get_dish_price(dish_id)
    order_amount = dish_price * quantity

    # 获取当前时间
    order_time = datetime.datetime.now()
    order_time = order_time.strftime("%Y-%m-%d %H:%M")
    # 更新数据库中的orders表
    order_id = update_orders_table(dish_id, guest_id, quantity, order_time, order_amount)

    # 返回订单ID
    return order_id


def place_order_step1(request):
    if request.method == 'POST':
        # 从表单中获取菜品名称、数量和顾客账号
        dish_name = request.POST.get('dish')
        quantity = int(request.POST.get('quantity'))
        guest_id = request.session.get('gid', '')  # 获取用户登录时键入的账号

        # 从表单中获取用户的地址信息:area, building, room
        area = request.POST.get('area')
        building = request.POST.get('building')
        room = request.POST.get('room')

        # 获取顾客的电话
        tel=request.POST.get('tel')

        # 调用place_order函数进行订单处理
        order_id = place_order_step2(dish_name, quantity, guest_id)
        # 地址操作
        insert_new_addr(guest_id, area, building, room)
        # 电话操作
        update_guest_tel(guest_id, tel)
        # 返回订单结果
        return render(request, 'place_order.html')
    else:
        # 处理GET请求，渲染下单页面
        return render(request, 'place_order.html')


# 商家登录后看到的前端逻辑，返回一个交互页面
def tosellerbusiness_view(request):
    sid = request.session.get('sid')
    dishes = Dish.objects.filter(seller_id=sid)
    order_details = OrderDetails.objects.filter(seller_id=sid)
    context = {
        'dishes': dishes,
        'order_details': order_details
    }
    return render(request, 'sellermenu.html', context)


def todishedit_view(request, dish_id):
    dish = get_object_or_404(Dish, dish_id=dish_id)

    return render(request, 'editdish.html', {'dish': dish})


def dishedit_view(request, dish_id):
    if request.method == 'POST':
        # 从请求中获取修改后的菜品名称、价格和描述
        dish = get_object_or_404(Dish, dish_id=dish_id)

        new_name = request.POST.get('dish_name')
        new_price = request.POST.get('dish_price')
        new_description = request.POST.get('dish_description')

        # 执行数据库更新操作
        dish.dish_name = new_name
        dish.dish_price = new_price
        dish.dish_description = new_description
        dish.save()

        # 可以根据需要执行其他操作

        return render(request, 'editdishOK.html')

    return HttpResponse('错误：无效的请求')


def dishdelete_view(request, dish_id):
    dish = get_object_or_404(Dish, dish_id=dish_id)

    dish.delete()
    return render(request, 'dishdeleteOK.html')


def dishadd_view(request):
    if request.method == 'POST':
        # 从会话中得到此时操作的商家账号sid
        sid = request.session.get('sid')
        # 从请求中获取新增的菜品名称、价格和描述
        new_name = request.POST.get('dish_name')
        new_price = request.POST.get('dish_price')
        new_description = request.POST.get('dish_description')

        # 获取已有记录中最大的 dish_id
        max_dish_id = Dish.objects.aggregate(max_dish_id=Max(Cast(F('dish_id'), output_field=IntegerField()))).get(
            'max_dish_id')
        # 计算新记录的 dish_id
        new_dish_id = str(int(max_dish_id) + 1) if max_dish_id else '1'  # 如果没有记录，从 1 开始

        # 创建新的dish记录
        new_dish = Dish(dish_id=new_dish_id, seller_id=sid, dish_name=new_name, dish_price=new_price,
                        dish_description=new_description)
        # 执行数据库更新操作
        new_dish.save()
        return render(request, 'dishaddOK.html')
    return HttpResponse('新增菜品失败')


def updateorderstatus_view(request, order_id):
    order = Orders.objects.get(order_id=order_id)  # 获取订单对象

    if request.method == 'POST':
        new_status = request.POST.get('new_status')  # 获取用户输入的新状态
        order.order_status = new_status  # 更新订单状态
        order.save()  # 保存订单对象

        return render(request, 'statusOK.html')

    return render(request, 'update_order_status.html', {'order': order})


def tomanagerbusiness_view(request):
    mid = request.session.get('mid')
    manager = CanteenManager.objects.filter(manager_id=mid)
    context = {'managers': manager}
    return render(request, 'managerview.html', context)


def tocanteenedit_view(request, canteen_id):
    canteen = get_object_or_404(Canteen, canteen_id=canteen_id)
    context = {'canteen': canteen}
    return render(request, 'canteenedit.html', context)


def canteenedit_view(request, canteen_id):
    canteen = get_object_or_404(Canteen, canteen_id=canteen_id)

    if request.method == 'POST':
        canteen.canteen_name = request.POST.get('canteen_name')
        # 其他表单字段的处理...
        canteen.save()
        return render(request, 'canteeneditOK.html')


def canteendelete_view(request, canteen_id):
    # 找到即将被删除的食堂的管理员、这个食堂里的所有商家和这个食堂
    manager = get_object_or_404(CanteenManager, canteen_id=canteen_id)
    sellers = Seller.objects.filter(canteen=canteen_id)
    canteen = get_object_or_404(Canteen, canteen_id=canteen_id)
    # 将此manager的canteen_id属性置空的逻辑
    manager.canteen_id = None
    manager.can_canteen_id = None
    manager.save()

    for seller in sellers:
        seller.canteen = None
        seller.save()
    # 删除这个食堂
    canteen.delete()
    return render(request, 'canteendeleteOK.html')


def canteenadd_view(request):
    if request.method == 'POST':
        new_name = request.POST.get('canteen_name')
        # 获取已有记录中最大的 canteen_id
        max_canteen_id = Canteen.objects.aggregate(
            max_canteen_id=Max(Cast(F('canteen_id'), output_field=IntegerField()))).get(
            'max_canteen_id')
        # 计算新记录的 canteen_id
        new_canteen_id = str(int(max_canteen_id) + 1) if max_canteen_id else '1'  # 如果没有记录，从 1 开始

        # 创建新的dish记录
        new_canteen = Canteen(canteen_id=new_canteen_id, canteen_name=new_name)
        # 执行数据库更新操作
        new_canteen.save()

        # 让当前管理员去管理这个新食堂
        mid = request.session.get('mid')
        manager = get_object_or_404(CanteenManager, manager_id=mid)
        manager.canteen_id = new_canteen_id
        manager.can_canteen_id = new_canteen_id
        manager.save()

        return render(request, 'canteenaddOK.html')
    return HttpResponse('新增食堂失败')
