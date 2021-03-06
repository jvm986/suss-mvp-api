# Generated by Django 3.0.8 on 2020-11-26 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formresponse',
            old_name='responder',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='products',
        ),
        migrations.CreateModel(
            name='Responder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('form_responses', models.ManyToManyField(blank=True, to='api.FormResponse')),
                ('products', models.ManyToManyField(blank=True, to='api.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
