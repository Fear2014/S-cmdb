# Generated by Django 2.0.8 on 2019-07-17 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_auto_20190715_1912'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='idc',
            unique_together={('name',)},
        ),
    ]
