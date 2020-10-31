/*custom_selector Menu*/
$('.custom_selector').click(function () {
    $(this).attr('tabindex', 1).focus();
    $(this).toggleClass('active');
    $(this).find('.custom_selector-menu').slideToggle(300);
});
$('.custom_selector').focusout(function () {
    $(this).removeClass('active');
    $(this).find('.custom_selector-menu').slideUp(300);
});
$('.custom_selector .custom_selector-menu li').click(function () {
    $(this).parents('.custom_selector').find('span').text($(this).text());
    $(this).parents('.custom_selector').find('input').attr('value', $(this).attr('id'));
});


$('.custom_selector-menu li').click(function () {
    var input = '<strong>' + $(this).parents('.custom_selector').find('input').val() + '</strong>',
        msg = '<span class="msg">Hidden input value: ';
    $('.msg').html(msg + input + '</span>');
});

function sortby(log) {
    $('#sortingby').on('submit', function (e) {
        e.preventDefault();

        let data = {};

        data.by = $(`#sortby_val`).val();
        console.log(log);

        const url = $(`#sortingby`).attr('action');

        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            caсhe: true,
            success: function (data) {
                const products = JSON.parse(data);

                text = '';

                for (let i in products) {
                    text += `
                            <div class="product-box col-lg-4 col-md-4 col-sm-6 col-12">
                                <div class="card">
                                    <div class="tag-box">
                                        <span>${products[i]['tag']}</span>
                                    </div>
                                    <div class="prod-wrap">
                                        <div class="img-box">
                                            <img class="w-100" src="${products[i]['photo']}"
                                                 alt="${products[i]['photo_alt']}">
                                        </div>
                                        <div class="content-box">
                                            <h3>${products[i]['name']}</h3>
                                            <p>${products[i]['desc']}</p>
                                            <a href="/shop/product/${products[i]['id']}">Подробнее</a>
                                        </div>
                                    </div>
                                </div>
                            </div>`
                }

                $('#product_view').html(text);

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

    })

    $('#sortingby').submit();

}