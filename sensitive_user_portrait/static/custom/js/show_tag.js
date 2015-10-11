
function Draw_tag(data){
	//console.log(data);
	var item;
	var name;
	var value;
	var attrTag = [];
	var attributeNames = [];
	var attributeValues = [];
    for(var key in data){
		item = data[key];
	}
	//console.log(item);
    for(i=0;i<item.length;i++){
		attrTag.push(item[i].split(':'));
	}
	for(i=0;i<attrTag.length;i++){
		attributeNames.push(attrTag[i][0]);
		attributeValues.push(attrTag[i][1]);
		//console.log(attrTag[i][0]);
	}
	//console.log(attributeNames);
	$('#ptag').empty();
	var html = '';
	for(i=0;i<item.length;i++){
		html += '<div class="tagClo fleft" ><span class="ptagName" style="color:red;">'+attributeNames[i]+'</span>:';
        html += '<span class="tagbg"><span>'+attributeValues[i]+'<span><a id="delIcon"></a></span></div>';	
	}
	$('#ptag').append(html);

    deleteTag();
}

function deleteTag(){
	$('a[id^=delIcon]').click(function(e){
		var del_url = '/tag/delete_user_tag/?';
		var temp = $(this).parent().parent().parent().parent().remove();
		var delname = $(this).parent().parent().parent().prev().html();
		del_url = del_url +'uid=' + uid +'&attribute_name='+delname+'&user=admin';
		call_ajax_request(del_url, self_refresh);
	});
}

function Draw_tag_value(data){
	//console.log(data);
	$('#attribute_value_zh').empty();
	var html = '';
	html += '<select id="select_attribute_value">';
	for(i=0;i<data.length;i++){
		html += '<option value="'+data[i]+'">'+data[i]+'</option>';
	}
	$('#attribute_value_zh').append(html);
}

//选择类别
function Draw_tag_name(data){
	//console.log(data);
	$('#attribute_name_zh').empty();
	var html = '';
	html += '<select id="select_attribute_name">';
	for(i=0;i<data.length;i++){
		html += '<option value="'+data[i]+'">'+data[i]+'</option>';
	}
	$('#attribute_name_zh').append(html);

    $('#select_attribute_name').change(function(){
        var select_attribute_name = $("#select_attribute_name").val();
        var url_attribute_value = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
        call_ajax_request(url_attribute_value, Draw_tag_value);
    });

    var select_attribute_name = $("#select_attribute_name").val();
    var url_attribute_value = "/tag/show_attribute_value/?attribute_name="+select_attribute_name;
    call_ajax_request(url_attribute_value, Draw_tag_value);
}
function self_refresh(data){
    var show_url = '/tag/show_user_tag/?uid_list=' + uid;
    call_ajax_request(show_url, Draw_tag);
    /*
    $("#float-wrap").addClass("hidden");
    $("#tagInfo").addClass("hidden");
    */
    //window.location.reload();
}
function bind_button_click(){
    $("#tag").off("click").click(function(){
        //var show_url ="/tag/show_user_tag/?uid_list=3697357313";
        var show_url ="/tag/show_user_tag/?uid_list=" + uid;
        call_ajax_request(show_url, Draw_tag);

        var url_attribute_name = "/tag/show_attribute_name/";
        call_ajax_request(url_attribute_name, Draw_tag_name);

        $("#float-wrap").removeClass("hidden");
        $("#tagInfo").removeClass("hidden");
        return false;
    });
    $(".Tagclose").off("click").click(function(){
        $("#float-wrap").addClass("hidden");
        $("#tagInfo").addClass("hidden");
        return false;
    });
    $("#add_person_tag_button").click(function(){
        //获取所有类别名
        var new_attribute_name = $("#select_attribute_name").val();
        var new_attribute_value = $("#select_attribute_value").val();
        var attributeNames = [];
        var  tagnames = $('.ptagName').length;
        for(i=0;i<tagnames;i++){
            attributeNames.push($('.ptagName').eq(i).html());
        }
        //判断是否重复
        var count = 0;
        for(i=0;i<attributeNames.length;i++){
            if(new_attribute_name==attributeNames[i]){
                count += 0;
            }else{
                count ++;
            }
        }
        if(count==attributeNames.length){
            //添加新tag
            //var add_url = '/tag/add_attribute/?uid=3697357313&attribute_name='+new_attribute_name+'&attribute_value='+new_attribute_value+'&user=admint';
            var add_url = '/tag/add_attribute/?uid=' + uid + '&attribute_name='+new_attribute_name+'&attribute_value='+new_attribute_value+'&user=admint';
            call_ajax_request(add_url, self_refresh);
        }else{
            alert("已经存在相同的标签类型，新的标签名将替换原有的标签名！");
            var change_url = '/tag/change_attribute_portrait/?uid=' + uid + '&attribute_name='+new_attribute_name+'&attribute_value='+new_attribute_value+'&user=admint';
            call_ajax_request(change_url, self_refresh);
        }
    });
}

bind_button_click();

