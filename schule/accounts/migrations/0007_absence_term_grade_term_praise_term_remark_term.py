# Generated by Django 4.1.3 on 2023-02-09 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.term'),
        ),
        migrations.AddField(
            model_name='grade',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.term'),
        ),
        migrations.AddField(
            model_name='praise',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.term'),
        ),
        migrations.AddField(
            model_name='remark',
            name='term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.term'),
        ),
    ]
