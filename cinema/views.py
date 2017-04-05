import json

from django.contrib import auth
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from datetime import date, datetime, timedelta, timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import Ticket
from .models import Movie
from .models import Auditorium
from .models import Showtime
from .models import Reservation
from .models import ReservationNumber

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test

from django.views.decorators.http import require_POST
from cinema.consts import AdminMessages, WorkingHours

from cinema.forms import UserForm


def contact_view(request):
    return render(request, 'contact.html', {'account_type': check_account_type(request.user)})


def in_client_group(user):
    return user.groups.filter(name='client').exists()


def in_staff_group(user):
    return user.groups.filter(name='staff').exists()


def in_administration_group(user):
    return user.groups.filter(name='administration').exists()


def in_client_staff_group(user):
    return user.groups.filter(name='staff').exists() or user.groups.filter(name='client').exists()


def check_account_type(user):
    account_type = 0
    if in_staff_group(user):
        account_type = 1
    if in_administration_group(user):
        account_type = 2
    return account_type


def home_view(request):
    return render(request, 'nav_page.html', {'account_type': check_account_type(request.user)})


def films_view(request):
    movies = [[movie.title, movie.image_url, movie.description, movie.length, movie.director, movie.pk] for movie in
              Movie.objects.all()]
    return render(request, 'films.html', {'movies': movies, 'account_type': check_account_type(request.user)})


def program_view(request):
    showtimes = []
    for showtime in Showtime.objects.filter(date__gte=datetime.now()):
        date = "" + str(showtime.date.day) + '-' + str(showtime.date.month) + '-' + str(showtime.date.year)
        seats_left = showtime.auditorium.rows * showtime.auditorium.seats - Reservation.objects.filter(
            showtime=showtime).count()
        showtimes.append(
            [showtime.date.hour, showtime.date.minute, date, showtime.auditorium.number, showtime.movie.title,
             showtime.id, seats_left, showtime.movie.title])
    return render(request, 'program.html', {'data': showtimes, 'account_type': check_account_type(request.user)})


@user_passes_test(in_administration_group, login_url='/')
def admin_view(request):
    months = [month for month in Ticket.MONTHS]
    days = [i for i in range(1, 32)]
    years = [date.today().year + i for i in range(0, 3)]
    shows_today = []
    for movie in Showtime.objects.all():
        if movie.date.date() == datetime.today().date():
            shows_today.append(
                movie.movie.title + " - sala " + str(movie.auditorium.number) + ": godzina " + str(movie.date.time()))
    notifications = []
    return render(request, 'admin_nav.html', {'shows_today': shows_today,
                                              'days': days, 'months': months, 'years': years,
                                              'notifications': notifications})


@user_passes_test(in_administration_group, login_url='/')
def admin_time_view(request):
    booked_hours = []
    times = []
    auditorium = int(request.GET['auditorium'])
    movie = request.GET['movie']
    year = int(request.GET['year'])
    day = int(request.GET['day'])
    month = int(request.GET['month'])
    movie_length = Movie.objects.filter(pk=movie).all()[0].length
    noon = datetime(year, month, day, 0, 0, 0)
    for showtime in Showtime.objects.filter(auditorium=auditorium):
        if showtime.date.date() == noon.date():
            booked_hours.append((showtime.date.astimezone(timezone.utc).replace(tzinfo=None), showtime.movie.length))
    time = noon + timedelta(hours=WorkingHours.BEGINNING)
    end = noon + timedelta(hours=WorkingHours.END)
    i = 0
    end_of_prev_film = time
    if len(booked_hours) > i:
        start_of_next_movie = booked_hours[i][0]
        next_movie_len = booked_hours[i][1]
    else:
        start_of_next_movie = end
    time_end = noon + timedelta(hours=WorkingHours.BEGINNING,
                                minutes=movie_length)
    while time_end < end:
        if time > end_of_prev_film and time_end < start_of_next_movie:
            times.append({'hour': time.hour, 'minutes': time.minute})
        if time_end > start_of_next_movie:
            end_of_prev_film = start_of_next_movie + timedelta(minutes=next_movie_len)
            if len(booked_hours) > i + 1:
                i += 1
                start_of_next_movie = booked_hours[i][0]
                next_movie_len = booked_hours[i][1]
            else:
                start_of_next_movie = end
        time = time + timedelta(minutes=10)
        time_end = time_end + timedelta(minutes=10)

    return HttpResponse(json.dumps({'time': times}), content_type="application/json")


