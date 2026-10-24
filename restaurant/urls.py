from django.urls import path
from . import views
urlpatterns=[
 path('groups/manager/users',views.ManagerUsers.as_view()),
 path('groups/manager/users/<int:user_id>',views.ManagerUserDetail.as_view()),
 path('groups/delivery-crew/users',views.CrewUsers.as_view()),
 path('groups/delivery-crew/users/<int:user_id>',views.CrewUserDetail.as_view()),
 path('categories',views.Categories.as_view()),
 path('menu-items',views.MenuList.as_view()),
 path('menu-items/<int:pk>',views.MenuDetail.as_view()),
 path('cart/menu-items',views.CartItems.as_view()),
 path('orders',views.Orders.as_view()),
 path('orders/<int:pk>',views.OrderDetail.as_view()),
]
