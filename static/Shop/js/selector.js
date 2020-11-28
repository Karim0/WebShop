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