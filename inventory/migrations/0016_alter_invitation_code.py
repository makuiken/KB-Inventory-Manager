# Generated by Django 4.2.7 on 2023-11-14 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_alter_invitation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default='q3U3Iy', max_length=12, unique=True),
        ),
    ]
