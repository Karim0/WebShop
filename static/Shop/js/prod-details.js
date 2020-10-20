var temp_price = 0;

function select_char(id, price) {

    $('#chars' + id).css('border-bottom', '1px solid black');

    temp_price = price;

    $('#cost').html(temp_price);
    $('#pricebox').html(temp_price);
    $('#countAmount').val(1);
    $('#amountbox').html($('#countAmount').val());

}

function modify(op) {
    console.log(temp_price)

    if (op === 'plus') {
        $('#countAmount').val(parseInt($('#countAmount').val()) + 1);
    } else if (op === 'minus') {
        var value = parseInt($('#countAmount').val()) - 1

        if (value < 0) {
            value = 0
        }

        $('#countAmount').val(value);

    }
    $('#pricebox').html(temp_price * parseInt($('#countAmount').val()));
    $('#amountbox').html($('#countAmount').val());
}