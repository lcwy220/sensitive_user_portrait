var data = [['1','未知','3as','1',1.2423,'3as'],['d','未知','s','d',2.2342,'s'],['d','未知','s','d',2.2342,'s']];
var tomorrow = new Date(2013,8,8);
function select_init(){
  $("#domain").empty();
  var domain_html = '';
  domain_html += '<select id="domain_select">';
  domain_html += '<option value="1" selected="selected">高校微博</option>';
  domain_html += '<option value="2">境内机构</option>';
  domain_html += '<option value="3">境外机构</option>';
  domain_html += '<option value="4">媒体</option>';
  domain_html += '<option value="5">境外媒体</option>';
  domain_html += '<option value="6">民间组织</option>';
  domain_html += '<option value="7">律师</option>';
  domain_html += '<option value="8">政府机构人士</option>';
  domain_html += '<option value="9">媒体人士</option>';
  domain_html += '<option value="10">活跃人士</option>';
  domain_html += '<option value="11">草根</option>';
  domain_html += '<option value="12">商业人士</option>';
  domain_html += '<option value="13">其他</option>';
  domain_html += '</select>';
  $("#domain").append(domain_html);
}

function date_initial(){
  var total_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    total_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#domain_date").empty();
  var total_date_html = '';
  total_date_html += '<select id="total_date_select">';
  total_date_html += '<option value="' + total_date[0] + '">' + total_date[0] + '</option>';
  total_date_html += '<option value="' + total_date[1] + '">' + total_date[1] + '</option>';
  total_date_html += '<option value="' + total_date[2] + '">' + total_date[2] + '</option>';
  total_date_html += '<option value="' + total_date[3] + '">' + total_date[3] + '</option>';
  total_date_html += '<option value="' + total_date[4] + '">' + total_date[4] + '</option>';
  total_date_html += '<option value="' + total_date[5] + '">' + total_date[5] + '</option>';
  total_date_html += '<option value="' + total_date[6] + '" selected="selected">' + total_date[6] + '</option>';
  total_date_html += '</select>';
  $("#domain_date").append(total_date_html);
}

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}

function draw(data){
    //console.log(data);
    var div = '#total_table0';
    var select_index = $('input[name="index_select"]:checked').val();
    console.log(select_index);
    $(div).empty();
    html = '';
    html += '<table id="total_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    if (select_index==1)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">影响力</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">入库状态</th></thead>';
    else if(select_index==2)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发量</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">微博链接</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==3)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论量</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">微博链接</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==4)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发爆发度</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    else if(select_index==5)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">排名</th><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论爆发度</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][3] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][4] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][5] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][6] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#total_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
date_initial();

$('#domain_button').click(function(){
  console.log('aaa');
  draw(data);
});
