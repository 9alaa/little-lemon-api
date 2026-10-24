from django.db import models
from django.conf import settings
class Category(models.Model):
 title=models.CharField(max_length=255,unique=True)
 slug=models.SlugField(unique=True)
 def __str__(self): return self.title
class MenuItem(models.Model):
 title=models.CharField(max_length=255)
 price=models.DecimalField(max_digits=8,decimal_places=2)
 featured=models.BooleanField(default=False)
 category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='items')
 def __str__(self): return self.title
class Cart(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
 menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
 quantity=models.PositiveIntegerField()
 unit_price=models.DecimalField(max_digits=8,decimal_places=2)
 price=models.DecimalField(max_digits=10,decimal_places=2)
 class Meta: constraints=[models.UniqueConstraint(fields=['user','menuitem'],name='unique_user_menuitem')]
class Order(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='customer_orders')
 delivery_crew=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='delivery_orders')
 status=models.BooleanField(default=False)
 total=models.DecimalField(max_digits=10,decimal_places=2)
 date=models.DateField(auto_now_add=True)
class OrderItem(models.Model):
 order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
 menuitem=models.ForeignKey(MenuItem,on_delete=models.PROTECT)
 quantity=models.PositiveIntegerField()
 unit_price=models.DecimalField(max_digits=8,decimal_places=2)
 price=models.DecimalField(max_digits=10,decimal_places=2)
