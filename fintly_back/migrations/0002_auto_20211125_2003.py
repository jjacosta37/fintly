# Generated by Django 3.2.7 on 2021-11-26 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fintly_back', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='accCategory',
            new_name='acc_category',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='bankProductId',
            new_name='bank_product_id',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='belvoid',
            new_name='belvo_id',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='transactionDate',
            new_name='transaction_date',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='metaAhorro',
            new_name='meta_ahorro',
        ),
    ]
