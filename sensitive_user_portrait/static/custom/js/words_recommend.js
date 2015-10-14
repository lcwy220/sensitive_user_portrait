// Date format
Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
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



var recommend_date=[];
function Draw_sensi_recommend_table(data){
	$('#sensi_manage_table').empty();
    var item = data;
    console.log(item);
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
<<<<<<< HEAD
        html += '<td name="word">'+item[i][0]+'</td>';
        html += '<td name="count">'+item[i][2]+'</td>'+'<td name="user_list">';
		for( var s=0;s<item[i][1].length;s++){
			html += '<span style="margin-left:10px;">'+item[i][1][s]+'</span>';
=======
        html += '<td name="level">'+item[i][0]+'</td>';
        html += '<td name="class">'+item[i][2]+'</td>'+'<td name="time">';
        
		for( var s=0;s<item[i].uid.length;s++){
			var uid_list = item[i][1];
			html += '<span style="margin-left:10px;">'+uid_list[s]+'</span>';
>>>>>>> ef68e08917a406a02a0a3db8f98d952d2ca6a02f
		}
		html += '<td name="check"><input name="recommend_word_all" class="recommend_word_all" type="checkbox" value=""  />' + '</td>';
		//html += '</td>+<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}

	html += '</tbody>';

	html += '</table>';
	html += '<br>'+'<button id="add_words" ;" data-toggle="modal" data-target="#confirm_add" >确定添加</button>'

	$('#sensi_manage_table').append(html);
  }
<<<<<<< HEAD
var recommend_data = [{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']},{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']}];
url_init = '/manage_sensitive_words/recommend_new_words/?date_list='
call_ajax_request(url_init, Draw_sensi_recommend_table) 
=======
//var recommend_data = [{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']},{"level":'敏感词', "sensi_class":'10', "uid":['1234','2345','3456','4567']}];
 

>>>>>>> ef68e08917a406a02a0a3db8f98d952d2ca6a02f
function date_initial(){
  var tomorrow = new Date(2013,8,8);
  $("#recommend_date_select").empty();
  var recommend_date_html = '';
<<<<<<< HEAD
    var timestamp = 1378483200000;
    var date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    recommend_date[0]=date;
    recommend_date_html += '<option value="' + date + '" selected="selected">' + date + '</option>';      
    for (var i = 1; i < 7; i++) {
      timestamp = timestamp-24*3600*1000;
      date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
      recommend_date[i]=date;
      recommend_date_html += '<option value="' + recommend_date[i] + '">' + recommend_date[i] + '</option>';
    }
  recommend_date_html += '<option value="recommend_date_all" selected="selected">最近七天</option>';
=======
  recommend_date_html += '<option value="' + recommend_date[0] + 'id="' + recommend_date[0] + '">' + recommend_date[0] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[1] + 'id="' + recommend_date[1] + '">' + recommend_date[1] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[2] + 'id="' + recommend_date[2] + '">' + recommend_date[2] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[3] + 'id="' + recommend_date[3] + '">'+ recommend_date[3] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[4] + 'id="' + recommend_date[4] + '">' + recommend_date[4] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[5] + 'id="' + recommend_date[5] + '">' + recommend_date[5] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[6] + 'id="' + recommend_date[6] + '">' + recommend_date[6] + '</option>';
  recommend_date_html += '<option id="recommend_date_all" selected="selected">最近七天</option>';
>>>>>>> ef68e08917a406a02a0a3db8f98d952d2ca6a02f
  $("#recommend_date_select").append(recommend_date_html);
  return recommend_date;
}
date_initial();
<<<<<<< HEAD
var data_list = recommend_date.join(',');



$('#show_recommend_word').click(function(){

	var choose_date = $('#recommend_date_select option:selected').text();
	if (choose_date=="最近七天"){
		choose_date = data_list;
	}
  console.log(choose_date);
  var url = '/manage_sensitive_words/recommend_new_words/?date_list='+choose_date;
	call_ajax_request(url, Draw_sensi_recommend_table);
	});

var url_init = '/manage_sensitive_words/recommend_new_words/?date_list='+data_list;
call_ajax_request(url_init, Draw_sensi_recommend_table); 

$('#add_words').off("click").click(function(){
  $('.modal-body').html('');
  var domain_word = [];
  var html='';
  $('[name="recommend_word_all"]:checked').each(function(){
        domain_word.push($(this).parent().prev().prev().prev().text());

    });
    html += '<table id="total_table" class="add_word_model table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">敏感词</th><th style="text-align:center;vertical-align:middle">等级</th><th style="text-align:center;vertical-align:middle">类别</th></tr></thead>';
    html += '<tbody>';
  for(var i=0;i<domain_word.length;i++){
    html += '<tr>';
    html += '<td class="changeword center" style="text-align:center;vertical-align:middle">'+ domain_word[i] +'</td>';
    html += '<td class="center" style="text-align:center;vertical-align:middle"><select name="level" id="level_need" class="add_sensi_level" style="width:90px; margin-right:5px;"><option value="1">level 1</option><option value="2">level 2</option><option value="3">level 3</option></select></td>'
    html += '<td class="center" style="text-align:center;vertical-align:middle"><select name="classify" class="add_sensi_class" style="width:90px; margin-right:5px;"><option value="politics">politics</option><option value="military">military</option><option value="law">law</option><option value="ideology">ideology</option><option value="democracy">democracy</option></select></td>'    
    html += '</tr>';
   }
    html += '</tbody>';
    html += '</table>';
  $('.modal-body').append(html);
});

$('#modifySave').off("click").click(function(){
  var date0 = currentDate();
  var word00 = [];
  var level00 = [];
  var category00 = [];
  $('.changeword').each(function(){
    word00.push($(this).text());
    level00.push($(this).next().children('select').val());
    category00.push($(this).next().next().children('select').val());
  });

  var word0 = word00.join(',');
  var level0 = level00.join(',');
  var category0 = category00.join(',');
  console.log(word0);
  var domain_url = '/manage_sensitive_words/self_add_in/?date='+date0+'&word_list='+word0+'&level_list='+level0+'&category_list='+category0;
  call_ajax_request(domain_url, confirm_ok); 
  console.log(domain_url);
});
=======
function get_data_list(){
var data_list = [];
for(var i=0; i<7; i++){
	data_list.push($('#recommend_date['+i+']').text());
	}
return data_list;
}
var a= date_initial();
console.log(a);
url_init = '/manage_sensitive_words/recommend_new_words/?date_list='+a;
console.log(url_init);
call_ajax_request(url_init, Draw_sensi_recommend_table);

$('#show_recommend_word').click(function(){

	var choose_date = $('#recommend_date_select').val();
	if (choose_date="最近七天"){
		choose_date = date_initial();
	}
	var url = '/manage_sensitive_words/recommend_new_words/?date_list='+choose_date;
  console.log(url);
	call_ajax_request(url, Draw_sensi_recommend_table);
	})



$('#sensi_add_Save').click(function(){
	var add_level = $('sensi_add_Save').val();
	var add_class = $('sensi_add_class').val();

})

>>>>>>> ef68e08917a406a02a0a3db8f98d952d2ca6a02f
