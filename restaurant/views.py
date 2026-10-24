from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category,MenuItem,Cart,Order,OrderItem
from .serializers import CategorySerializer,MenuItemSerializer,CartSerializer,OrderSerializer,UserSerializer
User=get_user_model()
def manager(user): return user.is_staff or user.is_superuser or user.groups.filter(name='Manager').exists()
def crew(user): return user.groups.filter(name='Delivery Crew').exists()
def customer(user): return not manager(user) and not crew(user)
def deny(): return Response({'detail':'You do not have permission to perform this action.'},status=403)
class GroupUsers(APIView):
 permission_classes=[IsAuthenticated]
 def group(self,role): return get_object_or_404(Group,name=role)
 def get(self,request,role):
  if not manager(request.user): return deny()
  return Response(UserSerializer(self.group(role).user_set.all(),many=True).data)
 def post(self,request,role):
  if not manager(request.user): return deny()
  user=get_object_or_404(User,username=request.data.get('username',''))
  self.group(role).user_set.add(user)
  return Response({'message':f'{user.username} added to {role}'},status=201)
 def delete(self,request,role,user_id):
  if not manager(request.user): return deny()
  user=get_object_or_404(User,pk=user_id)
  self.group(role).user_set.remove(user)
  return Response(status=204)
class ManagerUsers(GroupUsers):
 def get(self,request): return super().get(request,'Manager')
 def post(self,request): return super().post(request,'Manager')
class ManagerUserDetail(GroupUsers):
 def delete(self,request,user_id): return super().delete(request,'Manager',user_id)
class CrewUsers(GroupUsers):
 def get(self,request): return super().get(request,'Delivery Crew')
 def post(self,request): return super().post(request,'Delivery Crew')
class CrewUserDetail(GroupUsers):
 def delete(self,request,user_id): return super().delete(request,'Delivery Crew',user_id)
class MenuList(generics.ListCreateAPIView):
 queryset=MenuItem.objects.all().order_by('id')
 serializer_class=MenuItemSerializer
 filterset_fields=['category','featured']
 search_fields=['title','category__title']
 ordering_fields=['price','title','id']
 def post(self,request,*args,**kwargs):
  if not manager(request.user): return deny()
  return super().post(request,*args,**kwargs)
class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
 queryset=MenuItem.objects.all()
 serializer_class=MenuItemSerializer
 def put(self,request,*args,**kwargs):
  if not manager(request.user): return deny()
  return super().put(request,*args,**kwargs)
 def patch(self,request,*args,**kwargs):
  if not manager(request.user): return deny()
  return super().patch(request,*args,**kwargs)
 def delete(self,request,*args,**kwargs):
  if not manager(request.user): return deny()
  return super().delete(request,*args,**kwargs)
class Categories(generics.ListAPIView):
 queryset=Category.objects.all().order_by('id')
 serializer_class=CategorySerializer
class CartItems(APIView):
 permission_classes=[IsAuthenticated]
 def get(self,request):
  if not customer(request.user): return deny()
  return Response(CartSerializer(Cart.objects.filter(user=request.user),many=True).data)
 def post(self,request):
  if not customer(request.user): return deny()
  s=CartSerializer(data=request.data)
  s.is_valid(raise_exception=True)
  item=s.validated_data['menuitem'];quantity=s.validated_data['quantity']
  cart,created=Cart.objects.update_or_create(user=request.user,menuitem=item,defaults={'quantity':quantity,'unit_price':item.price,'price':item.price*quantity})
  return Response(CartSerializer(cart).data,status=201 if created else 200)
 def delete(self,request):
  if not customer(request.user): return deny()
  Cart.objects.filter(user=request.user).delete()
  return Response(status=204)
class Orders(APIView):
 permission_classes=[IsAuthenticated]
 def get(self,request):
  if manager(request.user): qs=Order.objects.all()
  elif crew(request.user): qs=Order.objects.filter(delivery_crew=request.user)
  else: qs=Order.objects.filter(user=request.user)
  return Response(OrderSerializer(qs.order_by('-id'),many=True).data)
 @transaction.atomic
 def post(self,request):
  if not customer(request.user): return deny()
  cart=list(Cart.objects.select_related('menuitem').filter(user=request.user))
  if not cart: return Response({'detail':'Cart is empty.'},status=400)
  total=sum((entry.price for entry in cart),Decimal('0.00'))
  order=Order.objects.create(user=request.user,total=total)
  OrderItem.objects.bulk_create([OrderItem(order=order,menuitem=entry.menuitem,quantity=entry.quantity,unit_price=entry.unit_price,price=entry.price) for entry in cart])
  Cart.objects.filter(user=request.user).delete()
  return Response(OrderSerializer(order).data,status=201)
class OrderDetail(APIView):
 permission_classes=[IsAuthenticated]
 def get_order(self,request,pk):
  if manager(request.user): qs=Order.objects.all()
  elif crew(request.user): qs=Order.objects.filter(delivery_crew=request.user)
  else: qs=Order.objects.filter(user=request.user)
  return get_object_or_404(qs,pk=pk)
 def get(self,request,pk): return Response(OrderSerializer(self.get_order(request,pk)).data)
 def patch(self,request,pk):
  if not manager(request.user) and not crew(request.user): return deny()
  order=self.get_order(request,pk)
  allowed={'delivery_crew','status'} if manager(request.user) else {'status'}
  if not request.data or set(request.data)-allowed: return Response({'detail':'Only permitted fields may be updated.'},status=400)
  if 'delivery_crew' in request.data:
   user=get_object_or_404(User,pk=request.data['delivery_crew'])
   if not crew(user): return Response({'detail':'User must belong to Delivery Crew.'},status=400)
   order.delivery_crew=user
  if 'status' in request.data:
   value=request.data['status']
   if value not in (True,False,0,1,'0','1'): return Response({'detail':'Invalid status.'},status=400)
   order.status=value in (True,1,'1')
  order.save()
  return Response(OrderSerializer(order).data)
 def put(self,request,pk): return self.patch(request,pk)
 def delete(self,request,pk):
  if not manager(request.user): return deny()
  self.get_order(request,pk).delete()
  return Response(status=204)
