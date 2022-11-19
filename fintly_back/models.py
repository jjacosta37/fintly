from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meta_ahorro = models.IntegerField(null=True, blank=True)


class UserLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_id = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)

# Transaction and transaction Manager

class TransactionManager(models.Manager):
    
    def find_all_for_user(self, user):
        return self.get_queryset().filter(userId=user)
    
class Transaction(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    belvo_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    type = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    bank_product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_number = models.CharField(max_length=100)
    acc_category = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    transaction_date = models.DateField()
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    isTransaction = models.BooleanField(default=False)

    objects = TransactionManager() # The default manager.

