from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_auto_20160614_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='reserv_number',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cinema.ReservationNumber'),
        ),
    ]