@require_POST
@user_passes_test(in_administration_group, login_url='/')
def admin_add_showtime_view(request):
    auditorium = int(request.POST['auditorium'])
    auditorium = Auditorium.objects.get(pk=auditorium)
    movie = request.POST['movie']
    movie = Movie.objects.get(pk=movie)
    year = int(request.POST['year'])
    day = int(request.POST['day'])
    month = int(request.POST['month'])
    time = request.POST['time']
    hour, minute = time.split(':')
    mydate = datetime(year, month, day, int(hour), int(minute))
    showtime = Showtime(auditorium=auditorium, movie=movie, date=mydate)
    showtime.save()
    return HttpResponse(json.dumps({'message': AdminMessages.SHOWTIME_ADDED, 'success': 1}),
                        content_type="application/json")


@require_POST
@user_passes_test(in_administration_group, login_url='/')
def admin_add_movie_view(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({'message': AdminMessages.NOT_LOGGED, 'success': 0}),
                            content_type="application/json")
    title = request.POST['title']
    director = request.POST['director']
    release_year = request.POST['release_year']
    url = request.POST['url']
    description = request.POST['description']
    length = request.POST['length']

    if not release_year.isdigit() and length.isdigit():
        return HttpResponse(json.dumps({'message': AdminMessages.DIGITS_NEEDED_ERROR, 'success': 0}),
                            content_type="application/json")

    movie = Movie(title=title, length=int(length), release_year=int(release_year), director=director, image_url=url,
                  description=description)
    try:
        movie.save()
        message = AdminMessages.FILM_ADDED + movie.title
        success = 1
    except ValidationError as e:
        message = e.messages
        success = 0
    return HttpResponse(json.dumps({'message': message, 'success': success}), content_type="application/json")


@require_POST
@user_passes_test(in_administration_group, login_url='/')
def admin_add_auditorium_view(request):
    number = int(request.POST['number'])
    seats = int(request.POST['seats'])
    rows = int(request.POST['rows'])
    if Auditorium.objects.filter(number=number).count() > 0:
        return HttpResponse(json.dumps({'message': AdminMessages.AUDITORIUM_EXISTS, 'success': 0}),
                            content_type="application/json")

    auditorium = Auditorium.objects.create(number=number, seats=seats, rows=rows)

    message = AdminMessages.AUDITORIUM_ADDED + str(auditorium.number)
    return HttpResponse(json.dumps({'message': message, 'success': 1}), content_type="application/json")


@user_passes_test(in_administration_group, login_url='/')
def admin_showtime_data_view(request):
    movies = [[movie.id, movie.title] for movie in Movie.objects.all()]
    auditoriums = [[auditorium.number, auditorium.number] for auditorium in Auditorium.objects.all()]
    return HttpResponse(json.dumps({'movies': movies, 'auditoriums': auditoriums}), content_type="application/json")


def movie_showtime(request, num):
    try:
        movie = Movie.objects.get(pk=int(num))
    except ObjectDoesNotExist as e:
        return HttpResponseForbidden(AdminMessages.NO_MOVIE)
    movie_showtimes = []
    for showtime in Showtime.objects.filter(movie=num).filter(date__gte=datetime.now()):
        date = "" + str(showtime.date.day) + '-' + str(showtime.date.month) + '-' + str(showtime.date.year)
        seats_left = showtime.auditorium.rows * showtime.auditorium.seats - Reservation.objects.filter(
            showtime=showtime).count()
        movie_showtimes.append(
            [showtime.date.hour, showtime.date.minute, date, showtime.auditorium.number, showtime.movie.title,
             showtime.id, seats_left, showtime.movie.title])

    return render(request, 'program.html', {'data': movie_showtimes, 'account_type': check_account_type(request.user)})


