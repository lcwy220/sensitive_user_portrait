
function call_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'get',
      dataType: 'json',
      async: false,
      success:callback
    });
}

function Draw_tag_table(data){
	//console.log(data);
    $('#Tagtable').empty();
    var item = data;
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>标签类别</th><th>标签名</th><th>创建者</th><th>时间</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(var i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="attribute_name">'+item[i].attribute_name+'</td>';
		var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" class="currentEdit" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" class="currentEdit fortag" title="点击编辑">'+item_value+'</a></td>';
        }
        html += '<td name="creater">'+item[i].user+'</td>';
		html += '<td name="time">'+item[i].date+'</td>'
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#Tagtable').append(html);
    
    editTag();
    deleteGroup();
}
function editTag(){
    $('.currentEdit').click(function(e){
        add_flag = false;
        var tagNames =  $(this).text();
        //console.log(tagNames);
        var tagname = new Array();
        if (tagNames.indexOf('/') > -1){
            tagname = tagNames.split('/');
        }
        else{
            if ($(this).hasClass('fortag')){
                tagname.push(tagNames);
            }
        }
        //console.log(tagname);
		$('#EDIT').empty();
		var html = '';
		html += '<div class="" style="margin-bottom:10px;"><span style="">标签类别&nbsp;&nbsp;&nbsp;&nbsp;</span>';
		html += '<span style="color:blue;" id="attributeName">'+$(this).parent().prev().html()+'</span ></div>';
		html += '<div class="" id=""><span style="margin-right:15px;">标签名</span>';
		for(i=0;i<tagname.length;i++){
			html += '<span class="tagbg" id="" name="attrName"><span class="tagName">'+tagname[i]+'</span><a  class="delCon" id="delIcon"></a></span>';
		}
		//html += '<input name="attribute_value" class="inputbox " type="text" value="" style="line-height:36px;">'
		html += '<span class="smallAdd"></span>'
		html += '</div>';
		$('#EDIT').append(html);
		$(".smallAdd").click(function(){
            //console.log("sadsd");
            if (!add_flag){
                add_flag = true;
                $(".smallAdd").before('<input name="newtag" id="newtag" class="input_tag_box" style="width:110px;" onkeydown="javascript:if (event.keyCode==13) addNew();"type="text" value="" style="line-height:36px;">');
            }
        });
		$('a[id^="delIcon"]').click(function(e){
			$(this).parent().remove();
		});
	});
}
function addNew(){
    var newtag = $('.input_tag_box').val();
    if (newtag == ''){
        alert("标签名不能为空！");
        return;
    }
    var tagnames = $('.tagName').length;
    var nameszh = [];
    for(i=0;i<tagnames;i++){
        nameszh.push($(".tagName").eq(i).html());
        //console.log(value);
    }
    var count = 0;
    for(i=0;i<nameszh.length;i++){
        if(newtag==nameszh[i]){
            count = count +0;
        }else{
            count = count +1;
        }
    }
    if(count==nameszh.length){
        add_flag = false;
        $(".input_tag_box").remove();
        $(".smallAdd").before('<span class="tagbg" id="" name="attrName"><span class="tagName">'+newtag+'</span><a  class="delCon" id="delIcon"></a></span>');
    }else{
        alert("已经存在相同标签名，请重新输入！");
    }
    $('a[id^="delIcon"]').click(function(e){
        $(this).parent().remove();
    });
}
function page_init(){
    $('.datatable').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
}
function self_refresh(){
    //var tag_url ="/tag/search_attribute/";
    //call_ajax_request(tag_url, Draw_tag_table);
    window.location.reload();
}

function deleteGroup(){
	$('a[id^="delTag"]').click(function(e){
		var delete_url = "/tag/delete_attribute/?";
		var temp = $(this).parent().prev().prev().prev().prev().html();
		delete_url += 'attribute_name=' + temp;
		console.log(delete_url);
		//window.location.href = url;
		call_ajax_request(delete_url, self_refresh);
	});
}

