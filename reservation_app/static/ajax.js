$(function () {
    function add_options(select, list){
        for (var i = 0; i < list.length; i++) {
            var opt = document.createElement('option');
            opt.text =  list[i][1];
            opt.value =  list[i][0];
            select.appendChild(opt);
        }
    }

    function remove_options(select){
        var i;
        for (i = select.options.length - 1; i >= 0; i--) {
                        select.remove(i);
                    }
    }

    $("#add_film").on("click", function (event) {
        event.preventDefault();
        var modal = document.getElementById('myModal');
        modal.style.display = "block";
        var token_val = $("#token input").first().val();
        var span = document.getElementsByClassName("close")[2];
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
        $("#btn_add_film").click(function () {
            var token_val = $("#token input").first().val();
            var title = document.getElementById("title").value;
            var director = document.getElementById('director').value;
            var release_year = document.getElementById('release_year').value;
            var url = document.getElementById('url').value;
            var description = document.getElementById('description').value;
            var length = document.getElementById('length').value;
            if (title == '' || length == '' || release_year == ''){
                alert("Uzupełnij wymagane pola: tytuł, rok produkcji i długość filmu");
                return;
            }
            var add_movie = $.post( "/administration_add_movie/", {'title': title, 'director': director, 'release_year': release_year, 'url': url, 'length': length, 'description': description, 'csrfmiddlewaretoken': token_val} );
            add_movie.done(function (response) {
                alert(response['message']);
                if (response['success'] == 1){
                    modal.style.display = "none";
                }
            });

        });
    });
    $("#add_auditorium").on("click", function (event) {
        event.preventDefault();
        var modal = document.getElementById('myModal1');
        modal.style.display = "block";
        var token_val = $("#token input").first().val();
        var span = document.getElementsByClassName("close")[2];
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
        $("#btn_add_auditorium").click(function () {
            var token_val = $("#token input").first().val();
            var number = document.getElementById("auditorium_number").value;
            var seats = document.getElementById('seat_number').value;
            var rows = document.getElementById('row_number').value;
            if (number == '' || seats == '', rows == ''){
                alert("Uzupełnij wszystkie pola");
            } else {
                var add_auditorium = $.post( "/administration_add_auditorium/", {'number': number, 'seats': seats, 'rows': rows, 'csrfmiddlewaretoken': token_val} );
                add_auditorium.done(function (response) {
                        alert(response['message']);
                        if (response['success'] == 1){
                            modal.style.display = "none";
                        }
                    });
            }
        });
    });
    $("#add_showtime").on("click", function (event) {
        event.preventDefault();
        var modal = document.getElementById('myModal2');
        modal.style.display = "block";
        var token_val = $("#token input").first().val();
        var span = document.getElementsByClassName("close")[2];
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
        var geting_data = $.get( "/administration_showtime_data/", {'csrfmiddlewaretoken': token_val}, function (response) {
            var movies = response['movies'];
            var auditoriums = response['auditoriums'];
            var drop_down_auditorium = document.getElementById("drop_down_auditorium");
            remove_options(drop_down_auditorium);
            add_options(drop_down_auditorium, auditoriums);
            var drop_down_movie = document.getElementById("drop_down_movie");
            remove_options(drop_down_movie);

            add_options(drop_down_movie, movies);
            var sel = document.getElementById("drop_down_time");
            if (sel != null){
                sel.remove();
            }
            var btn = document.getElementById('add_showtime_btn');
            if (btn != null){
                btn.remove();
            }
            $("#btn_show_time").click(function () {
                // modal.style.display = "none";
                var token_val = $("#token input").first().val();
                var movie = document.getElementById("drop_down_movie").value;
                var auditorium = document.getElementById("drop_down_auditorium").value;
                var day = document.getElementById("drop_down_day").value;
                var month = document.getElementById("drop_down_month").value;
                var year = document.getElementById("drop_down_year").value;
                if (movie == '' || auditorium == '' || day == '' || month == '' || year == ''){
                    alert("Uzupełnij dane");
                    return;
                }

                var geting_date = $.get( "/administration_time/", { 'movie': movie, 'auditorium' : auditorium, 'day' : day, 'month' : month, 'year' : year, 'csrfmiddlewaretoken': token_val}, function (response) {
                    var hours = response['time'];
                    if (hours.length == 0){
                        alert("Brak wolnych godzin w tej sali.")
                        return;
                    }
                    var ul = document.getElementById("add_showtime_modal");
                    var sel = document.getElementById("drop_down_time");
                    if (sel == null){
                        sel = document.createElement('select');
                        sel.id = "drop_down_time";
                    } else {
                        for (i = sel.options.length - 1; i >= 0; i--) {
                            sel.remove(i);
                        }
                    }
                    for (var i = 0; i < hours.length; i++) {
                        console.log("ok " + hours[i]['hour'] + ":" + hours[i]['minutes']);
                        var opt = document.createElement('option');
                        opt.text =  " " + hours[i]['hour'] + ":" + hours[i]['minutes'];
                        opt.value =  hours[i]['hour'] + ":" + hours[i]['minutes'];
                        sel.appendChild(opt);
                    }
                    ul.appendChild(sel);
                    var div_choices = document.getElementById("choices_showtime");
                    var btn = document.getElementById('add_showtime_btn');
                    if (btn == null){
                        btn = document.createElement("BUTTON");
                        btn.id = "add_showtime_btn";
                        btn.textContent = "dodaj seans";
                    }
                    div_choices.appendChild(btn)
                    $("#add_showtime_btn").click(function () {
                        var time = document.getElementById("drop_down_time").value;
                        var movie = document.getElementById("drop_down_movie").value;
                        var auditorium = document.getElementById("drop_down_auditorium").value;
                        var day = document.getElementById("drop_down_day").value;
                        var month = document.getElementById("drop_down_month").value;
                        var year = document.getElementById("drop_down_year").value;
                        if (movie == '' || auditorium == '' || day == '' || month == '' || year == ''){
                            alert("Uzupełnij dane");
                            return;
                        }
                        if (time == ''){
                            alert("Wybierz godzinę seansu");
                            return;
                        }
                        var add_showtime = $.post( "/administration_add_showtime/", { 'time': time, 'movie': movie, 'auditorium' : auditorium, 'day' : day, 'month' : month, 'year' : year, 'csrfmiddlewaretoken': token_val} );
                        add_showtime.done(function (response) {
                            alert(response['message']);
                            if (response['success'] == 1){
                                modal.style.display = "none";
                            }
                        });
                    });
                });
            });
        });
    });
});