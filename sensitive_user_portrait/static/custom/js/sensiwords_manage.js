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
		html += '<tr id=' + item[i][0] + '>'
		html += '<td name="attribute_name">'+item[i][0]+'</td>';
		html += '<td name="level">'+item[i][1]+'</td>';
        html += '<td name="class">'+item[i][2]+'</td>';
		//html += '<td name="time">'+item[i].date+'</td>';
		html += '<td name="operate" style="cursor:pointer;" ><a class="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a class="edit_word" id="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#sensi_manage_table').append(html);
    

    $('.delTag').off("click").click(function(){
        var delete_url = "/manage_sensitive_words/self_delete/?";
        var temp = $(this).parent().parent().attr('id');
        delete_url += 'word=' + temp;
        //console.log(delete_url);
        //window.location.href = url;
        call_ajax_request(delete_url, self_refresh);
    });

    $('.edit_word').off("click").click(function(){
        $('#edit_snesiword').empty();
        var word_level=$(this).parent().prev().prev().html()
        var word_class=$(this).parent().prev().html()
        //console.log(word_class);
        //console.log(word_level);
        var html = '';
        html += '<div class="edit_word_model" style="margin-top:12px;"><input id="input_sensi" name="input_sensi" style="min-width: 100px;margin-top:0px;" value="'+$(this).parent().prev().prev().prev().html()+'">';
        html += '选择等级<select name="level" id="edit_sensi_level" class="edit_sensi_level" style="width:60px; margin-right:5px;">';
        html += '<option value="1">1</option>   <option value="2" >2</option><option value="3">3</option></select>';
        html += '选择类别<select name="classify" id="edit_sensi_class" class="edit_sensi_class" style="width:100px; margin-right:5px;">';
        for (var i = 0;i < category_list.length; i++){
            html += '<option value=' + category_list[i] +'>' + category_list[i] + '</option>';
        }
        html += '</select></div>';
        //$('#edit_sensi_class option[value="'+ word_class +'"]').attr("selected", true);
        //$("#sel  option[value='s2'] ").attr("selected",true);
        //console.log(html);
        $('#edit_snesiword').append(html); 
        $('#edit_sensi_level').val(word_level);
        $('#edit_sensi_class').val(word_class);
       	
    })
    $('#word_modifySave').off("click").click(function(){
        var url = '/manage_sensitive_words/identify_in/?date=';
        var edit_date = currentDate();
        var date = new Array;
        date.push(edit_date);
        var word_level=$(".edit_sensi_level").val();
        var level = new Array;
        level.push(word_level);
        var word_class=$(".edit_sensi_class").val();
        var class_word = new Array;
        class_word.push(word_class);
        var word = $('#input_sensi').val()
        var word_list = new Array;
        word_list.push(word);
        if(word != ''){
        url += date+'&words_list='+word_list+'&level_list='+level+'&category_list='+class_word;
        console.log(url);
        call_ajax_request(url, self_refresh);
        }else{
            alert('敏感词不能为空！')
        } 
	})
    //datatable for page
    $('.datatable').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });

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
//var category_name= ['politics', 'military','law','ideology','democracy']
$('#free_add_class').off("click").click(function(){
    $('#exist_categroy').empty();
    var html = ''
    for (i=0;i<category_list.length;i++){
         html += '<span class="tagbg" id="" name="attrName"><span class="tagName">'+category_list[i]+'</span><a  class="delCon" id="delIcon"></a></span>';
    }
    $('#exist_categroy').append(html);
    $('a[id^="delIcon"]').click(function(e){
            $(this).parent().remove();
        });
});

