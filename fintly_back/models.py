from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponse
import csv
from django.contrib import admin






def export_as_csv(self, request, queryset):
    
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response

export_as_csv.short_description = "Export Selected"




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

    objects = TransactionManager()


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected" 

class TransactionAdmin(admin.ModelAdmin,ExportCsvMixin):
    actions = ["export_as_csv"]


