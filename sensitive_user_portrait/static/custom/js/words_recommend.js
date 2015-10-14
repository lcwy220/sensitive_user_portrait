function call_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'get',
      dataType: 'json',
      async: false,
      success:callback
    });
}
function confirm_ok(data){
  //console.log(data);
  if(data)
    alert('操作成功！');
}
function Draw_sensi_recommend_table(data){
	//console.log(data);
	$('#sensi_manage_table').empty();
    var item = data;
    
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>敏感词</th><th>次数</th><th>用户ID</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		//html += '<td name="attribute_name">'+item[i].words+'</td>';
		/*var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" title="点击编辑">'+item_value+'</a></td>';
        }*/
        html += '<td name="level">'+item[i].level+'</td>';
        html += '<td name="class">'+item[i].sensi_class+'</td>'+'<td name="time">';
        console.log(item[i].uid);
		for( var s=0;s<item[i].uid.length;s++){
			var uid_list = item[i].uid;
			html += '<span style="margin-left:10px;">'+uid_list[s]+'</span>';
		}
		html += '<td name="check"><input name="recommend_word_all" id="recommend_word_all" type="checkbox" value="" onclick="recommend_all()" />' + '</td>';
		//html += '</td>+<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}

	html += '</tbody>';

	html += '</table>';
	html += '<br>'+'<button id="add_words" style="float:left;" data-toggle="modal" data-target="#confirm_add" >确定添加</button>'

	$('#sensi_manage_table').append(html);
  }
var recommend_data = [{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']},{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']}];
url_init = '/manage_sensitive_words/recommend_new_words/?date_list='
call_ajax_request(url_init, Draw_sensi_recommend_table) 

function date_initial(){
  var tomorrow = new Date(2013,8,8);
  var recommend_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    recommend_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#recommend_date_select").empty();
  var recommend_date_html = '';
  recommend_date_html += '<option value="' + recommend_date[0] + '">' + recommend_date[0] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[1] + '">' + recommend_date[1] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[2] + '">' + recommend_date[2] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[3] + '">' + recommend_date[3] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[4] + '">' + recommend_date[4] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[5] + '">' + recommend_date[5] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[6] + '>' + recommend_date[6] + '</option>';
  recommend_date_html += '<option value="recommend_date_all" selected="selected">最近七天</option>';
  $("#recommend_date_select").append(recommend_date_html);

}
date_initial();
var data_list = [];
for(var i=0; i<7; i++){
	data_list.push($('#recommend_date['+i+']').innerText);
	}


$('#show_recommend_word').click(function(){

	var choose_date = $('recommend_date_select').val;
	if (choose_date="最近七天"){
		choose_date = date_list;
	}
	var url = '/manage_sensitive_words/recommend_new_words/?date_list='+choose_date;
	call_ajax_request(url, Draw_sensi_recommend_table())
	})
url_init = '/manage_sensitive_words/recommend_new_words/?date_list='+data_list;
call_ajax_request(url_init, Draw_sensi_recommend_table) 