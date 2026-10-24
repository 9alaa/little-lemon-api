from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from restaurant.models import Category,MenuItem
class Command(BaseCommand):
 help='Create groups and example menu items'
 def handle(self,*args,**kwargs):
  for role in ['Manager','Delivery Crew']: Group.objects.get_or_create(name=role)
  items=[('Starters','starters','Greek Salad','8.50'),('Starters','starters','Bruschetta','6.00'),('Mains','mains','Lemon Chicken','15.00'),('Mains','mains','Pasta','12.50'),('Mains','mains','Grilled Fish','19.00'),('Desserts','desserts','Baklava','7.00'),('Drinks','drinks','Lemonade','4.00')]
  for cat,slug,title,price in items:
   category,_=Category.objects.get_or_create(slug=slug,defaults={'title':cat})
   MenuItem.objects.get_or_create(title=title,defaults={'category':category,'price':price})
  self.stdout.write(self.style.SUCCESS('Groups and sample menu ready'))
