# Generated by Django 4.1.3 on 2023-02-09 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_absence_term_grade_term_praise_term_remark_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.subject'),
        ),
    ]
