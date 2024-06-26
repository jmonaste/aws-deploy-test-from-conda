# Generated by Django 4.2.2 on 2024-06-07 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(max_length=20)),
                ('comment', models.TextField(blank=True)),
                ('license_plate_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('datecompleted', models.DateTimeField(blank=True, null=True)),
                ('img_datetime', models.DateTimeField(blank=True, null=True)),
                ('img_lat', models.CharField(blank=True, max_length=25, null=True)),
                ('img_long', models.CharField(blank=True, max_length=25, null=True)),
                ('employee_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_user_for_task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
