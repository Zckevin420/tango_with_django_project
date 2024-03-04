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
function closeMessage() {
    document.getElementById('tipmessage').style.display = "none";
}

function showMessage(msgText) {
    var datime = 5000;

    if (msgText == 'pw') {
        msgText = '<ul><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>';
        datime = 10000
    }
    document.getElementById('tipmessage').style.display = "block";
    document.getElementById('tipmessage').innerHTML = msgText;
    setTimeout(closeMessage, datime);
}

function selectUser(element) {
  // 移除之前选择的元素的类
  document.querySelectorAll('.users-list li').forEach(li => {
    li.classList.remove('selected');
  });
  // 为当前点击的元素添加类
  element.classList.add('selected');
}

function confirmDelete(userid) {
    var baseUrl = "/deleteuser/";
    var deleteUrl = baseUrl + userid;
    // print(deleteUrl)
    var confirmAction = confirm("您确定要删除这个用户吗？");
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
    var confirmAction = confirm("您确定要删除这个用户吗？");
    if (confirmAction) {
        // 用户点击了"OK"，进行删除操作
        window.location.href = deleteUrl;
    } else {
        // 用户点击了"Cancel"，不做任何操作
    }
}

function editUserProfile(userid) {

}


function openModal(userid, username, email) {
    document.getElementById("modal_userid").value = userid;
    document.getElementById("modal_username").value = username;
    document.getElementById("modal_email").value = email;
    document.getElementById("myModal").style.display = "block";
}

function openItem(itemid, itemname, price, quantity) {
    document.getElementById("modal_itemid").value = itemid;
    document.getElementById("modal_itemname").value = itemname;
    document.getElementById("modal_price").value = price;
    document.getElementById("modal_quantity").value = quantity;
    document.getElementById("itemModal").style.display = "block";
}


function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

function closeItem() {
    document.getElementById("itemModal").style.display = "none";
}

function enableInput(inputId) {
    document.getElementById(inputId).disabled = false;
}

function submitForm() {
    var userid = document.getElementById("modal_userid").value; // 使用隐藏字段的值

    // 使用 fetch API 提交表单数据
    fetch(`/updateuser/${userid}/`, {
        method: 'POST',
        body: new FormData(document.getElementById('updateUserForm')),
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
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
            'X-CSRFToken': '{{ csrf_token }}'
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
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // 获取表单数据
    const form = document.getElementById('addItemForm');
    const formData = new FormData(form);

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
        console.log('Success:', data);
        // 关闭模态框
        document.getElementById('addItemModal').style.display = 'none';
        // 这里可以添加一些操作，如刷新页面或显示消息
        window.location.reload(); // 刷新页面
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function profileAndWalletForm() {
    const formData = new FormData(document.getElementById('profileAndWalletForm'));
    fetch('/updateprofileandwallet/', { // 替换为实际更新视图的URL
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
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
        window.location.reload(); // 刷新页面
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function verifyOldPassword() {
    const oldPassword = document.getElementById('old_password').value;
    console.log(oldPassword);

    // 创建一个 FormData 对象并添加旧密码
    const formData = new FormData();
    formData.append('old_password', oldPassword);

    fetch('/verifypassword/', {
        method: 'POST',
        body: formData, // 发送 FormData 对象
        headers: {
            'X-CSRFToken': csrftoken, // 确保你有获取 csrftoken 的逻辑
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

