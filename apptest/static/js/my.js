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
