$(function () {
       $(".see_showtimes").click(function () {
           var value = this.getAttribute("value");
        window.location.href = "/program/movie" + value.trim() + "/";
    });

    $(".seat").click(function(){
        if (this.src.match("seat_empty")){
            this.src = "/static/seat_chosen.png";
        }else if (this.src.match("seat_chosen")){
            this.src = "/static/seat_empty.png";
        } else {
            alert("To miejsce jest zajęte. Wybierz inne (nieoznaczone kolorem czerwonym)")
        }
    })

    $(".check_seats").click(function(){
        window.location.href = "/book" + this.getAttribute("value").trim() + "/";
    });

    $("#book").click(function(){
        var showtime_id = this.value;
        var numbers = [];
        var seats = document.getElementsByClassName("seat");
        for(var i = 0; i < seats.length; i++) {
            if (seats.item(i).src.match("seat_chosen")){
                var string = seats.item(i).getAttribute("value");
                var list = string.split(" ");
                var row = list[0];
                var number = list[1];
                numbers.push({'row': row, 'number': number});

            }
        }
        if (jQuery.isEmptyObject(numbers)){
            alert("Wyberz co najmniej 1 miejsce!");
            return;
        }
        var token_val = $("#token input").first().val();
        var book = $.post( "/book_tickets/", {'showtime_id': showtime_id, 'seat': JSON.stringify(numbers), 'csrfmiddlewaretoken': token_val });
        book.done(function (response) {
            if (response['message'] === undefined) {
                alert("Nie masz dostępu do rezerwacji. Zaloguj się jako użytkownik lub pracownik.");
                location.reload();
                return;
            }
            alert(response['message']);
            if (response['success'] == 1) {
                if (response['staff'] == 1) {
                    window.location.href = "/ticket_reservation" + response['reservation_number'] + "/";
                } else {
                    location.reload();
                }
            }

        });

    });
});