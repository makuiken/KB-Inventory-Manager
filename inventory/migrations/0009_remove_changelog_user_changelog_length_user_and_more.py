# Generated by Django 4.2.5 on 2023-09-26 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0008_sale_changetype_alter_invitation_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changelog',
            name='user',
        ),
        migrations.AddField(
            model_name='changelog',
            name='length_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='length_changelog', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='changelog',
            name='lumber_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lumber_changelog', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='changelog',
            name='sale_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_changelog', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='code',
            field=models.CharField(default='s5MSiJ', max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sales_code',
            field=models.CharField(default='h3Bs4G', max_length=6, primary_key=True, serialize=False),
        ),
    ]