def book_seats(request, num):
    try:
        showtime = Showtime.objects.get(pk=int(num))
    except ObjectDoesNotExist as e:
        return HttpResponseForbidden(AdminMessages.NO_SHOWTIME + num)
    row_number = showtime.auditorium.rows
    seat_number = showtime.auditorium.seats
    seats = {}
    for row in range(1, row_number + 1):
        for_row = []
        for seat in range(1, seat_number + 1):
            if Reservation.objects.filter(showtime=showtime).filter(seat_row=row).filter(
                    seat_number=seat).count() > 0:
                for_row.append({seat: 'taken'})
            else:
                for_row.append({seat: 'empty'})
        seats[row] = for_row
    date = "" + str(showtime.date.day) + '-' + str(showtime.date.month) + '-' + str(showtime.date.year)
    title = Movie.objects.filter(id=showtime.movie.id)[0].title
    time = "" + str(showtime.date.hour) + ":" + str(showtime.date.minute)

    return render(request, 'booking.html',
                  {'title': title, 'seats': seats, 'date': date, "time": time, "showtime_id": showtime.id,
                   'account_type': check_account_type(request.user)})


@require_POST
@user_passes_test(in_client_staff_group, login_url='/')
def book_tickets(request):
    try:
        showtime = Showtime.objects.get(pk=int(request.POST['showtime_id']))
    except ObjectDoesNotExist as e:
        message = AdminMessages.NO_SHOWTIME
        success = 0
        return HttpResponse(json.dumps({'message': message, 'success': success}), content_type="application/json")
    seats = request.POST.get('seat')
    seats = json.loads(request.POST['seat'])

    reservation_number = ReservationNumber.objects.create()
    for seat in seats:
        Reservation.objects.create(showtime=showtime, seat_number=int(seat['number']),
                                   seat_row=int(seat['row']), user=request.user,
                                   reservation_number=reservation_number)

    message = AdminMessages.SEATS_BOOKED + str(reservation_number.id)
    staff = 0
    if in_staff_group(request.user):
        staff = 1
    return HttpResponse(json.dumps(
        {'message': message, 'success': 1, 'staff': staff, 'reservation_number': str(reservation_number.id)}),
        content_type="application/json")


def log_out(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def login_form(request):
    return render(request, 'login.html')


@require_POST
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        login(request, user)
    return HttpResponseRedirect('/')


def register_form(request):
    return render(request, 'register.html', {'account_type': check_account_type(request.user)})


def register_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            g = Group.objects.get(name='client')
            g.user_set.add(new_user)
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            login(request, user)
    return HttpResponseRedirect('/')


@user_passes_test(in_staff_group, login_url='/')
def get_reservation_ticket(request, num):
    reservation_list = Reservation.objects.filter(reservation_number=int(num))
    if len(reservation_list) == 0:
        return render(request, 'inform_template.html', {'message': AdminMessages.NO_RESERVATION})
    message = ""
    for reservation in reservation_list:
        if Ticket.objects.filter(reservation=reservation).count() > 0:
            message += AdminMessages.TICKET_NO + num + AdminMessages.TICKET_ALREADY_PRINTED
            break
        ticket = Ticket(reservation=reservation, user=request.user, date=datetime.now())
        ticket.save()
        # print ticket
    message += AdminMessages.PRINTING_ENDED
    return render(request, 'inform_template.html', {'message': message})


@user_passes_test(in_staff_group, login_url='/')
def get_ticket(request):
    movies = [(movie.title, movie.director, movie.release_year, movie.id) for movie in Movie.objects.all()]
    return render(request, 'film_reservation.html', {'movies': movies})


@user_passes_test(in_staff_group, login_url='/')
def reservation_view(request):
    return render(request, 'staff_nav.html')


@user_passes_test(in_staff_group, login_url='/')
def client_reservation(request):
    return render(request, 'client_reservation.html')
