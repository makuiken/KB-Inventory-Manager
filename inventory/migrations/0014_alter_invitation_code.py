# Generated by Django 4.2.7 on 2023-11-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_invitation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default='1UavIb', max_length=12, unique=True),
        ),
    ]
