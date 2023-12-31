# Generated by Django 4.2.5 on 2023-09-27 01:38

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_changelog_user_changelog_length_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='change_code',
            field=models.CharField(default=inventory.models.generate_random_change_code, max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default='NML8NG', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sales_code',
            field=models.CharField(default=inventory.models.generate_random_sales_code, max_length=6, primary_key=True, serialize=False),
        ),
    ]
