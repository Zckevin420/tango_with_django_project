# Generated by Django 2.1.5 on 2024-03-13 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptest', '0009_auto_20240313_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderid',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
