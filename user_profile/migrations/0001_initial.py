# Generated by Django 4.2 on 2023-05-18 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('passion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(max_length=1)),
                ('preferred_gender', models.CharField(max_length=1)),
                ('mbti', models.CharField(max_length=4)),
                ('height', models.CharField(max_length=3)),
                ('religion', models.CharField(max_length=3)),
                ('smoking_status', models.BooleanField(default=False)),
                ('drinking_status', models.CharField(max_length=2)),
                ('location', models.CharField(max_length=2)),
                ('bio', models.CharField(max_length=500)),
                ('is_banned', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('passions', models.ManyToManyField(blank=True, to='passion.passion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
