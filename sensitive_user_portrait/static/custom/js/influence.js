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
        success: callback
    });
}

function select_init(){
  $("#domain").empty();
  var domain_html = '';
  domain_html += '<select id="domain_select">';
  domain_html += '<option value="1" selected="selected">维权律师</option>';
  domain_html += '<option value="2">作家写手</option>';
  domain_html += '<option value="3">专家学者</option>';
  domain_html += '<option value="4">草根红人</option>';
  domain_html += '<option value="5">宗教人士</option>';
  domain_html += '<option value="6">公知分子</option>';
  domain_html += '<option value="7">非公企业主</option>';
  domain_html += '<option value="8">独立媒体</option>';
  domain_html += '<option value="9">官方媒体</option>';
  domain_html += '<option value="10">公职人员</option>';
  domain_html += '<option value="11">文体明星</option>';
  domain_html += '<option value="12">社会公益</option>';
  domain_html += '</select>';
  $("#domain").append(domain_html);
}

function date_initial(){
  $("#domain_date").empty();
  var total_date_html = '';
  total_date_html += '<select id="total_date_select">';
    //var timestamp = Date.parse(new Date());
    var timestamp = 1378483200000;
    var date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    total_date_html += '<option value="' + date + '" selected="selected">' + date + '</option>';      
    for (var i = 0; i < 6; i++) {
        timestamp = timestamp-24*3600*1000;
        date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
        total_date_html += '<option value="' + date + '">' + date + '</option>';
    }
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


function draw_table(data){
    var select_index = $('input[name="index_select"]:checked').val();
    var item = data;
    var div = '#total_table0';
    console.log(select_index);
    $(div).empty();
    html = '';
    html += '<table id="total_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    if (select_index==1)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">影响力</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">重要度</th><th style="text-align:center;vertical-align:middle">活跃度</th></tr></thead>';
    else if(select_index==2)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发量</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">重要度</th><th style="text-align:center;vertical-align:middle">活跃度</th></tr></thead>';
    else if(select_index==3)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论量</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">重要度</th><th style="text-align:center;vertical-align:middle">活跃度</th></tr></thead>';
    else if(select_index==4)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">转发爆发度</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">重要度</th><th style="text-align:center;vertical-align:middle">活跃度</th></tr></thead>';
    else if(select_index==5)
      html += '<thead><tr><th style="text-align:center;vertical-align:middle">头像</th><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle">昵称</th><th style="text-align:center;vertical-align:middle">评论爆发度</th><th style="text-align:center;vertical-align:middle">敏感度</th><th style="text-align:center;vertical-align:middle">重要度</th><th style="text-align:center;vertical-align:middle">活跃度</th></tr></thead>';

    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][3]=="未知")
        item[i][3] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][0]!='未知'&&select_index==1)
        item[i][0] = item[i][0].toFixed(2);      
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      if(item[i][5]!='未知')
        item[i][5] = item[i][5].toFixed(2);      
      if(item[i][6]!='未知')
        item[i][6] = item[i][6].toFixed(2);  
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><img src="'+ item[i][3] +'" class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][1] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][1] +'" target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i][0] +'</td>';
      //html += '<td class="center" style="text-align:center;vertical-align:middle">'+ 'wait...' +'</td>';      
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

function draw_graph(data){
  var myChart = echarts.init(document.getElementById("distribute")); 
  var item = data;
  var total_date = [];
      //var timestamp = Date.parse(new Date());
  var timestamp = 1378483200000;
  total_date[0] = new Date(parseInt(timestamp)).format("yyyy-MM-dd");    
  for (var i = 1; i < 7; i++) {
        timestamp = timestamp-24*3600*1000;
        total_date[i] = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
  }

  var option = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:[total_date[0],total_date[1],total_date[2],total_date[3],total_date[4],total_date[5],total_date[6]]
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            name : '影响力',
            type : 'category',
            boundaryGap : false,
            data : ['0-200','200-500','500-700','700-900','900-1100','1100-10000']
        }
    ],
    yAxis : [
        {
            name : '人数',
            type : 'value'
        }
    ],
    series : [
        {
            name:total_date[0],
            type:'line',
            data:item[1][0]
        },
        {
            name:total_date[1],
            type:'line',
            data:item[1][1]
        },
        {
            name:total_date[2],
            type:'line',
            data:item[1][2]
        },
        {
            name:total_date[3],
            type:'line',
            data:item[1][3]
        },
        {
            name:total_date[4],
            type:'line',
            data:item[1][4]
        },
        {
            name:total_date[5],
            type:'line',
            data:item[1][5]
        },
        {
            name:total_date[6],
            type:'line',
            data:item[1][6]
        }
    ]
};
    myChart.setOption(option);   
}

date_initial();
select_init();
    var url2 = '/influence_application/influence_distribution';
$('#rank_submit').click(function(){
  var select_date = $('#total_date_select option:selected').val();
  var domain_text = $('#domain_select option:selected').text();  
  var select_index = $('input[name="index_select"]:checked').val();
  var url1 = '/influence_application/search_domain_influence/?date='+select_date+'&domain='+domain_text+'&order='+select_index;
  call_ajax_request(url1,draw_table);
  //draw_table(data);
});

$(document).ready(function(){
  var select_date = $('#total_date_select option:selected').val();
  var domain_text = $('#domain_select option:selected').text();  
  var select_index = $('input[name="index_select"]:checked').val();
  var url1 = '/influence_application/search_domain_influence/?date='+select_date+'&domain='+domain_text+'&order='+select_index;
  call_ajax_request(url1,draw_table);
  call_ajax_request(url2,draw_graph);
})
