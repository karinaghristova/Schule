# Generated by Django 4.1.3 on 2023-02-09 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_subjectclass_class_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectclass',
            name='students',
            field=models.ManyToManyField(blank=True, to='accounts.student'),
        ),
    ]