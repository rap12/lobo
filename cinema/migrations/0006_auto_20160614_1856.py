from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_auto_20160614_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='reserv_number',
            new_name='reservation_number',
        ),
    ]
