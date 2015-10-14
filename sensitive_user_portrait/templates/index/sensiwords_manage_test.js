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
    
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>敏感词</th><th>等级</th><th>类别</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="attribute_name">'+item[i][0]+'</td>';
		/*var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" title="点击编辑">'+item_value+'</a></td>';
        }*/
        html += '<td name="level">'+item[i][1]+'</td>';
        html += '<td name="class">'+item[i][2]+'</td>';
		//html += '<td name="time">'+item[i].date+'</td>';
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" class="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" class="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#sensi_manage_table').append(html);

    $('.delTag').off("click").click(function(){

    var delete_url = "/manage_sensitive_words/self_delete/?";
    var temp = $(this).parent().prev().prev().prev().html();
    delete_url += 'word=' + temp;
    console.log(delete_url);
    //window.location.href = url;
    call_ajax_request(delete_url, self_refresh);
    });

    $('.edit_word').off("click").click(function(){
        $('#edit_snesiword').empty();
        var html = '';
        html = '<div class="edit_word_model" style="margin-top:12px;">本词等级:<select name="level" class="edit_sensi_level" style="width:90px; margin-right:5px;">  <option value="1">level 1</option>   <option value="2">level 2</option><option value="3">level 3</option></select>请选择类别:<select name="classify" class="edit_sensi_class" style="width:90px; margin-right:5px;">  <option value="politics">politics</option><option value="military">military</option><option value="law">law</option><option value="ideology">ideology</option><option value="democracy">democracy</option></select>';
        html += '<input name="input_sensi" style="min-width: 30px;margin-top:0px;" value="'+$(this).parent().prev().prev().prev().html()+'"></div>';
       $('#edit_snesiword').append(html); 
       //call_ajax_request(url, self_refresh); 
    })
    $('#word_modifySave').off("click").click(function(){
    var url = '/manage_sensitive_words/self_add_in/?date=';
    var edit_date = currentDate();
    var word_level=$(".edit_sensi_level").val();
    var word_class=$(".edit_sensi_class").val();
    var word = $("input[name='input_sensi']").val()
    url += edit_date+'&word='+word+'&level='+word_level+'&category='+word_class;
    console.log(url);
    call_ajax_request(url, self_refresh); 
})

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

    return date;
}

$('#add_words_Save').off("click").click(function(){
    var add_words_name = new Array;
    var add_words_class = new Array;
    var add_words_level = new Array;
    var add_words_date = currentDate();
    $('[name="input_sensi"]').each(function(){
        var each_word_name = $(this).val();
        if (each_word_name == ''){
        alert("敏感词不能为空！");
        return;
        }
        add_words_name.push(each_word_name);
    })
    $('.add_sensi_level').each(function(){
        var each_word_level = $(this).val();
        add_words_level.push(each_word_level);
    })
    $('.add_sensi_class').each(function(){
        var each_word_class = $(this).val();
        add_words_class.push(each_word_class);
    });
    url = '/manage_sensitive_words/identify_in/'
    url += '?date='+add_words_date + '&words_list=' +add_words_name + '&level_list=' + add_words_level + '&category_list=' + add_words_class;
    console.log(url);
})


$(".addIcon").off("click").click(function(){
        var html = '';
        html = '<div class="add_word_model" style="margin-top:12px;">等级:<select name="level" class="add_sensi_level" style="width:90px; margin-right:5px;">  <option value="1">level 1</option>   <option value="2">level 2</option><option value="3">level 3</option></select>类别:<select name="classify" class="add_sensi_class" style="width:90px; margin-right:5px;">  <option value="politics">politics</option><option value="military">military</option><option value="law">law</option><option value="ideology">ideology</option><option value="democracy">democracy</option></select><input name="input_sensi" class="input_sensi" style="min-width: 30px;margin-top:0px;" placeholder="输入敏感词"></div>';
        $('#add_word_div').append(html);
    });


//var table_data1 = [{'words':'敏感词1','level':'A','sensi_class':'a类','date':'09-01'},{'words':'敏感词2','level':'A','sensi_class':'b类','date':'09-01'},{'words':'敏感词3','level':'B','sensi_class':'a类','date':'09-01'},{'words':'敏感词4','level':'B','sensi_class':'b类','date':'09-01'}];
all_words='/manage_sensitive_words/search_sensitive_words/?level=0&category='
call_ajax_request(all_words, Draw_sensi_manage_table);

$('#edit_word').click(function(){

})

$('#show_sensi_manage').click(function (){
    var word_level=$("#sensi_manage_level").val();
    var word_class=$("#sensi_manage_class").val();
    if (word_class== 0){
        word_class = '';
    }
    //alert(word_level);
    var base_choose_data_url = '/manage_sensitive_words/search_sensitive_words/?'
    var choose_data_url=base_choose_data_url+'level='+word_level+'&category='+word_class;
    //var need_data=[]
    
call_ajax_request(choose_data_url, Draw_sensi_manage_table);   
})

function self_refresh(){

    window.location.reload();
}


