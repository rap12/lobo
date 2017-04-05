from django.db import models

from django.core.exceptions import ValidationError
from datetime import datetime

from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=20, null=False)
    director = models.CharField(max_length=40, null=True)
    description = models.TextField(max_length=250, null=True)
    release_year = models.IntegerField(null=False)
    image_url = models.URLField(null=True)
    length = models.PositiveIntegerField(null=False)  # time in minutes

    def clean(self):
        if self.title == "":
            raise ValidationError("Title cannot be empty")

    def save(self, *args, **kwargs):
        self.clean()
        super(Movie, self).save(*args, **kwargs)


class Auditorium(models.Model):
    number = models.IntegerField(primary_key=True)
    rows = models.IntegerField(null=False, default=5)  # number of rows in auditorium
    seats = models.IntegerField(null=False, default=8)  # number of seats in a row


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium)
    date = models.DateTimeField(default=datetime.now)


class ReservationNumber(models.Model):
    pass


class Reservation(models.Model):
    showtime = models.ForeignKey(Showtime)
    user = models.ForeignKey(User, unique=False, null=False)
    seat_number = models.IntegerField(null=False)  # min_value=1, max_value=showtime.auditorium.seats)
    seat_row = models.IntegerField(null=False)  # min_value=1, max_value=showtime.auditorium.rows)
    reservation_number = models.ForeignKey(ReservationNumber, default=1)

    def save(self, *args, **kwargs):
        if 1 <= self.seat_number <= self.showtime.auditorium.seats and 1 <= self.seat_row <= self.showtime.auditorium.rows:
            super(Reservation, self).save(*args, **kwargs)


class Ticket(models.Model):
    reservation = models.ForeignKey(Reservation)
    user = models.ForeignKey(User, unique=False, null=False)
    date = models.DateTimeField()

    MONTHS = (
        (1, 'styczeń'),
        (2, 'luty'),
        (3, 'marzec'),
        (4, 'kwiecień'),
        (5, 'maj'),
        (6, 'czerwiec'),
        (7, 'lipiec'),
        (8, 'sierpień'),
        (9, 'wrzesień'),
        (10, 'pażdziernik'),
        (11, 'listopad'),
        (12, 'grudzień')
    )
