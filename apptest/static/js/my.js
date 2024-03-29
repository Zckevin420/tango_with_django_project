//
/* */
/* 
var name = "Kevin"; // String -- var name = String("Kevin")
var v1 = name.length; // 5
var v2 = name[0]; // K
var v3 = name.trim // remove space
var v4 = name.substring(0, 2); // Ke
console.log(name); //like print

var loginEmail = document.getElementById("email");
var loginPassword = document.getElementById("password");
var loginImages = ["20", "24"];
*/
var csrftoken = '{{ csrf_token }}';

function closeMessage() {
    document.getElementById('tipmessage').style.display = "none";
}

function showMessage(msgText) {
    var datime = 5000;

    if (msgText == 'pw') {
        msgText = '<ul><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>';
        datime = 200000
    }
    document.getElementById('tipmessage').style.display = "block";
    document.getElementById('tipmessage').innerHTML = msgText;
    setTimeout(closeMessage, datime);
}




function confirmDelete(userid) {
    var baseUrl = "/deleteuser/";
    var deleteUrl = baseUrl + userid;
    // print(deleteUrl)
    var confirmAction = confirm("Are sure to delete the user");
    if (confirmAction) {
        // 用户点击了"OK"，进行删除操作
        window.location.href = deleteUrl;
    } else {
        // 用户点击了"Cancel"，不做任何操作
    }
}

function confirmDeleteItem(itemid) {
    var baseUrl = "/deleteitem/";
    var deleteUrl = baseUrl + itemid;
    // print(deleteUrl)
    var confirmAction = confirm("Are sure to delete the item");
    if (confirmAction) {
        // 用户点击了"OK"，进行删除操作
        window.location.href = deleteUrl;
    } else {
        // 用户点击了"Cancel"，不做任何操作
    }
}


function openModal(userid, username, email) {
    document.getElementById("modal_userid").value = userid;
    document.getElementById("modal_username").value = username;
    document.getElementById("modal_email").value = email;
    document.getElementById("myModal").style.display = "block";
    console.log(document.getElementById("modal_userid").value)
}

function openItem(itemid, itemname, price, quantity) {
    document.getElementById("modal_itemid").value = itemid;
    document.getElementById("modal_itemname").value = itemname;
    document.getElementById("modal_price").value = price;
    document.getElementById("modal_quantity").value = quantity;
    document.getElementById("itemModal").style.display = "block";
}

function openOrder(orderEmail, itemName, quantity, totalPrice, payTime) {
    // 设置模态框内容
    document.getElementById('m-email').textContent = 'User Email: ' + orderEmail;
    document.getElementById('m-itemname').textContent = 'Item ID: ' + itemName;
    document.getElementById('m-quantity').textContent = 'Quantity: ' + quantity;
    document.getElementById('modal_totalprice').textContent = 'Total Price: ' + totalPrice;
    document.getElementById('m-paytime').textContent = 'Pay time: ' + payTime;

    // 显示模态框
    document.getElementById("orderModal").style.display = "block";
}



function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

function closeOrder() {
    document.getElementById("orderModal").style.display = "none";
}

function closeItem() {
    document.getElementById("itemModal").style.display = "none";
}

// function enableInput(inputId) {
//     document.getElementById(inputId).disabled = false;
// }

function enableInput(inputId) {
    const inputField = document.getElementById(inputId);
    inputField.disabled = false;
    inputField.removeAttribute('disabled'); // 从<form>标签中解除输入字段
}

