from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import DepositProduct


# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=255, blank=True, null=True)
    financial_products = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    img = models.ImageField(blank=True, upload_to='%Y%m%d')
    deposit_products = models.ManyToManyField(DepositProduct, through='LikeProduct') # LikeProduct 필드를 위한 M:M.
    
class LikeProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_products')
    depositproduct = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='depositproducts')
    rating = models.FloatField(validators=[MinValueValidator(0,5),MaxValueValidator(5.0)])