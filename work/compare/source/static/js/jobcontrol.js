

function addjob() {
	var id = $("tr").length;
	var type = "very";
	var select=$("<select id='myselect1'><option>请选择job类型</option></select>")
	var myselect1Array =["verify","monitor"];
	for(var i = 0 ; i < myselect1Array.length ; i++) {
				select.append("<option value='t0_" + i +  "'>" + myselect1Array[i] + "</option>");
			}
	var td=$("<td></td>")
	select.appendTo(td);
	var tr = $("<tr><td>" + id + "</td></tr>")
	td.appendTo(tr);
	var td = $("<td><a onclick='startjob(" + id
			+ ")'><font color='blue'>运行</font></a></td>")
	var td2 = $("<td>未启动</td><td><a id=look" + id + ">查看</a></td><td><a id=job"
			+ id + ">暂无</a></td>")
	td.attr("id", "run" + id);
	tr.attr("class", "tr" + id);
	td.appendTo(tr)
	td2.appendTo(tr)
	tr.appendTo($("table"));
}
function startjob(id) {
	
	var selectIndex = document.getElementById("myselect1").selectedIndex
	var selectText = document.getElementById("myselect1").options[selectIndex].text
	var url="/job/start/"+selectText
	alert(url);
	$.get(url, function(data) {
				var jsonobj = $.parseJSON(data);
				if (jsonobj.status == "-1") {
					$("#run" + id).next().html("<a>启动失败</a>");
				} else {
					$("#job" + id).text(jsonobj.jobid);
					var url = "/job/record/" + jsonobj.jobid;
					$("#look" + id).attr("href", url);
					$("#look" + id).attr("target", '_blank');
					getstatus(jsonobj.jobid, id);
				}

			})
}

function killjob(jobid) {
	var url = "/job/kill/" + jobid;
	$.get(url, function(data) {
				var jsonobj = $.parseJSON(data);
				alert(jsonobj.response);
				$("#run" + jobid).next().html("<a>运行结束</a>");
			})
}

function getstatus(jobid, id) {
	var url = "/job/status/" + jobid;
	$.get(url, function(data) {
		$(".statuscontent").empty();
		var jsonobj = $.parseJSON(data);
		var record = jsonobj.response;
		var timeout;
		if (record.indexOf("finish") != "-1"
				|| record.indexOf("failed") != "-1") {
			$("#run" + id).next().text("运行结束")
			clearTimeout(timeout);
		} else {
			$("#run" + id)
					.next()
					.html("<font color='green'><strong>正在运行中</strong></font><a onclick='killjob("
							+ jobid + ")'><font color='red'>停止运行</font></a>");
			timeout = setTimeout("getstatus(" + jobid + "," + id + ")", 3000);
		}
	})
}
function getdetailstatus() {
	var patharray = location.pathname.split('/');
	var jobid = patharray[patharray.length - 1];
	$("#pagetitle").text("第"+jobid+"次记录");
	var url = "/job/status/" + jobid;
	$.get(url, function(data) {
		$(".statuscontent").empty();
		var jsonobj = $.parseJSON(data);
		var record = jsonobj.response;
		var recordarry = record.split('!')
		$.each(recordarry, function(index) {
					var recordelem = $("<a>" + recordarry[index] + "<br/></a>");
					recordelem.appendTo($(".statuscontent"));

				})
		var timeout;
		if (record.indexOf("finish") != "-1"
				|| record.indexOf("failed") != "-1") {
			clearTimeout(timeout);
		} else {
			timeout = setTimeout("getdetailstatus()", 3000);
		}
	}

	)
}