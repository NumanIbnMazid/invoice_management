// This is the only other script tag that needs to be included on the page.

new Card({
    form: document.querySelector('form'),
    container: '.card-wrapper'
});

$('#cc-number').validateCreditCard(function (result) {
    $('#cc-type').html((result.card_type == null ? '' : '( ' + result.card_type.name + ' )'));

});