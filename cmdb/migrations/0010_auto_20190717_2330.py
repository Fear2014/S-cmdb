# Generated by Django 2.0.8 on 2019-07-17 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0009_auto_20190717_2329'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='idc',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='rack',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('name',)},
        ),
    ]
