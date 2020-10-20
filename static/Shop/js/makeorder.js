function addAmount(id) {
    $(`#item${id}Amount`).val(parseInt($(`#item${id}Amount`).val()) + 1);

    $(`#item${id}Count`).html($(`#item${id}Amount`).val());

    $(`#totalCheck`).html(parseInt($(`#item${id}Amount`).val()) * parseFloat($(`#item${id}Price`).html()));


    let data = {};
    data.product_id = id;
    data.amount = parseInt($(`#item${id}Amount`).val());
    const url = $(`#modifyForm`).attr('action');

    console.log($(`#modifyForm`));
    // console.log($(`#delete_item`));

    $.ajax({
        url: url,
        type: 'GET',
        data: data,
        caсhe: true,
        success: function (data) {},
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

}

function minusAmount(id) {
    var value = parseInt($(`#item${id}Amount`).val()) - 1;

    if (value <= 0) {
        console.log('DEl');
    }

    $(`#item${id}Amount`).val(value);

    $(`#item${id}Count`).html($(`#item${id}Amount`).val());

    $(`#totalCheck`).html(parseInt($(`#item${id}Amount`).val()) * parseFloat($(`#item${id}Price`).html()));

}
$(`#modifyForm`).on('submit', function (e) {
    e.preventDefault();
});

$(`#delete_item`).on('submit', function (e) {
    e.preventDefault();
});


function delItem(id) {
    let data = {};
    data.product_id = id;
    const url = $(`#delete_item`).attr('action');

    $.ajax({
        url: url,
        type: 'GET',
        data: data,
        caсhe: true,
        success: function (data) {
            const cart = JSON.parse(data);
            let cartAmount = 0;

            if (cart.length < 1) {
                $('#cartSize').html('0');
                $('#delete_item').html(`
                пока нет товаров (
                `);
            } else {
                let text = "";
                for (let i in cart) {
                    cartAmount += 1;
                    let props = "";
                    for (let j in cart[i]['props']) {
                        props += ` 
                        <p class="mb-3 text-muted text-uppercase small"> ${cart[i]['props'][j]['prop']}:
                                                                        ${cart[i]['props'][j]['value']}</p>
                        `;
                    }

                    text += `
                            <div class="cart-item">
                                <div class="row mb-4">
                                    <div class="col-md-5 col-lg-3 col-xl-3">
                                        <div class="view zoom overlay z-depth-1 rounded mb-3 mb-md-0">
                                            <img class="img-fluid w-100"
                                                 src="${cart[i]['img']}"
                                                 alt="${cart[i]['alt']}">
                                        </div>
                                    </div>
                                    <div class="col-md-7 col-lg-9 col-xl-9">
                                        <div class="cart-item-info">
                                            <div class="d-flex justify-content-between flex-wrap">
                                                <div class="col-lg-6 col-md-6 col-12">
                                                    <h3>${cart[i]['name']}</h3>
                                                    ${props}
                                                </div>
                                                <div class="col-lg-6 col-md-6 col-12 counter-box text-center">
                                                    <div class="def-number-input number-input safari_only mb-0 w-100">
                                                        <a onclick="minusAmount(${cart[i]['id']})"
                                                           class="minus decrease"><i
                                                                class="fas fa-minus"></i>
                                                        </a>
                                                        <input class="quantity" min="0"
                                                               name="item${cart[i]['id']}Amount"
                                                               id="item${cart[i]['id']}Amount"
                                                               value="${cart[i]['amount']}"
                                                               type="number">
                                                        <a onclick="addAmount(${cart[i]['id']})"
                                                           class="plus increase"><i
                                                                class="fas fa-plus"></i>
                                                        </a>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <div>
                                                    <button onclick="delItem(${cart[i]['id']})"
                                                            class="btn small text-uppercase mr-3">
                                                        <i
                                                                class="fas fa-trash-alt mr-1"></i> Убрать из
                                                        корзины
                                                    </button>
                                                </div>
                                                <p class="mb-0"><span
                                                        id="item{{ cp.id }}Price">${cart[i]['price']}</span>
                                                    X <span id="item{{ cp.id }}Count">${cart[i]['amount']}</span>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                    `
                }
                $('#delete_item').html(text);
                $(`#totalCheck`).html();
            }
            $('#cartSize').html(cartAmount);
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
}


function courierSel() {

    $('#delType').html('курьером');

    $('#optionalFields').css('display', 'block');
}

function selfSel() {

    $('#delType').html('самовывоз');

    $('#optionalFields').css('display', 'none');
}