function call_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'get',
      dataType: 'json',
      async: false,
      success:callback
    });
}
function Draw_sensi_manage_table(data){
	//console.log(data);
	$('#sensi_manage_table').empty();
    var item = data;
    console.log(item);
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>敏感词</th><th>等级</th><th>类别</th><th>时间</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="attribute_name">'+item[i].words+'</td>';
		/*var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" title="点击编辑">'+item_value+'</a></td>';
        }*/
        html += '<td name="level">'+item[i].level+'</td>';
        html += '<td name="class">'+item[i].sensi_class+'</td>';
		html += '<td name="time">'+item[i].date+'</td>';
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#sensi_manage_table').append(html);
  }

function addNew(){
    var newtag = $('.input_tag_box').val();
    if (newtag == ''){
        alert("不能为空！");
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
function get_input_data(){
    var temp='attribute_name=';
    var input_value;
    var input_name = "attribute_name=";
    var attribute_name = $("#show_sensi_manage").val();
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

$('#add_words_Save').off("click").click();



//var table_data1 = [{'words':'敏感词1','level':'A','sensi_class':'a类','date':'09-01'},{'words':'敏感词2','level':'A','sensi_class':'b类','date':'09-01'},{'words':'敏感词3','level':'B','sensi_class':'a类','date':'09-01'},{'words':'敏感词4','level':'B','sensi_class':'b类','date':'09-01'}];
all_words='/manage_sensitive_words/search_sensitive_words/?level=0&category='
	
call_ajax_request(all_words, Draw_sensi_manage_table);

$('#edit_word').click(function(){

})

$('#show_sensi_manage').click(function (){
    var word_level=$("#sensi_manage_level").val();
    var word_class=$("#sensi_manage_class").val();
    //alert(word_level);
    var base_choose_data_url = '/manage_sensitive_words/search_sensitive_words/?'
    var choose_data_url=base_choose_data_url+'level='+word_level+'&category='+word_class;
    //var need_data=[]
    
call_ajax_request(choose_data_url, Draw_sensi_manage_table);   
})

function self_refresh(){
    //var tag_url ="/tag/search_attribute/";
    //call_ajax_request(tag_url, Draw_tag_table);
    window.location.reload();
}

function deleteWords(){
    $('a[id^="delTag"]').click(function(e){
        var delete_url = "/manage_sensitive_words/self_delete/?";
        var temp = $(this).parent().prev().prev().prev().prev().html();
        delete_url += 'word=' + temp;
        console.log(delete_url);
        //window.location.href = url;
        call_ajax_request(delete_url, self_refresh);
    });
}
