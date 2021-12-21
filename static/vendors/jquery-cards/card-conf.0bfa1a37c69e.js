// Card Configuration

var cardFlipped;

$(document).ready(function () {
    cardFlipped = false;
    $("input").keyup(function () {
        var value = $(this).val();
        var name = "#" + $(this).attr("name");
        $(name).text(value);
    }).keyup();

    $("#flip").focus(function () {
        flipCard();
    });
    $("#flip").focusout(function () {
        flipCard();
    });
});

function flipCard() {
    if (cardFlipped == false) {
        // Flip the card to back
        $("#payment-card-front").fadeOut(300);
        $("#payment-card-back").fadeIn(300);

        cardFlipped = true;
    } else {
        // Flip the card to front
        $("#payment-card-back").fadeOut(300);
        $("#payment-card-front").fadeIn(300);

        cardFlipped = false;
    }
}