# Generated by Django 4.2 on 2023-06-03 23:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user_profile.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('M', '남성'), ('F', '여성')], max_length=1)),
                ('preferred_gender', models.CharField(choices=[('M', '남성'), ('F', '여성'), ('A', '모두')], max_length=1)),
                ('mbti', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex='^[EI]{1}[NS]{1}[FT]{1}[JP]{1}$')])),
                ('passions', models.JSONField(blank=True, max_length=100, null=True, validators=[user_profile.validators.PassionsValidator(limit_value={'items': {'type': 'string'}, 'maxItems': 3, 'minItems': 0, 'type': 'array', 'uniqueItems': True})])),
                ('height', models.CharField(max_length=3)),
                ('religion', models.CharField(choices=[('없음', '없음'), ('기독교', '기독교'), ('불교', '불교'), ('천주교', '천주교')], max_length=3)),
                ('smoking_status', models.BooleanField()),
                ('drinking_status', models.CharField(choices=[('안함', '안함'), ('가끔', '가끔'), ('자주', '자주')], max_length=2)),
                ('location', models.CharField(choices=[('서울', '서울'), ('부산', '부산'), ('대구', '대구'), ('인천', '인천'), ('광주', '광주'), ('대전', '대전'), ('울산', '울산'), ('세종', '세종'), ('경기', '경기'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'), ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남'), ('제주', '제주')], max_length=2)),
                ('bio', models.CharField(max_length=500)),
                ('is_banned', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