function get_search_data(){
	var temp='';
    var input_value;
    var input_name;
	 $('.searchinput').each(function(){
        input_name = $(this).attr('name')+'=';
        input_value = $(this).val()+'&';
        temp += input_name;
        temp += input_value;;
    });
	//console.log(temp);
	temp = temp.substring(0, temp.length-1);
	return temp;
}
function bindButtonClick(){
	$('#searchbtn').off("click").click(function(){
		var url = "/tag/search_attribute/?";
		url += get_search_data();
		$("#float-wrap").addClass("hidden");
        $("#SearchTab").addClass("hidden");
		call_ajax_request(url,Draw_tag_table);
        page_init();
	});
	$('#newTag').off("click").click(function(){
		var url = "/tag/submit_attribute/?";
        var input = get_input_data();
        if (input){
            console.log('true');
            url += input;
            call_ajax_request(url, self_refresh);
            //page_init();
            //$('#add').modal("hide");
        }
        else{
            console.log('false');
        }
	});
	$('#modifySave').off("click").click(function(){
		var url = "/tag/change_attribute/?";
		url += input_data();
		call_ajax_request(url, self_refresh);
        //page_init();
        //$('#editor').modal("hide");
	});
    $(".addIcon").off("click").click(function(){
        var html = '';
        html += '<div class="tagCols"><span style="margin-left:65px;">标签名</span><input name="user_attribute_value" class="inputbox " type="text" value="" style="margin-left:35px;"></div>';
        $('#ADDTAG').append(html);
    });
}


var add_flag;
var tag_url ="/tag/search_attribute/";
call_ajax_request(tag_url, Draw_tag_table);
bindButtonClick();


function cDate(){
	var myDate = new Date();
	var yy = myDate.getFullYear();
	var mm = myDate.getMonth() + 1;
	if(mm<10){
		mm = '0'+mm.toString();
		
	}
	var dd = myDate.getDate();
	if(dd<10){
		dd = '0'+dd.toString();
	}
	
	var date = yy.toString()+ '-' + mm.toString() + '-' + dd.toString();
	//console.log(date);
	return date;
}

function get_input_data(){
	var temp='attribute_name=';
    var input_value;
    var input_name = "attribute_name=";
	var attribute_name = $("#tagClass").val();
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]";

	if(!attribute_name.match(reg)){
		alert('标签类型只能包含英文、汉字、数字和下划线，请重新输入');
		$('#tagClass').focus();
        return false;
	}

    temp += attribute_name;
    var attribute_value_list = new Array();
    $("[name='user_attribute_value']").each(function(){
        var attribute_value = $(this).val();
        console.log(attribute_value);
        if (attribute_value){
            attribute_value_list.push(attribute_value);
        }
    });
    temp += '&' + 'attribute_value=' + attribute_value_list.join(',');
    temp += '&' + 'user=admin&date=' + currentDate();

	console.log(temp);
	return temp;
}
function currentDate(){
	var myDate = new Date();
	var yy = myDate.getFullYear();
	var mm = myDate.getMonth() + 1;
	if(mm<10){
		mm = '0'+mm.toString();
		
	}
	var dd = myDate.getDate();
	if(dd<10){
		dd = '0'+dd.toString();
	}
	
	var date = yy.toString()+ '-' + mm.toString() + '-' + dd.toString();
	console.log(date);
	return date;
}
function input_data(){
	var temp='';
    var input_value;
    var input_name;
	//console.log(tagnames);
	input_name = "attribute_name=";
	input_value = $('#attributeName').html()+'&';
	temp += input_name;
    temp += input_value;

	var tagnames = $('.tagName').length;
	input_name = "attribute_value=";
	var value = '';
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";	
	for(i=0;i<tagnames;i++){
		value += $(".tagName").eq(i).html()+',';
		//console.log(value);
	}
	value = value.substring(0,value.length-1);
	input_value = value+'&';
	temp += input_name;
    temp += input_value;

	input_name = "user=";
	input_value ="admint&";
	temp += input_name;
    temp += input_value;
	input_name = "date=";
	input_value =cDate()+'&';
	temp += input_name;
    temp += input_value;
	temp = temp.substring(0, temp.length-1);
	console.log(temp);
	return temp;
}
