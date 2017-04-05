from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('rows', models.IntegerField()),
                ('seats', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CinemaUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('SU', 'Super User'), ('A', 'Worker'), ('C', 'Client')], default='C', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('director', models.CharField(max_length=40, null=True)),
                ('description', models.TextField(max_length=250, null=True)),
                ('release_year', models.IntegerField()),
                ('image_url', models.URLField(null=True)),
                ('length', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField()),
                ('seat_row', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Auditorium')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Reservation')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Worker'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='showtime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.Showtime'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
