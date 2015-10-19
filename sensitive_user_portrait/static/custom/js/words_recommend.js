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
  //console.log(date);
  return date;
}



var recommend_date=[];
function Draw_sensi_recommend_table(data){
	$('#sensi_manage_table').empty();
    var item = data;
    //console.log(item);
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>敏感词</th><th>出现次数</th><th>相关用户</th><th style="width:18px;text-align:center;"><input name="choose_all" id="choose_all"  type="checkbox" value="" onclick="choose_all()" /></th></tr>';
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

        html += '<td name="word">'+item[i][0]+'</td>';
        html += '<td name="count">'+item[i][2]+'</td>'+'<td name="user_list">';
		for( var s=0;s<item[i][1].length;s++){
			html += '<span style="margin-left:10px;">'+item[i][1][s]+'</span>';
		}
		html += '<td name="check" style="text-align:center;"><input name="recommend_word_all" class="recommend_word_all" type="checkbox" value=' + item[i][0] + '  />' + '</td>';
		//html += '</td>+<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="edit_word" data-toggle="modal" data-target="#word_edit">修改</a></td>';
		html += '</tr>';
	}

	html += '</tbody>';

	html += '</table>';
	html += '<br>'+'<button id="add_words" style="margin-left:850px;" class="btn btn-primary btn-sm" >添加入库</button>'

	$('#sensi_manage_table').append(html);
    //datatable
    $('.datatable').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[3]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }

function choose_all(){
  $('input[name="recommend_word_all"]').prop('checked', $("#choose_all").prop('checked'));
}
 

function date_initial(){
  var tomorrow = new Date(2013,8,8);
  $("#recommend_date_select").empty();
  var recommend_date_html = '';
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
  $("#recommend_date_select").append(recommend_date_html);
  return recommend_date;
}

$('#show_recommend_word').click(function(){

	var choose_date = $('#recommend_date_select option:selected').text();
	if (choose_date=="最近七天"){
		choose_date = data_list;
	}
  //console.log(choose_date);
  var url = '/manage_sensitive_words/recommend_new_words/?date_list='+choose_date;
	call_ajax_request(url, Draw_sensi_recommend_table);
    var global_pre_page = 1;
    var global_choose_uids = new Array();
});

var global_pre_page = 1;
var global_choose_uids = new Array();
date_initial();
var data_list = recommend_date.join(',');
var url_init = '/manage_sensitive_words/recommend_new_words/?date_list='+data_list;
call_ajax_request(url_init, Draw_sensi_recommend_table); 
var category_url = '/manage_sensitive_words/category_list/';
var category_list = new Array();
call_ajax_request(category_url, get_category_list);


function get_category_list(data){
    category_list = data;
}

$('#add_words').off("click").click(function(){
  $('.modal-body').empty();
  var cur_uids = []
  $('input[name="recommend_word_all"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var domain_word = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        domain_word.push(temp_list[i]);
      }
  }
  //console.log(domain_word);
  var len = domain_word.length;
  if (len < 1){
      alert("请选择至少1个敏感词!");
  }
  else{
    var html='';
    html += '<table id="total_table" class="add_word_model table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">敏感词</th><th style="text-align:center;vertical-align:middle">等级</th><th style="text-align:center;vertical-align:middle">类别</th></tr></thead>';
    html += '<tbody>';
    for(var i=0;i<domain_word.length;i++){
        html += '<tr>';
        html += '<td class="changeword center" style="text-align:center;vertical-align:middle">'+ domain_word[i] +'</td>';
        html += '<td class="center" style="text-align:center;vertical-align:middle"><select name="level" id="level_need" class="add_sensi_level" style="width:90px; margin-right:5px;"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td>'
        html += '<td class="center" style="text-align:center;vertical-align:middle"><select name="classify" class="add_sensi_class" style="width:90px; margin-right:5px;">';
        for (var j = 0; j < category_list.length; i++){
            html += '<option value=' + category_list[j] + '>' + category_list[j] + '</option>';
        }
        html += '</select></td>'    
        html += '</tr>';
   }
    html += '</tbody>';
    html += '</table>';
    $('.modal-body').append(html);
    $("#confirm_add").modal();
  }
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
  //console.log(word0);
  var domain_url = '/manage_sensitive_words/identify_in/?date='+date0+'&words_list='+word0+'&level_list='+level0+'&category_list='+category0;
  console.log(domain_url);
  call_ajax_request(domain_url, confirm_ok); 
  window.location.reload();
});
