# Generated by Django 4.2.5 on 2023-09-20 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='length',
            unique_together={('ref_id', 'length')},
        ),
    ]