$('#add_words_Save').off("click").click(function(){
    var add_words_name = new Array;
    var add_words_class = new Array;
    var add_words_level = new Array;
    var add_words_date = currentDate();
    $('.add_sensi_level').each(function(){
        var each_word_level = $(this).val();
        add_words_level.push(each_word_level);

    })
    $('.add_sensi_class').each(function(){
        var each_word_class = $(this).val();
        add_words_class.push(each_word_class);
    });
    var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
    $('[name="input_sensi"]').each(function(){
        var each_word_name = $(this).val();
        if (each_word_name == ''){
            //alert("敏感词不能为空！");
            //return false;
            add_words_name.push(each_word_name);
        }else{
            if (!each_word_name.match(reg)){
                alert('敏感词只能包含英文、汉字、数字和下划线,请重新输入!');

                return;

            }

            //console.log(each_word_name);
            add_words_name.push(each_word_name);
        }
        //console.log(add_words_name);
    });
    //console.log(add_words_name.length);
    //console.log(add_words_level.length);
    if (add_words_name.length == add_words_level.length){
        var url = '/manage_sensitive_words/identify_in/';
        var words_list = new Array();
        var class_list = new Array();
        var level_list = new Array();
        for (var i = 0;i < add_words_name.length;i++){
            if (add_words_name[i] == ''){
            }
            else{
                words_list.push(add_words_name[i]);
                class_list.push(add_words_class[i]);
                level_list.push(add_words_level[i]);
            }
        }
        if (words_list.length > 0){
            url += '?date='+ add_words_date + '&words_list=' + words_list.join(',') + '&level_list=' + level_list.join(',') + '&category_list=' + class_list.join(',');
            //console.log(url);
            call_ajax_request(url, self_refresh);
        }
        else{
            $('#add_sensiword').modal('hide');
        }
    }else{
        console.log('no');
        return 0;
    }
})


$(".addIcon").off("click").click(function(){
    var html = '';
    html = '<div class="add_word_model" style="margin-top:12px;"><input name="input_sensi" class="input_sensi" style="min-width: 50px;margin-top:0px;float:left;" placeholder="输入敏感词">';
    html +='<span style="margin-left:10px;">等级</span><select name="level" class="add_sensi_level" style="width:90px;margin-left:10px;margin-right:5px;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select>';
    html +='<span style="margin-left:10px;">类别</span><select name="classify" class="add_sensi_class" style="width:90px;margin-left:11px;margin-right:5px;">';
    for (var i = 0; i < category_list.length; i++){
        html += '<option value=' + category_list[i] + '>' + category_list[i] + '</option>';
    }
    html += '</select>';
    html +='</div>';
    $('#add_snesiword').append(html);
});


//var table_data1 = [{'words':'敏感词1','level':'A','sensi_class':'a类','date':'09-01'},{'words':'敏感词2','level':'A','sensi_class':'b类','date':'09-01'},{'words':'敏感词3','level':'B','sensi_class':'a类','date':'09-01'},{'words':'敏感词4','level':'B','sensi_class':'b类','date':'09-01'}];
var all_words='/manage_sensitive_words/search_sensitive_words/?level=0&category='
call_ajax_request(all_words, Draw_sensi_manage_table);
var category_list = new Array();
var category_url = '/manage_sensitive_words/category_list/';
call_ajax_request(category_url, get_category_list);

function get_category_list(data){
    category_list = data;
}

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
    //console.log(choose_data_url);
	call_ajax_request(choose_data_url, Draw_sensi_manage_table);   
})

function self_refresh(data){
    //console.log(data);
    window.location.reload();
}


$.ajax({
    type:"POST",
    url:"/ucenter/add_sensitive_words/",
    contentType:"application/json",
    data:JSON.stringify(sub_sen),
    dataType:"json",
    success:self_refresh,
});
    $('#recommend_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "custom_bootstrap",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}, {"bSortable": false, "aTargets":[7]}],   把第6 7列不排序
        "aaSorting":[[5,"desc"]],   

        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页",
        }
    });

                "aoColumnDefs": [ {"sWidth": "4.5em" ,"aTargets":[0]},{"sWidth": "4.5em" ,"aTargets":[1]}, {"sWidth": "6em" ,"aTargets":[2]},{"sWidth": "6em" ,"aTargets":[3]},{"sWidth": "7em" ,"aTargets":[4]},{"sWidth": "5em" ,"aTargets":[5]},{"sWidth": "6.6em" ,"aTargets":[6]},{"sWidth": "4em" ,"aTargets":[7]},{"sWidth": "6em" ,"aTargets":[8]},{"sWidth": "6em" ,"aTargets":[9]}],
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>"  宽度