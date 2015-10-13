function call_ajax_request(url, callback){
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: false,
        success: callback
    });
}
var tomorrow = new Date(2013,8,8);

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
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href="/index/personal/?uid='+ item[i][2] +'" target="_blank">'+ item[i][2] +'</td>';
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
  var option = {
    title : {
        text: '7天用户影响力分布',
        subtext: 'XXX'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['一天前','两天前','三天前','四天前','五天前','六天前','七天前']
    },
    toolbox: {
        show : true,
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
            name:'一天前',
            type:'line',
            data:item[1][0]
        },
        {
            name:'两天前',
            type:'line',
            data:item[1][1]
        },
        {
            name:'三天前',
            type:'line',
            data:item[1][2]
        },
        {
            name:'四天前',
            type:'line',
            data:item[1][3]
        },
        {
            name:'五天前',
            type:'line',
            data:item[1][4]
        },
        {
            name:'六天前',
            type:'line',
            data:item[1][5]
        },
        {
            name:'七天前',
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
$('#domain_button').click(function(){
  var select_date = $('#total_date_select option:selected').val();
  var domain_text = $('#domain_select option:selected').text();  
  var select_index = $('input[name="index_select"]:checked').val();
  var url1 = '/influence_application/search_domain_influence/?date='+select_date+'&domain='+domain_text+'&order='+select_index;
  call_ajax_request(url1,draw_table);
  console.log(select_date,domain_text);
  //draw_table(data);
});

$(document).ready(function(){
  call_ajax_request(url2,draw_graph);
})
