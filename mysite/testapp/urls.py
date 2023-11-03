from django.urls import path
from . import views

app_name = 'testapp'
urlpatterns = [
    path('', views.toLogin_view),
    path('toregister/', views.toRegister_view),
    path('register/', views.Register_view),  # 后端逻辑

    path('toguestlogin/', views.toguestLogin_view),
    path('guestlogin/', views.guestLogin_view),

    path('tosellerlogin/', views.tosellerLogin_view),
    path('sellerlogin/', views.sellerLogin_view),

    path('tomanagerlogin/', views.tomanagerLogin_view),
    path('managerlogin/', views.managerLogin_view),

    path('toguestbusiness/', views.toguestbusiness_view),
    path('place_order/', views.place_order_step1, name='place_order'),

    path('tosellerbusiness/', views.tosellerbusiness_view),
    path('dishadd/', views.dishadd_view),

    path('todishedit/<str:dish_id>/', views.todishedit_view, name='todishedit'),
    path('dishedit/<str:dish_id>/', views.dishedit_view, name='dishedit'),

    path('dishdelete/<str:dish_id>/', views.dishdelete_view, name='dishdelete'),
    path('updateorderstatus/<int:order_id>/', views.updateorderstatus_view, name='updateorderstatus'),
    path('tomanagerbusiness/', views.tomanagerbusiness_view),

    path('tocanteenedit/<str:canteen_id>/', views.tocanteenedit_view, name='tocanteenedit'),
    path('canteenedit/<str:canteen_id>/', views.canteenedit_view, name='canteenedit'),
    path('canteendelete/<str:canteen_id>/', views.canteendelete_view, name='canteendelete'),
    path('canteenadd/', views.canteenadd_view),

]
