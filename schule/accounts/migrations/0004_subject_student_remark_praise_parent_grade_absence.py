# Generated by Django 4.1.3 on 2023-02-08 23:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Praise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('child', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(decimal_places=2, max_digits=3)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('excused', models.BooleanField(default=False)),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.subject')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
    ]
