# Generated by Django 5.1.1 on 2024-10-07 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=10)),
                ('user_id', models.CharField(max_length=10)),
                ('product_name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='image')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='image',
            field=models.ImageField(default='image', upload_to='image'),
        ),
    ]
