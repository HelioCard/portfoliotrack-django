# Generated by Django 4.2.6 on 2023-10-31 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_transactions_portfolioitems'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolioitems',
            old_name='type',
            new_name='sort_of',
        ),
        migrations.RenameField(
            model_name='transactions',
            old_name='type',
            new_name='sort_of',
        ),
    ]
