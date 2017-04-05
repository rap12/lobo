from django.contrib import admin

from .models import Ticket
from .models import Movie
from .models import Auditorium
from .models import Showtime
from .models import Reservation

admin.site.register(Movie)
admin.site.register(Auditorium)
admin.site.register(Showtime)
admin.site.register(Reservation)
admin.site.register(Ticket)