function submitForm() {
    var userid = document.getElementById("modal_userid").value; // 使用隐藏字段的值

    // 使用 fetch API 提交表单数据
    fetch(`/updateuser/${userid}/`, {
        method: 'POST',
        body: new FormData(document.getElementById('updateUserForm')),
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function enableInputAndSubmitUser() {
    document.getElementById('modal_username').disabled = false;
    document.getElementById('modal_email').disabled = false;
    submitForm(); // 然后调用 submitItem 函数
}

function submitItem() {
    var itemid = document.getElementById("modal_itemid").value; // 使用隐藏字段的值

    // 使用 fetch API 提交表单数据
    fetch(`/updateitem/${itemid}/`, {
        method: 'POST',
        body: new FormData(document.getElementById('updateItemForm')),
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function enableInputAndSubmitItem() {
    document.getElementById('modal_itemname').disabled = false;
    document.getElementById('modal_price').disabled = false;
    document.getElementById('modal_quantity').disabled = false;
    submitItem(); // 然后调用 submitItem 函数
}

function submitItemForm() {
    // 获取CSRF Token，假设你已经在模板中通过{% csrf_token %}渲染了它
    // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData(document.getElementById('addItemForm'));

    fetch('/additem/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken, // 需要在请求头中包含CSRF token
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        // console.log('Success:', data);
        // close modal
        document.getElementById('addItemModal').style.display = 'none';
        window.location.reload(); // reload page
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function profileAndWalletForm() {
    const formData = new FormData(document.getElementById('profileAndWalletForm'));
    fetch('/updateprofileandwallet/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Something went wrong');
    })
    .then(data => {
        console.log('Success:', data);
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function verifyOldPassword() {
    const oldPassword = document.getElementById('old_password').value;
    console.log(oldPassword);

    // Create FormData, object is old password
    const formData = new FormData();
    formData.append('old_password', oldPassword);

    fetch('/verifypassword/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_password_correct) {
            document.getElementById('new_password').disabled = false;
        } else {
            alert('Incorrect old password');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function submitTopUpForm() {
    const formData = new FormData(document.getElementById('topUpForm'));

    fetch('/topup/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success: ', data);
        window.location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function submitSearchForm() {
    // get search keyword
    const searchKeyword = document.getElementById('searchKeyword').value;

    // create formdata
    const formData = new FormData();
    formData.append('searchKeyword', searchKeyword);

    // 发送 POST 请求到后端
    fetch('/searchitem/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Search results:', data);
        updateItemsDisplay(data.items);
        var modalElement = document.getElementById('searchItemModel');
        var modalInstance = bootstrap.Modal.getInstance(modalElement);
        modalInstance.hide(); // 关闭模态框
    })
    .catch(error => console.error('Error:', error));
}

function updateItemsDisplay(items) {
    const container = document.querySelector('.card-container');
    container.innerHTML = '';

    items.forEach(item => {
        const card = `<div class="card" style="width: 18rem; float: left; margin: 10px;">
            <div class="card-body">
                <h5 class="card-title">${item.itemname}</h5>
                <p class="card-text" id="price_${item.itemid}">Price: £${item.price}</p>
                <input type="number" class="form-control quantity-input" id="quantity_${item.itemid}" name="numofitem_${item.itemid}" 
                        step="1" value="1" min="1" required onchange="updatePrice(${item.itemid}, ${item.price})">
                <button onclick="addToCart('${item.itemid}')" class="btn btn-primary">Add to Cart</button>
                <button onclick="checkWalletAndRedirect(${ item.price }, '${ item.itemid }', this)"
                                data-item-price="${ item.price }" class="btn btn-success">Pay Now</button>
            </div>
        </div>`;
        container.innerHTML += card;
    });
}

function updatePrice(itemid, itemPrice) {
    const quantityInput = document.getElementById(`quantity_${itemid}`).value;
    const newPrice = itemPrice * quantityInput;
    document.getElementById(`price_${itemid}`).innerText = `Price: £${newPrice.toFixed(2)}`;
}

function addToCart(itemid) {
    const quantityInput = document.getElementById(`quantity_${itemid}`);
    if (quantityInput) {
        quantity = quantityInput.value;
    }

    fetch(`/addToCart/${itemid}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        alert('Item added to cart successfully!');
    })
    .catch((error) => {
        alert('Error adding item to cart. Please try again.');
    });
}

function removeFromCart(itemid) {
    fetch(`/removeFromCart/${itemid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => {
        if (response.ok) {
            updateCartModal();  // reload to be the newest
        } else {
            alert('Failed to remove item from cart.');
        }
    })
    .catch(error => {
        console.error('Error removing item from cart:', error);
    });
}

function updateCartModal() {
    console.log('Updating cart modal...');
    fetch('/cartItems/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        const cartItemsContainer = document.getElementById('cartItemsContainer');
        cartItemsContainer.innerHTML = ''; // clear
        data.items.forEach(item => {
            // 创建卡片元素
            let card = document.createElement('div');
            card.className = 'card mb-3'; // use Bootstrap card
            card.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${item.itemname}</h5>
                    <p class="card-text">ID: ${item.itemid}</p>
                    <p class="card-text">Quantity: ${item.quantity}</p>
                    <p class="card-text" id="price_${item.itemid}">Price: £${item.price.toFixed(2)}</p>
                    <button class="btn btn-danger remove-item" data-itemid="${item.itemid}">Remove</button>
                    <input type="hidden" name="item_id[]" value="${item.itemid}">
                    <input type="hidden" name="quantity[]" value="${item.quantity}">
                    <input type="hidden" name="price[]" value="${item.price}">
                </div>
            `;
            // add card in the container
            cartItemsContainer.appendChild(card);
            updatePrice(item.itemid, item.price);
        });
        // renew total prise
        document.getElementById('totalPrice').textContent = `Total Price: £${data.total_price.toFixed(2)}`;

        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.getAttribute('data-itemid');
                removeFromCart(itemId);
            });
        });
    })
    .catch(error => {
        console.error('Error fetching cart items:', error);
    });
}

document.body.addEventListener('click', function(event) {
    if (event.target.matches('.bi-cart-fill')) {
        updateCartModal();
    }
});

// $('#cartModal').on('shown.bs.modal', function () {
//     const payAllButton = document.getElementById('payAll');
//     if (payAllButton) {
//         payAllButton.removeEventListener('click', payAllHandler); // 防止重复添加事件处理器
//         payAllButton.addEventListener('click', payAllHandler);
//     } else {
//         console.error('Element with id `payAll` was not found.');
//     }
// });


// document.addEventListener('DOMContentLoaded', (event) => {
//     const payAllButton = document.getElementById('payAll');
//     if (payAllButton) {
//         payAllButton.addEventListener('click', function() {
//             const totalPriceElement = document.getElementById('totalPrice');
//             const totalPrice = totalPriceElement.textContent.replace('Total Price: £', '');
//             window.location.href = `/addressPage/?price=${totalPrice}`;
//         });
//     }
// });

document.addEventListener('DOMContentLoaded', (event) => {
    const payAllButton = document.getElementById('payAll');
    if (payAllButton) {
        payAllButton.addEventListener('click', function() {
            const itemIds = Array.from(document.querySelectorAll('input[name="item_id[]"]')).map(input => input.value);
            const quantities = Array.from(document.querySelectorAll('input[name="quantity[]"]')).map(input => input.value);
            const prices = Array.from(document.querySelectorAll('input[name="price[]"]')).map(input => input.value);

            const searchParams = new URLSearchParams();
            itemIds.forEach((id, index) => {
                searchParams.append(`items[${index}][itemid]`, id);
                searchParams.append(`items[${index}][quantity]`, quantities[index]);
                searchParams.append(`items[${index}][price]`, prices[index]);
            });

            window.location.href = `/addressPage/?${searchParams.toString()}`;
        });
    }
});

function searchUser() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("userSearchBox");
    filter = input.value.toUpperCase();
    table = document.getElementById("userstable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2]; // 选择包含 email 的列
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function searchOrder() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("orderSearchBox");
    filter = input.value.toUpperCase();
    table = document.getElementById("orderstable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[2]; // 选择包含 email 的列
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function searchItem() {

    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("itemSearchBox");
    filter = input.value.toUpperCase();
    table = document.getElementById("itemstable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // 选择包含 email 的列
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function checkWalletAndRedirect(price, itemid) {
    const quantity = document.getElementById(`quantity_${itemid}`).value;

    const searchParams = new URLSearchParams({
        'items[0][itemid]': itemid,
        'items[0][quantity]': quantity,
        'items[0][price]': price,
    });

    fetch(`/checkWallet/?price=${price}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.can_afford) {
            window.location.href = `/addressPage/?${searchParams.toString()}`;
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}




function payTheBill() {

    const formData = new FormData(document.getElementById('addressForm'));
    formData.append('items_data', JSON.stringify(itemsData)); // Convert itemsData back to a JSON string and add it to the form data

    fetch('/payTheBill/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Payment successful!');
            window.location.href = '/home/';
        } else {
            alert('Pay the bill failed: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}



