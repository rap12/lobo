$(function () {
       $("#reservation_btn").click(function () {
           var value = document.getElementById('reservation_number').value;
        window.location.href = "/ticket_reservation" + value.trim() + "/";
    });

    $("#ticket_btn").click(function(){
        window.location.href = "/ticket_new/";
    });
    $(".book_btn").click(function () {
        var value = this.getAttribute("value");
        window.location.href = "/program/movie" + value.trim() + "/";
    });
    $("#buy_ticket").click(function () {
        var value = this.getAttribute("value");
        window.location.href = "/program/movie" + value.trim() + "/";
    });
});