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
    console.log(sticky)
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