from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category,MenuItem,Cart,Order,OrderItem
User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
 class Meta: model=User;fields=['id','username']
class CategorySerializer(serializers.ModelSerializer):
 class Meta: model=Category;fields=['id','title','slug']
class MenuItemSerializer(serializers.ModelSerializer):
 class Meta: model=MenuItem;fields=['id','title','price','featured','category']
class CartSerializer(serializers.ModelSerializer):
 class Meta: model=Cart;fields=['id','menuitem','quantity','unit_price','price','user'];read_only_fields=['id','unit_price','price','user']
 def validate_quantity(self,value):
  if value<1: raise serializers.ValidationError('Quantity must be at least 1.')
  return value
class OrderItemSerializer(serializers.ModelSerializer):
 class Meta: model=OrderItem;fields=['menuitem','quantity','unit_price','price']
class OrderSerializer(serializers.ModelSerializer):
 items=OrderItemSerializer(many=True,read_only=True)
 class Meta: model=Order;fields=['id','user','delivery_crew','status','total','date','items'];read_only_fields=['id','user','total','date','items']
