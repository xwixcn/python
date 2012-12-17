function createAjax() {
	var xmlhttp;
	if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp = new XMLHttpRequest();
	}
	else { // code for IE6, IE5
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	return xmlhttp;
}

function startservice(url, id) {
	var xttp = createAjax();
	var x = document.getElementById(id)
	if (xttp) {
		xttp.open('GET', url, true);
		xttp.onreadystatechange = function(id) {
			if (xttp.readyState == 4) {
				if (xttp.status == 200) {
					x.textContent = "运行";
					x.disabled = false;
				}
				else {
					alert("服务端异常" + xttp.statusText);
					window.location.reload();
				}

			}
			else {
				x.textContent = "数据加载中..";
				x.disabled = true;
			}
		}
	}
	xttp.send();
}

function change_readonly() {
	var nodelist = document.getElementsByName("lname");
	var i = 0;

	for (i = 0; i < nodelist.length; i++) {
		nodelist[i].readOnly = false;
	}

}
function test() {
	document.getElementById('2').innerHTML = "";
}

