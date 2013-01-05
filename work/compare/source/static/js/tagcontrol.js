var setting = {
	/*
	 * tree的配置文件
	 */
	view : {
		dblClickExpand : false
	},
	check : {
		enable : true
	},
	callback : {
		onRightClick : OnRightClick,
		onRename : OnRename,
		onRemove : OnRemove,
		onDrop : OnDrop

	},
	edit : {
		drag : {
			isMove : true,
			prev : false
		},
		enable : true,
		showRemoveBtn : false,
		showRenameBtn : false

	},
	data : {
		key : {
			children : "subtag"
		}
	}
};

var zNodes;
var tagdata = new Array();
function OnRightClick(event, treeId, treeNode) {
	/*
	 * 定义节点右键事件
	 */
	if (!treeNode && event.target.tagName.toLowerCase() != "button"
			&& jQuery(event.target).parents("a").length == 0) {
		zTree.cancelSelectedNode();
		showRMenu("root", event.clientX, event.clientY);
	} else if (treeNode && !treeNode.noR) {
		zTree.selectNode(treeNode);
		showRMenu("node", event.clientX, event.clientY);
	}
}

function showRMenu(type, x, y) {
	/*
	 * 显示菜单列表
	 */
	jQuery("#rMenu ul").show();
	if (type == "root") {
		jQuery("#m_del").hide();
		jQuery("#m_check").hide();
		jQuery("#m_unCheck").hide();
	} else {
		jQuery("#m_del").show();
		jQuery("#m_check").show();
		jQuery("#m_unCheck").show();
	}
	rMenu.css({
				"top" : y + "px",
				"left" : x + "px",
				"visibility" : "visible"
			});

	jQuery("body").bind("mousedown", onBodyMouseDown);
}

function hideRMenu() {
	/*
	 * 隐藏菜单列表
	 */
	if (rMenu)
		rMenu.css({
					"visibility" : "hidden"
				});
	jQuery("body").unbind("mousedown", onBodyMouseDown);
}
function onBodyMouseDown(event) {
	if (!(event.target.id == "rMenu" || jQuery(event.target).parents("#rMenu").length > 0)) {
		rMenu.css({
					"visibility" : "hidden"
				});
	}
}
var addCount = 1;
function OnRename(event, treeId, treeNode) {
	/*
	 * 当节点名字发生变化时候，把修改的数据添加到要提交的列表里
	 */
	var data = {
		"rootid" : getRootNode(treeNode).id,
		"previousTagId" : getParentId(treeNode),
		"name" : treeNode.name,
		"id" : treeNode.id,
		'opt' : 'edit'
	}
	if (treeNode.name != oldNodename) {
		$("#content").text(treeNode.name);
		tagdata.push(data)
	}
}
function OnRemove(event, treeId, treeNode) {
	/*
	 * 当移动节点后触发的操作
	 */

	var rootid = getRootNode(treeNode).id;
	var url = "/tag/edit/" + rootid;
	if (treeNode.id == "-1") {
		alert("新增节点就不搞传送了");
	} else {
		$.ajax({
					url : url,
					type : "POST",
					data : {
						"id" : treeNode.id,
						"opt" : "delete"
					},
					success : function(data) {
						$("#res").text(data);
						initTree();
					},
					error : function(textStatus) {
						alert(textStatus)
					}
				})
	}

}
function OnDrop(event, treeId, treeNodes, targetNode, moveType, isCopy) {

	var data = {
		"rootid" : getRootNode(targetNode).id,
		"previousTagId" : getParentId(treeNodes[0]),
		"id" : treeNodes[0].id,
		'opt' : 'mv'
	}
	tagdata.push(data);
}
var oldNodename;// 未修改前的节点名字
function editTreeNode() {
	/*
	 * 编辑节点
	 */
	hideRMenu();
	oldNodename = zTree.getSelectedNodes()[0].name;
	if (zTree.getSelectedNodes()[0]) {
		zTree.editName(zTree.getSelectedNodes()[0]);
	} else {
		zTree.editName(zTree.getSelectedNodes()[0]);
	}
}
function removeTreeNode() {
	/*
	 * 删除选中的节点
	 */
	hideRMenu();
	var nodes = zTree.getSelectedNodes();
	if (nodes && nodes.length > 0) {
		if (nodes[0].subtag && nodes[0].subtag.length > 0) {
			var msg = "要删除的节点是父节点，如果删除将连同子节点一起删掉。\n\n请确认！";
			if (confirm(msg) == true) {
				zTree.removeNode(nodes[0], callbackFlag = true);
			}
		} else {

			zTree.removeNode(nodes[0], callbackFlag = true);

		}
	}
}
function addTreeNode() {
	/*
	 * 添加节点
	 */
	hideRMenu();
	var newNode = {
		name : prompt("请输入tagName", "")

	};
	if (zTree.getSelectedNodes()[0]) {
		newNode.checked = zTree.getSelectedNodes()[0].checked;
		zTree.addNodes(zTree.getSelectedNodes()[0], newNode);
	} else {
		zTree.addNodes(null, newNode);
	}
	var data = {
		"rootid" : getRootNode(zTree.getSelectedNodes()[0]).id,
		"previousTagId" : null,
		"name" : newNode.name,
		"id" : "-1",
		'opt' : 'add'
	}

	if (zTree.getSelectedNodes()[0] == getRootNode(zTree.getSelectedNodes()[0])) {
		data.previousTagId = "None"
	} else {
		data.previousTagId = zTree.getSelectedNodes()[0].id
	}

	tagdata.push(data);

}

