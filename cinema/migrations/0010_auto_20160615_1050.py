from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0009_auto_20160615_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditorium',
            name='seats1',
        ),
        migrations.AlterField(
            model_name='auditorium',
            name='rows',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='auditorium',
            name='seats',
            field=models.IntegerField(default=8),
        ),
    ]
