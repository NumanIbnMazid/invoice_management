function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function to set Request Header with `CSRFTOKEN`
function setRequestHeader() {
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}


// Example Implementation

// $(".example").click(function () {

//     setRequestHeader();

//     $.ajax({
//         dataType: 'json',
//         type: 'POST',
//         url: "/example/",
//         data: {
//             "example-data": value
//         },
//         success: function (response) {
//             console.log("Success! ", response)
//         },
//         error: function (response) {
//             console.log("Error! ", response)
//         }
//     })
// });