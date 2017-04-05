from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0008_auto_20160615_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditorium',
            name='seats1',
            field=models.IntegerField(default=7),
        ),
    ]
