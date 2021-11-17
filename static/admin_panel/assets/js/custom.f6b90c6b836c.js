// ************************************** Custom Scripts **************************************

// dynamic navbar active
$(function ($) {
    let url = window.location.href
    $('nav ul li a').each(function () {
        if (this.href === url) {
            $(this).parent().addClass('active')
            // $(this).parent().parent().parent().addClass('menu-open')
        }
    })

    // console.log(url)
})

// ************************************** /Custom Scripts **************************************

// ************************************** Select2 Arrow **************************************
$(".select2-selection__arrow").html("<i class='fas fa-caret-square-down font-23'></i>")
// ************************************** /Select2 Arrow **************************************