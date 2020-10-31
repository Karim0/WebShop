$(".rotate").textrotator({
    animation: "dissolve", // You can pick the way it animates when rotating through words. Options are dissolve (default), fade, flip, flipUp, flipCube, flipCubeUp and spin.
    separator: ",", // If you don't want commas to be the separator, you can define a new separator (|, &, * etc.) by yourself using this field.
    speed: 2000 // How many milliseconds until the next word show.
});

$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        loop: true,
        margin: 10,
        items: 3,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 3
            }
        }
    });
});


window.onscroll = function () {
    myFunction()
};

// Get the navbar
var navbar = document.getElementById("main_header");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
    if (window.pageYOffset > sticky) {
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky");
    }
}


$(`#callback-form`).on('submit', function (e) {
    e.preventDefault();

    let data = {};
    data.name = $('#callname').val();
    data.phone = $('#callphone').val();
    const url = $(`#callback-form`).attr('action');
    $('#callname').val('');
    $('#callphone').val('');
    $.ajax({
        url: url,
        type: 'GET',
        data: data,
        caсhe: true,
        success: function (data) {
            var note = new jBox('Notice', {
                content: "Спасибо, мы обязятельно с вами свяжемся",
                color: 'green',
                delayClose: 2000,
            });
            note.open();
            note.close();
        },
        error: function () {
            var note = new jBox('Notice', {
                content: "Что то пошло не так, попробуйте позже`",
                color: 'red',
                delayClose: 2000,
            });
            note.open();
            note.close();
        }
    });

});


$(`#send_comment`).on('submit', function (e) {
    e.preventDefault();

    let data = {};
    data.prod_id = $('#prod_id').val();
    data.user_name = $('#user_name').val();
    data.phone_number = $('#phone_number').val();
    data.text = $('#comment_text').val();
    let rat = 0;
    let rad = document.getElementsByName('rating')
    for (let i = 0; i < rad.length; i++) {
        if (rad[i].checked) {
            rat = rad[i].value;
            rad[i].checked = false;
        }
    }
    $(".rating span").removeClass('checked');
    data.rating = rat

    data['csrfmiddlewaretoken'] = $('#send_comment [name="csrfmiddlewaretoken"]').val()

    const url = $(`#send_comment`).attr('action');
    $('#user_name').val('');
    $('#phone_number').val('');
    $('#comment_text').val('');


    $.ajax({
        url: url,
        type: 'POST',
        data: data,
        caсhe: true,
        success: function (data) {
            text = "";

            var com = JSON.parse(data);

            console.log(com)
            for (i in com){
                stars = "";
                for (let j = 0; j < com[i]['rate']; j++) {
                    stars += "<span class=\"star\"><i class=\"fas fa-star\"></i></span>";
                }
                text += `<li>
                            <div class="comment-box">
                                <span class="commentator"> ${ com[i]['name'] } </span>
                                ${stars}
                                <p>${com[i]['text']}</p>
                                <span class="date">${com[i]['date']}</span>
                            </div>
                        </li>`
            }

            $('#comments_view').html(text);

        },
        error: function () {
            var note = new jBox('Notice', {
                content: "Что то пошло не так, попробуйте позже`",
                color: 'red',
                delayClose: 2000,
            });
            note.open();
            note.close();
        }
    });

});