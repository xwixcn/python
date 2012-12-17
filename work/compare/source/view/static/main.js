$(document).ready(function() {
	setselect();
	showcasedata();

})

function showcasedata() {
	$("#buttontype").click(function() {
		/* 根据select获取内容 */
		$("tbody").empty();
		var selecttext = "";
		var selectvalue = "";
		var selecttext = $("select").find("option:selected").text();
		var selectvalue = $("select").find("option:selected").attr("value");
		$(".addrow").remove();
		var addbutton = $('<input class="addrow" type="button" value="新增">')
		addbutton.click(function() {
			addrow(selectvalue);
		});
		addbutton.appendTo($("#addbutton"));
		$("#content").ajaxError(function(StatusText) {
			$(this).html("数据加载失败,请稍后再试....");
		});
		$("#content").ajaxStart(function() {
			$(this).html("");
		});
		var url = "/casemanager/tag/" + selectvalue;

		$.getJSON(url, function(json) {
			var tr = $("<tr><td>patternStr</td><td>patternCode</td><td>treeCode</td>" + "<td>md5</td><td>name</td><td>OPT</td></tr>")
			tr.appendTo($("table"));
			tr.attr("id", "tr" + 0);
			$("table").show();
			$.each(json, function(index, content) {
				var tr = $("<tr></tr>");
				var index = index + 1
				tr.attr("id", "tr" + index);
				tr.attr("class", "contentlist");
				$.each(content, function(i, Text) {
					if (i != "id") {
						var td = $("<td></td>");
						td.text(Text);
						td.attr("id", i);
						td.attr("class", "tdcontent" + index);
						td.appendTo(tr);
					}
				})
				var del = $("<button >删除</button>");
				del.attr("id", "del" + index);
				var submit = $("<button>提交</button>");
				submit.attr("id", "submit" + index);
				var td = $("<td></td>")
				del.appendTo(td);
				submit.appendTo(td);
				submit.hide();
				td.appendTo(tr);
				tr.appendTo($("table"));
				delrow(index, content.id, selectvalue);
				submitdata(index, selectvalue);
				edittable(index);
			});
			$.easypage({
				'contentclass': 'contentlist',
				'navigateid': 'navigatediv',
				'everycount': 2,
				'navigatecount': 5
			});
		});
	});

}

function addrow(selectvalue) {
	var tr = $("<tr></tr>");
	var index = Date.parse(new Date());
	tr.attr("id", "tr" + index);
	tr.attr("class", "contentlist");
	tr.appendTo($("tbody"));
	var newarry = {
		"patternStr": "",
		"patternCode": "",
		"treeCode": "",
		"md5": "",
		"name": "",
		"id": "sss"
	}
	$.each(newarry, function(i, Text) {
		if (i != "id") {
			var td = $("<td></td>");
			td.text(Text);
			td.attr("id", i);
			td.attr("class", "tdcontent" + index);
			td.appendTo(tr);
		}
	})
	var del = $("<button >删除</button>");
	del.attr("id", "del" + index);
	var submit = $("<button>提交</button>");
	submit.attr("id", "submit" + index);
	var td = $("<td></td>")
	del.appendTo(td);
	submit.appendTo(td);
	submit.hide();
	td.appendTo(tr);
	delrow(index, newarry["id"], selectvalue);
	submitdata(index, selectvalue);
	edittable(index);
	return false;
}

function delrow(index, iddata, selectvalue) {

	$("#del" + index).click(function() {
		if (confirm("确定要删除该行吗？"))
		/* 删除行数据 */
		{
			$.ajax({
				url: "/casemanager",
				data: {
					id: iddata,
					tag: selectvalue,
					opt: "delete"
				},
				success: function(msg) {
					$("#pcontent").html(msg);
					$("#pcontent").show("slow");
					$("#pcontent").hide("slow");
					$("#tr" + index).remove();
				},
				type: "POST",
				error: function() {
					var msg = "删除失败!"
					$("#pcontent").html("<font color='red>" + msg + "</font>");
					$("#pcontent").show("slow");
					$("#pcontent").hide("slow");
				}
			})
		}

	});

}

function submitdata(index, selectvalue) {
	$("#submit" + index).click(function() {
		/* 提交表格数据 */
		if (confirm("你确定要提交数据吗？")) {
			var data = new Array();
			$(".tdcontent" + index).each(function() {
				var changedata = $(this).attr('id') + "=" + $(this).text();
				data.push(changedata)
			})
			var postdata = data.join("&") + "&tag=" + selectvalue;
			$.ajax({
				url: "/casemanager",
				data: postdata,
				success: function(msg) {
					$("#pcontent").html(msg);
					$("#pcontent").show("slow");
					$("#pcontent").hide("slow");
					$('#submit' + index).hide()
				},
				type: "POST",
				error: function() {
					alert("提交失败");
				}
			})
		}
	})

}

function edittable(index) {
	$(".tdcontent" + index).dblclick(function() {
		/* 修改表格内容 */
		var objtd = $(this);
		var oldText = $.trim(objtd.text());
		var input = $("<input type='text'/>"); // 文本框的HTML代码
		objtd.html(input);
		input.click(function() {
			return false;
		});
		input.attr("value", oldText);
		input.css("border-width", "0px"); // 边框为0
		input.height(objtd.height()); // 文本框的高度为当前td单元格的高度
		input.width(objtd.width()); // 宽度为当前td单元格的宽度
		input.css("font-size", "14px"); // 文本框的内容文字大小为14px
		input.css("text-align", "center"); // 文本居中
		input.trigger("focus").trigger("select"); // 全选
		input.blur(function() {

			var newText = $(this).val();
			if (newText != oldText) {
				$('#submit' + index).show();
				var type = objtd.attr('id')

				objtd.html(newText);
			} else {
				objtd.html(oldText);
			}
		}

		)
	})

}
function setselect() {
	/* 设置select的值 */

	var url = '';
	$.getJSON('/casemanager/regression', function(json) {

		for (var x = 0; x < json.length; x++) {
			var option = $("<option></option>");
			option.text(json[x].name);
			option.attr("value", json[x].id);
			option.appendTo($("select"));

		}
		$("select").first().attr("selected='selected'");

	})

}
function runtask(id){
   
   $("#"+id).click(function(){
          $.ajax({
				url: "/start/multi",
				success: function(msg) {
                refresh();
				},
				type: "GET",
				error: function() {
				    $("#"+id).html("<font color='red'><strong>运行失败</strong></font>")	
                    refresh();
				}
			})
            $("#"+id).html("<font color='red'><strong>正在运行程序</strong></font> <a href='stoprun?cid=8&amp;cr=taskInfo&amp;id=136&amp;ref=P2NyPXRhc2tJbmZvJmNpZD04JnBhZ2U9'>停止运行</a>");
           }) 

}
function refresh()
{location.reload();
}
