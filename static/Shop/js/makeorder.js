function addAmount(id) {
    $(`#item${id}Amount`).val(parseInt($(`#item${id}Amount`).val()) + 1);

    $(`#item${id}Count`).html($(`#item${id}Amount`).val());

    $(`#totalCheck`).html(parseInt($(`#item${id}Amount`).val()) * parseFloat($(`#item${id}Price`).html()));

    $(`#modifyItem${id}`).on('submit', function (e) {
        e.preventDefault();
    });

    let data = {};
    data.product_id = id;
    data.amount = parseInt($(`#item${id}Amount`).val());
    const url = $(`#modifyItem${id}`).attr('action');


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
                $('#cartItemsList').html(`
                пока нет товаров (
                `);
                $(`#totalCheck`).html('0');

            } else {
                let totals = 0;
                let text = "";
                for (let i in cart) {
                    cartAmount += 1;
                    let props = "";
                    totals += cart[i]['amount'] * cart[i]['price'];
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
                                                <form action="/shop/product/modify" id="modifyItem${cart[i]['id']}"
                                                                      method="get">
                                                    <div class="def-number-input number-input safari_only mb-0 w-100">
                                                        <button onclick="minusAmount(${cart[i]['id']})"
                                                           class="minus decrease"><i
                                                                class="fas fa-minus"></i>
                                                        </button>
                                                        <input class="quantity" min="0"
                                                               name="item${cart[i]['id']}Amount"
                                                               id="item${cart[i]['id']}Amount"
                                                               value="${cart[i]['amount']}"
                                                               type="number">
                                                        <button onclick="addAmount(${cart[i]['id']})"
                                                           class="plus increase"><i
                                                                class="fas fa-plus"></i>
                                                        </button>
                                                    </div>
                                                    </form>
                                                    
                                                </div>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-center">
                                                
                                                <form action="/shop/product/delete"
                                                                      id="delete_item${cart[i]['id']}"
                                                                      method="get">
                            
                                                                    <div>
                                                                        <button onclick="delItem(${cart[i]['id']})"
                                                                                class="btn small text-uppercase mr-3">
                                                                            <i
                                                                                    class="fas fa-trash-alt mr-1"></i>
                                                                            Убрать из
                                                                            корзины
                                                                        </button>
                                                                    </div>
                                                                </form>
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
                $('#cartItemsList').html(text);
                $(`#totalCheck`).html(totals);
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

function minusAmount(id) {
    var value = parseInt($(`#item${id}Amount`).val()) - 1;

    $(`#item${id}Amount`).val(value);

    $(`#item${id}Count`).html($(`#item${id}Amount`).val());

    $(`#totalCheck`).html(parseInt($(`#item${id}Amount`).val()) * parseFloat($(`#item${id}Price`).html()));

    $(`#modifyItem${id}`).on('submit', function (e) {
        e.preventDefault();
    });

    let data = {};
    data.product_id = id;
    data.amount = parseInt($(`#item${id}Amount`).val());
    const url = $(`#modifyItem${id}`).attr('action');

    console.log($(`#modifyItem${id}`));

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
                $('#cartItemsList').html(`
                пока нет товаров (
                `);
                $(`#totalCheck`).html('0');

            } else {
                let totals = 0;
                let text = "";
                for (let i in cart) {
                    cartAmount += 1;
                    let props = "";
                    totals += cart[i]['amount'] * cart[i]['price'];
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
                                                <form action="/shop/product/modify" id="modifyItem${cart[i]['id']}"
                                                                      method="get">
                                                    <div class="def-number-input number-input safari_only mb-0 w-100">
                                                        <button onclick="minusAmount(${cart[i]['id']})"
                                                           class="minus decrease"><i
                                                                class="fas fa-minus"></i>
                                                        </button>
                                                        <input class="quantity" min="0"
                                                               name="item${cart[i]['id']}Amount"
                                                               id="item${cart[i]['id']}Amount"
                                                               value="${cart[i]['amount']}"
                                                               type="number">
                                                        <button onclick="addAmount(${cart[i]['id']})"
                                                           class="plus increase"><i
                                                                class="fas fa-plus"></i>
                                                        </button>
                                                    </div>
                                                    </form>
                                                </div>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <form action="/shop/product/delete"
                                                                      id="delete_item${cart[i]['id']}"
                                                                      method="get">
                            
                                                                    <div>
                                                                        <button onclick="delItem(${cart[i]['id']})"
                                                                                class="btn small text-uppercase mr-3">
                                                                            <i
                                                                                    class="fas fa-trash-alt mr-1"></i>
                                                                            Убрать из
                                                                            корзины
                                                                        </button>
                                                                    </div>
                                                                </form>
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
                $('#cartItemsList').html(text);
                $(`#totalCheck`).html(totals);
            }
            $('#cartSize').html(cartAmount);
            $(`#cartProductAmount`).html(`<sup> ${cartAmount}</sup>`);
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

function delItem(id) {
    let data = {};
    data.product_id = id;

    $(`#delete_item${id}`).on('submit', function (e) {
        e.preventDefault();
    });

    const url = $(`#delete_item${id}`).attr('action');

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
                $(`#totalCheck`).html('0');
                $('#cartItemsList').html(`
                пока нет товаров (
                `);
            } else {
                let text = "";
                let totals = 0;
                for (let i in cart) {
                    cartAmount += 1;
                    let props = "";
                    totals += cart[i]['amount'] * cart[i]['price'];
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
                                                <form action="/shop/product/modify" id="modifyItem${cart[i]['id']}"
                                                                      method="get">
                                                    <div class="def-number-input number-input safari_only mb-0 w-100">
                                                        <button onclick="minusAmount(${cart[i]['id']})"
                                                           class="minus decrease"><i
                                                                class="fas fa-minus"></i>
                                                        </button>
                                                        <input class="quantity" min="0"
                                                               name="item${cart[i]['id']}Amount"
                                                               id="item${cart[i]['id']}Amount"
                                                               value="${cart[i]['amount']}"
                                                               type="number">
                                                        <button onclick="addAmount(${cart[i]['id']})"
                                                           class="plus increase"><i
                                                                class="fas fa-plus"></i>
                                                        </button>
                                                    </div>
                                                    </form>
                                                </div>
                                            </div>
                                            <div class="d-flex justify-content-between align-items-center">
                                                <form action="/shop/product/delete"
                                                                      id="delete_item${cart[i]['id']}"
                                                                      method="get">
                            
                                                                    <div>
                                                                        <button onclick="delItem(${cart[i]['id']})"
                                                                                class="btn small text-uppercase mr-3">
                                                                            <i
                                                                                    class="fas fa-trash-alt mr-1"></i>
                                                                            Убрать из
                                                                            корзины
                                                                        </button>
                                                                    </div>
                                                                </form>
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
                $('#cartItemsList').html(text);
                $(`#totalCheck`).html(totals);
                console.log(totals);
            }
            $('#cartSize').html(cartAmount);
            $(`#cartProductAmount`).html(`<sup> ${cartAmount}</sup>`);

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
    $('#address').removeAttr('required');
}

function paySel(type) {
    $('#paymentType').html(type);
}


$(`#make_order`).on('submit', function (e) {
    if (parseInt($('#cartSize').html()) === 0) {
        e.preventDefault();
        var note = new jBox('Notice', {
            content: "Ваша корзина пуста",
            color: 'red',
            delayClose: 2000,
            position: {
                x: 'left',
                y: 'top'
            }
        });
        note.open();
        note.close();
    }
});

function add_cart_fast(char_id) {

    $(`#fast_add_cart_${char_id}`).on('submit', function (e) {
        e.preventDefault();
        let data = {};

        data.prodchars = $(`#fast_add_cart_${char_id} [name="char_id"]`).val();
        data.amount = $(`#fast_add_cart_${char_id} [name="char_amount"]`).val();
        data.fast = $(`#fast_add_cart_${char_id} [name="is_fast"]`).val();


        const url = $(`#fast_add_cart_${char_id}`).attr('action');

        var csrf_token = $(`#fast_add_cart_${char_id} [name="csrfmiddlewaretoken"]`).val();

        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            caсhe: true,
            success: function (data) {
                const amount = JSON.parse(data)['amount'];
                $(`#cartProductAmount`).html(`<sup> ${amount}</sup>`);

                var note = new jBox('Notice', {
                    content: "Добавлен в корзину",
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

    $(`#fast_add_cart_${char_id}`).submit();

}