function getParentId(treenode) {
	/*
	 * 获取当前节点父节点
	 */
	var isparent;
	if (treenode.isParent) {
		isparent = "None";
	} else {
		isparent = treenode.getParentNode().id;
	}
	return isparent
}
function getRootNode(treenode) {
	/*
	 * 获取节点的根节点
	 */

	while (treenode.getParentNode()) {
		treenode = treenode.getParentNode()
	}
	return treenode
}
function tclick() {
	/*
	 * 提交修改的数据
	 */
	var i;

	if (tagdata.length == 0) {
		alert("没有对tag进行任何修改");
	} else {
		while (tagdata.length > 0) {
			var postdata = tagdata.pop();
			var url = "/tag/edit/" + postdata.rootid
			delete postdata.rootid
			$.ajax({
						url : url,
						type : "POST",
						data : postdata,
						success : function(data) {
							$("#res").text(data);
						},
						error : function(textStatus) {
							alert(textStatus)
						}
					})
		}
		initTree();
	}
}

function checkTreeNode(checked) {
	/*
	 * 选中当前节点
	 */
	var nodes = zTree.getSelectedNodes();
	if (nodes && nodes.length > 0) {
		var selectvalue = nodes[0].id;
		zTree.checkNode(nodes[0], checked, true);
		if (checked) {
			showcasedata(selectvalue)
		}
	}
	hideRMenu();
}
function resetTree() {
	/*
	 * 重置tree
	 */
	hideRMenu();
	tagdata.splice(0, tagdata.length);
	jQuery.fn.zTree.init(jQuery("#treeDemo"), setting, zNodes);
}

function showcasedata(selectvalue) {

	/* 根据select获取内容 */
	var selectvalue = selectvalue;
	$(".contentlist").remove();
	$(".singleadd").remove();
	$(".batchadd").remove();
	var Url = "/case/" + selectvalue;
	var singlebutton = $('<input class="singleadd" type="button" value="新增单个case">')
	var batchbutton=$('<input class="batchadd" type="button" value="批量增加case">')
	singlebutton.click(function() {
				addrow(selectvalue);
			});
			var posturl = "/case/edit/" + selectvalue;
	batchbutton.click(function(selectvalue){
		var scrollTop = document.body.scrollTop;
		if(scrollTop == 0){
			scrollTop = document.documentElement.scrollTop;
		}
		$('#caseform').attr("action",posturl);
		$("#cginfo").css("top",150+scrollTop);
		$("#cginfo").toggle("slow");
	

	});
	
	singlebutton.appendTo($("#Singleincrease"));
	batchbutton.appendTo($("#Batchincrease"));
	
	$.ajax({
				url : Url,
				statusCode : {
					404 : function() {
						alert("没有此tag数据");
					}
				},
				success : function(json) {
					var json = $.parseJSON(json);
					$.each(json, function(index, content) {
								var tr = $("<tr></tr>");
								var index = index + 1;
								tr.attr("id", "tr" + index);
								tr.attr("class", "contentlist");

								$.each(content, function(i, Text) {
											var td = $("<td></td>");
											td.text(Text);
											td.attr("id", i);
											td.attr("class", "tdcontent"
															+ index);
											td.appendTo(tr);
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
								'contentclass' : 'contentlist',
								'navigateid' : 'navigatediv',
								'everycount' : 50,
								'navigatecount' : 5
							});
				}
			});

}

function addrow(selectvalue) {
	/* 增加行 */
	var tr = $("<tr></tr>");
	var index = Date.parse(new Date());
	tr.attr("id", "tr" + index);
	tr.attr("class", "contentlist");
	tr.appendTo($("tbody"));
	var newarry = {
		"patternStr" : "",
		"patternCode" : "",
		"treeCode" : "",
		"md5" : "",
		"id" : "sss",
		"name" : ""

	}
	$.each(newarry, function(i, Text) {
				var td = $("<td></td>");
				td.text(Text);
				td.attr("id", i);
				td.attr("class", "tdcontent" + index);
				td.appendTo(tr);
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
						url : "/case/edit/" + selectvalue,
						data : {
							id : iddata,
							tag : selectvalue,
							opt : "delete"
						},
						success : function(msg) {
							$("#rescontent").html(msg);
							$("#rescontent").show("slow");
							$("#rescontent").hide("slow");
							$("#tr" + index).remove();
						},
						type : "POST",
						error : function() {
							var msg = "删除失败!"
							$("#pcontent").html("<font color='red>" + msg
									+ "</font>");
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
						var changedata = $(this).attr('id') + "="
								+ $(this).text();
						data.push(changedata)
					})
			var postdata = data.join("&") + "&tag=" + selectvalue;
			var url = "/case/edit/" + selectvalue;
			$.ajax({
						url : url,
						data : postdata,
						success : function(msg) {
							$("#rescontent").html(msg);
							$("#rescontent").show("slow");
							$("#rescontent").hide("slow");
							$('#submit' + index).hide()
						},
						type : "POST",
						error : function() {
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
function hidecaseform() {
 /*
  * 隐藏添加多个问句时候，弹出来的框
  */
	var clearTag = new Array("sitelist");
	for (key in clearTag) {
		$("#" + clearTag[key]).attr("value", "");
	}
	$("#cginfo").toggle("slow");

}
var zTree, rMenu;
function initTree() {
	/*
	 * 初始化tag树
	 */
	$.getJSON("/tag/get", function(data) {
				zNodes = data;
				jQuery.fn.zTree.init(jQuery("#treeDemo"), setting, zNodes);
				zTree = jQuery.fn.zTree.getZTreeObj("treeDemo");
				rMenu = jQuery("#rMenu");
				var node = zTree.getNodeByParam("name", "regression", null);
				zTree.expandNode(node, true, false, true);
			})
}
jQuery(document).ready(function(data) {
			initTree();
});
