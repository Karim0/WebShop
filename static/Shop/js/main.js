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
//
// var form = $("#test-form")
// var form2 = $('#add_prod_form')
// var form3 = $('#select_char')
// var form4 = $('#refresh_cart')
// var form5 = $('#open_order')
// var form6 = $('#make_order')
// var form7 = $('#call_back')
//
// form.on('submit', function (e) {
//     e.preventDefault();
// });
//
// function showDetails(url, tot_price) {
//     var data = {};
//     var csrf_token = $('#test-form [name="csrfmiddlewaretoken"]').val();
//     data["csrfmiddlewaretoken"] = csrf_token;
//
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var product = JSON.parse(data);
//             var text = "";
//             for (i in product['photos']) {
//                 text += `<img data-margin='auto' data-fit='cover' src="${product['photos'][i]}" alt="prod-name">`;
//             }
//
//             $("#product-photos").html(`<div class="fotorama"
//                                 data-allowfullscreen="native"
//                                 data-fit='none'
//                                 data-width='100%'
//                                 data-maxwidth='300px'
//                                 data-height='auto'
//                                 data-ratio="1/1"
//                                 data-nav="thumbs"
//                                 data-navposition="right"
//                                 data-arrows="false">
//                                 ${text}
//                             </div>`);
//             $('.fotorama').fotorama();
//
//             text = "<li class='headers'><label><span >В наличии</span><span>Размер</span><span>Цвет</span><span>Цена</span></li>";
//             for (i in product['chars']) {
//                 if (product['chars'][i]['sale'] !== null) {
//                     text += `<li>
//           <input onclick="selectChar(${product['chars'][i]['id']}, ${product['chars'][i]['amount']}, ${product['chars'][i]['price'] * (1 - product['chars'][i]['sale'] / 100)}, '${product['name']}', '${url}', '${tot_price}')" id="select${product['chars'][i]['id']}" type="submit" name="selection">`;
//                 } else {
//                     text += `<li>
//           <input onclick="selectChar(${product['chars'][i]['id']}, ${product['chars'][i]['amount']}, ${product['chars'][i]['price']}, '${product['name']}', '${url}', '${tot_price}')" id="select${product['chars'][i]['id']}" type="submit" name="selection">`;
//                 }
//                 if (product['chars'][i]['amount'] > 0) {
//                     text += `
//           <label for="select${product['chars'][i]['id']}">
//           <span id="amountCh">${product['chars'][i]['amount']}</span>
//           <span id="sizeCh"> ${product['chars'][i]['size']}</span>
//           <span id="colorCh">${product['chars'][i]['color_name']}</span>`;
//                 } else {
//                     text += `
//           <label for="select${product['chars'][i]['id']}">
//           <span id="amountCh"> ПРЕДЗАКАЗ </span>
//           <span id="sizeCh"> ${product['chars'][i]['size']}</span>
//           <span id="colorCh"> ${product['chars'][i]['color']}</span>`
//                 }
//                 if (product['chars'][i]['sale'] === null) {
//                     text += `<span id="priceCh">${product['chars'][i]['price']}тг</span>
//           </label>
//           </li>`;
//                 } else {
//                     text += `<span id="priceCh"><del>${product['chars'][i]['price']}тг</del> ${product['chars'][i]['price'] * (1 - product['chars'][i]['sale'] / 100)}тг </span>
//           </label>
//           </li>`;
//                 }
//             }
//
//             $("#product-infos").html(`<h4> ${product['name']} </h4>
//           <span> ${tot_price} </span>
//           <ul>
//           ${text}
//           </ul>
//           <div id="prInterface"></div>
//           <h5> Описание </h5>
//           <p>${product['short_desc']}
//           <span id="dots">...</span><span id="more-desc">${product['desc']}</span></p>
//           <button onclick="showMore()" id="desc-btn"> Подробнее </button>
//
//
//           </div>`);
//
//             document.getElementById('details-window').classList.add('active_prod');
//             $('body').css('overflow', 'hidden');
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//         }
//     })
// }
//
// form3.on('submit', function (e) {
//     e.preventDefault();
// });
//
// var tot_num;
// var tot_sum;
//
// function selectChar(id, amount, price, prodName, url, tot_price) {
//     var data = {}
//
//     data.product_id = id;
//
//
//     var url = form3.attr('action');
//     $.ajax({
//         url: url,
//         type: 'GET',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var info = JSON.parse(data);
//
//             tot_sum = info['price'];
//             tot_num = info['amount'];
//
//             $(`#prInterface`).html(`
//           <div class="prCounter">
//           <a onclick="minusCount(${price}, ${amount})"> <i class="fas fa-minus-circle"></i> </a>
//           <span id="amount"> ${tot_num} </span>
//           <a onclick="plusCount(${price}, ${amount})"> <i class="fas fa-plus-circle"></i> </a>
//           </div>
//           <div class="totalSum">
//           <h5> Общая сумма: <span id="tot-sum">${tot_sum}</span> тг</h5>
//           <div class="prButtons">
//           <button onclick="inst_buy(${id}, '${prodName}')" > Купить </button>
//           <form action="/shop/add_cart_prod" id="add_prod_form" class="form-inline">
//           <button type="submit" onclick="add_to_cart(${id}, '${prodName}')"> Добавить в корзину </button>
//           </form>
//           </div>`);
//
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
// function plusCount(price, amount) {
//     tot_num++;
//     tot_sum += price;
//     $(`#amount`).html(tot_num);
//     $(`#tot-sum`).html(tot_sum);
// }
//
// function minusCount(price, amount) {
//     tot_num--;
//     tot_sum -= price;
//     if (tot_num < 1 || tot_sum < price) {
//         tot_num = 1;
//         tot_sum = price;
//     }
//     $(`#amount`).html(tot_num);
//     $(`#tot-sum`).html(tot_sum);
// }
//
// form2.on('submit', function (e) {
//     e.preventDefault();
// });
//
// function add_to_cart(id, name) {
//     var data = {}
//     var csrf_token = $('#test-form [name="csrfmiddlewaretoken"]').val();
//     data["csrfmiddlewaretoken"] = csrf_token;
//
//     data.product_id = id;
//     data.amount = tot_num;
//
//     var url = form2.attr('action');
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var cart = JSON.parse(data);
//
//             var text = "";
//
//             var cartAmount = 0;
//
//
//             for (i in cart) {
//                 cartAmount += cart[i]['prod_amount']
//                 if (cart[i]['preOrder']) {
//                     text += `<li class="p-1">
//           <button onclick="del_prod(${cart[i]['id']})" class="del_btn"> <i class="fas fa-times"></i> </button>
//           <button onclick="showDetails('${cart[i]['url']}', '${cart[i]['fullPrice']}')"
//           type="submit"> ${name} ПРЕДЗАКАЗ </button>
//           <p> <span id="amount${cart[i]['id']}"> Кол-во: ${cart[i]['prod_amount']} </span>
//           <span id="price${cart[i]['id']}"> Цена: ${cart[i]['prod_tot_price']}тг</span></p>
//           </li>`
//                 } else {
//                     text += `<li class="p-1">
//           <button onclick="del_prod(${cart[i]['id']})" class="del_btn"> <i class="fas fa-times"></i> </button>
//           <button onclick="showDetails('${cart[i]['url']}', '${cart[i]['fullPrice']}')"
//           type="submit"> ${name} </button>
//           <p> <span id="amount${cart[i]['id']}"> Кол-во: ${cart[i]['prod_amount']} </span>
//           <span id="price${cart[i]['id']}"> Цена: ${cart[i]['prod_tot_price']}тг</span></p>
//           </li>`
//                 }
//             }
//             $('#cart-list').html(text)
//             var note = new jBox('Notice', {
//                 content: `Добавленно в корзину: ${name} кол-во: ${tot_num}шт.`,
//                 color: 'green',
//                 delayClose: 500,
//                 animation: 'tada',
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//
//             tot_num = 0;
//             tot_price = 0;
//             close_details()
//             $('#cartAmount').html(cartAmount)
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
// form4.on('submit', function (e) {
//     e.preventDefault();
// });
//
//
// function refresh_cart() {
//     var data = {}
//
//     var url = form4.attr('action');
//     $.ajax({
//         url: url,
//         type: 'GET',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var cart = JSON.parse(data);
//
//             var cartAmount = 0;
//
//
//             if (cart.length < 1) {
//                 $('#cart-list').html(`<li class="p-1">
//            <span> Пока ничего нет( </span>
//            </li>`);
//                 $('#make-order-div').css('display', 'none');
//                 $('#buy-prod').css('display', 'block');
//
//             } else {
//                 var text = ""
//                 for (i in cart) {
//                     cartAmount += cart[i]['prod_amount']
//
//
//                     if (cart[i]['preOrder']) {
//                         text += `<li class="p-1">
//             <button onclick="del_prod(${cart[i]['elemId']})" class="del_btn"> <i class="fas fa-times"></i> </button>
//             <button onclick="showProd('${cart[i]['url']}', '${cart[i]['fullPrice']}', ${cart[i]['id']}, ${cart[i]['amount']}, ${cart[i]['price']}, '${cart[i]['name']}')"
//             type="submit"> ${cart[i]['name']}  ПРЕДЗАКАЗ </button>
//             <p> <span id="amount${cart[i]['id']}"> Кол-во: ${cart[i]['prod_amount']} </span>
//             <span id="price${cart[i]['id']}"> Цена: ${cart[i]['prod_tot_price']}тг</span></p>
//             </li>`
//
//                     } else {
//                         text += `<li class="p-1">
//             <button onclick="del_prod(${cart[i]['elemId']})" class="del_btn"> <i class="fas fa-times"></i> </button>
//             <button onclick="showProd('${cart[i]['url']}', '${cart[i]['fullPrice']}', ${cart[i]['id']}, ${cart[i]['amount']}, ${cart[i]['price']}, '${cart[i]['name']}')"
//             type="submit"> ${cart[i]['name']} </button>
//             <p> <span id="amount${cart[i]['id']}"> Кол-во: ${cart[i]['prod_amount']} </span>
//             <span id="price${cart[i]['id']}"> Цена: ${cart[i]['prod_tot_price']}тг</span></p>
//             </li>`
//                     }
//                 }
//                 $('#cart-list').html(text)
//                 $('#make-order-div').css('display', 'block');
//                 $('#buy-prod').css('display', 'none');
//             }
//
//
//             $('#cartAmount').html(cartAmount)
//
//
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
//
// function showProd(url, fullPrice, id, amount, price, prodName) {
//
//     showDetails(url, fullPrice);
//
//     selectChar(id, amount, price, prodName, url, tot_price)
//
//
// }
//
// function open_order() {
//
//     $('#sub_btn').css('display', 'block')
//
//     var data = {}
//     var url = form5.attr('action');
//     $.ajax({
//         url: url,
//         type: 'GET',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var cart = JSON.parse(data);
//
//             var text = ""
//             var tot_sum = 0
//
//             for (i in cart) {
//                 text += `<li>
//           <img src="${cart[i]['photo']}" alt="${cart[i]['name']}">
//           <ul>
//           <li><span>${cart[i]["name"]}</span> </li>
//           <li><span>Цвет: ${cart[i]["color"]}</span></li>
//           <li><span>Размер: ${cart[i]["size"]}</span></li>
//           <li><span class="price_span">${cart[i]["price"]}тг X ${cart[i]["prod_amount"]}шт</span></li>
//           </ul>
//           </li>`
//                 tot_sum += cart[i]["price"] * cart[i]["prod_amount"]
//             }
//             $('#order_list').html(text)
//
//             $('#total_price_order').html(`${tot_sum}тг`)
//
//             document.getElementById('order-window-cover').style.display = 'block';
//             $('body').css('overflow', 'hidden');
//
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
//
// function inst_buy(id, name) {
//
//     var data = {}
//     var csrf_token = $('#test-form [name="csrfmiddlewaretoken"]').val();
//     data["csrfmiddlewaretoken"] = csrf_token;
//
//     data.product_id = id;
//     data.amount = tot_num;
//
//     var url = form2.attr('action');
//     $.ajax({
//         url: url,
//         type: 'POST',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var cart = JSON.parse(data);
//             var text = ""
//             var cartAmount = 0;
//
//             for (i in cart) {
//                 cartAmount += cart[i]['prod_amount']
//             }
//             tot_num = 0;
//             tot_price = 0;
//             close_details()
//             $('#cartAmount').html(cartAmount)
//             open_order()
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//                 position: {
//                     x: 'left',
//                     y: 'top'
//                 }
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
//
// function closeOrder() {
//     refresh_cart();
//     document.getElementById('order-window-cover').style.display = 'none';
//
//     $('body').css('overflow', 'visible');
// }
//
//
// form6.on('submit', function (e) {
//     e.preventDefault();
// });
//
// function make_order() {
//     var data = {};
//     var csrf_token = $('#test-form [name="csrfmiddlewaretoken"]').val();
//     data["csrfmiddlewaretoken"] = csrf_token;
//     var pass = true;
//
//
//     if ($('#name').val().length < 1) {
//         $("#name_warn").css('display', 'block');
//         pass = false;
//     } else {
//         data['name'] = $('#name').val();
//     }
//     if ($('#phone').val().length < 1) {
//         $("#phone_warn").css('display', 'block');
//         pass = false;
//     } else {
//         data['phone'] = $('#phone').val();
//     }
//     if ($('#address').val().length < 1) {
//         $("#address_warn").css('display', 'block');
//         pass = false;
//     } else {
//         data['address'] = $('#address').val();
//     }
//
//     if (pass) {
//         var url = form6.attr('action');
//
//         $('#sub_btn').css('display', 'none')
//         $.ajax({
//             url: url,
//             type: 'POST',
//             data: data,
//             caсhe: true,
//             success: function (data) {
//
//                 closeOrder();
//                 var note = new jBox('Notice', {
//                     content: "Ваш заказ принят, ожидайте звонка",
//                     color: 'green',
//                     delayClose: 500,
//                     animation: 'tada',
//                     position: {
//                         x: 'left',
//                         y: 'top'
//                     }
//
//                 });
//                 note.open();
//                 note.close();
//                 refresh_cart();
//
//             },
//             error: function () {
//                 var note = new jBox('Notice', {
//                     content: "Что то пошло не так, попробуйте позже`",
//                     color: 'red',
//                     delayClose: 2000,
//                     position: {
//                         x: 'left',
//                         y: 'top'
//                     }
//                 });
//                 note.open();
//                 note.close();
//             }
//         });
//     }
//
// }
//
//
// function del_prod(id) {
//     var data = {}
//     data.product_id = id;
//     var url = $('#del_prod').attr('action');
//
//     $.ajax({
//         url: url,
//         type: 'GET',
//         data: data,
//         caсhe: true,
//         success: function (data) {
//             var cart = JSON.parse(data);
//             var cartAmount = 0;
//
//             if (cart.length < 1) {
//                 $('#cart-list').html(`<li class="p-1">
//            <span> Пока ничего нет( </span>
//            </li>`);
//                 $('#make-order-div').css('display', 'none');
//                 $('#buy-prod').css('display', 'block');
//
//             } else {
//                 var text = ""
//                 for (i in cart) {
//                     cartAmount += i.amount;
//
//                     text += `<li class="p-1">
//             <button onclick="del_prod(${cart[i]['elemId']})" class="del_btn"> <i class="fas fa-times"></i> </button>
//             <button onclick="showProd('${cart[i]['url']}', '${cart[i]['fullPrice']}', ${cart[i]['id']}, ${cart[i]['amount']}, ${cart[i]['price']}, '${cart[i]['name']}')"
//             type="submit"> ${cart[i]['name']} </button>
//             <p> <span id="amount${cart[i]['id']}"> Кол-во: ${cart[i]['prod_amount']} </span>
//             <span id="price${cart[i]['id']}"> Цена: ${cart[i]['prod_tot_price']}тг</span></p>
//             </li>`
//                 }
//                 $('#cart-list').html(text)
//                 $('#buy-prod').css('display', 'none');
//             }
//             $('#cartAmount').html(cartAmount)
//         },
//         error: function () {
//             var note = new jBox('Notice', {
//                 content: "Что то пошло не так, попробуйте позже`",
//                 color: 'red',
//                 delayClose: 2000,
//             });
//             note.open();
//             note.close();
//         }
//     });
// }
//
//
// function show_callback() {
//     $("#callback_wrap").css('display', 'block');
//     $('#qbutton').css('display', 'inline-block')
// }
//
// function close_callback() {
//     $("#callback_wrap").css('display', 'none');
//     form7.trigger("reset");
// }
//
// function close_details() {
//     document.getElementById('details-window').classList.remove('active_prod');
//     $('body').css('overflow', 'visible');
// }
//
// form7.on('submit', function (e) {
//     e.preventDefault();
// });
//
//
// function sent_question() {
//     var data = {};
//     var csrf_token = $('#call_back [name="csrfmiddlewaretoken"]').val();
//     data["csrfmiddlewaretoken"] = csrf_token;
//     var pass = true;
//
//
//     if ($('#call_name').val().length < 1) {
//         $("#call_name_warn").css('display', 'block');
//         pass = false;
//     } else {
//         data['name'] = $('#call_name').val();
//     }
//     if ($('#call_phone').val().length < 1) {
//         $("#call_phone_warn").css('display', 'block');
//         pass = false;
//     } else {
//         data['phone'] = $('#call_phone').val();
//     }
//     data['question'] = $('#call_question').val();
//
//     $('#qbutton').css('display', 'none')
//     if (pass) {
//         var url = form7.attr('action');
//
//
//         $.ajax({
//             url: url,
//             type: 'POST',
//             data: data,
//             caсhe: true,
//             success: function (data) {
//                 var note = new jBox('Notice', {
//                     content: "Ваш вопрос отправлен, мы обязательно вам перезвоним",
//                     color: 'green',
//                     animation: 'tada',
//                     delayClose: 2000,
//                     position: {
//                         x: 'left',
//                         y: 'top'
//                     }
//                 });
//
//                 close_callback();
//                 note.open();
//                 note.close();
//             },
//             error: function () {
//                 var note = new jBox('Notice', {
//                     content: "Что то пошло не так, попробуйте позже`",
//                     color: 'red',
//                     delayClose: 2000,
//                     position: {
//                         x: 'left',
//                         y: 'top'
//                     }
//                 });
//                 callWindow.close()
//                 note.open();
//                 note.close();
//
//             }
//         });
//     }
// }
//
//
// function showMore() {
//     var dots = document.getElementById("dots");
//     var moreText = document.getElementById("more-desc");
//     var btnText = document.getElementById("desc-btn");
//
//     if (dots.style.display === "none") {
//         dots.style.display = "inline";
//         btnText.innerHTML = " Подробнее ";
//         moreText.style.display = "none";
//     } else {
//         dots.style.display = "none";
//         btnText.innerHTML = " Уменьшить ";
//         moreText.style.display = "inline";
//     }
// }
//
