# Generated by Django 4.2.5 on 2023-09-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_rename_ref_id_length_lumber_alter_invitation_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lumber',
            name='lumber_type',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default='sxpsff', max_length=12, unique=True),
        ),
    ]
