$(document).ready(function(){
    // Check Radio-box
    $(".rating input:radio").attr("checked", false);

    $('.rating input').click(function () {
        $(".rating span").removeClass('checked');
        $(this).parent().addClass('checked');
        console.log('asdasdas');
    });

    $('input:radio').change(
      function(){
        var userRating = this.value;
    });
});