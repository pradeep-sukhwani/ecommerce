# Generated by Django 5.1.4 on 2025-01-07 08:57

import ecommerce.models
import enumchoicefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the topping', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the dish', max_length=25)),
                ('size', enumchoicefield.fields.EnumChoiceField(default=ecommerce.models.SizeChoiceEnum['SMALL'], enum_class=ecommerce.models.SizeChoiceEnum, help_text='Size of the dish', max_length=6)),
                ('price', models.FloatField(help_text='Price of the dish')),
                ('toppings', models.ManyToManyField(to='ecommerce.topping')),
            ],
        ),
    ]
