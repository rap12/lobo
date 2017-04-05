from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_auto_20160614_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinemauser',
            name='user',
        ),
        migrations.DeleteModel(
            name='CinemaUser',
        ),
    ]
