from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=150)
    cat_image=models.ImageField(upload_to="category_iamge")
    description=models.TextField()
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    pro_image=models.ImageField(upload_to="product_iamge")
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.IntegerField(null=False,blank=False)
    selling_price=models.IntegerField(null=False,blank=False)
    description=models.TextField()
    status=models.BooleanField(default=False)
    trending=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
        
        
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)        
    product=models.ForeignKey(Product,on_delete=models.CASCADE)        
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)  
    
    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
    
    
         