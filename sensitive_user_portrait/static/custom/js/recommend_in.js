// Date format
Date.prototype.format = function(format){
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
function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}
function confirm_ok(data){
  //console.log(data);
  if(data)
    alert('操作成功！');
}
function draw_line_chart(xaxis, yaxis, div, uname){
  var uname_text = '"' + uname + '"的微博数';
  var line_chart_option = {
    title : {
        text: '用户微博走势图',
        subtext: '',
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:[uname_text]
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
            type : 'category',
            boundaryGap : false,
            axisLabel:{
              interval:5,
            },
            data : xaxis,
        }
    ],
    yAxis : [
        {
            type : 'value',
        }
    ],
    series : [
        {
            name:uname_text,
            type:'line',
            data:yaxis,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
    ]
  };
  var draw_init2 = echarts.init(document.getElementById(div));
  draw_init2.setOption(line_chart_option);
}
function draw_recommend(data){
    var div = '#recommend';
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    var html = '';
    html += '<table id="recommend_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:140px">用户ID</th><th>昵称</th><th>注册地</th>';
    html += '<th style="width:100px">粉丝数</th><th style="width:100px">微博数</th><th style="width:100px">影响力</th>';
    // global_index
    if(global_index == 2){
        html += '<th style="width:100px">敏感词</th>';
    }
    html += '<th style="width:100px">用户详情</th>';
    html += '<th style="width:18px;"><input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    html += '<tbody>';

    var item = data;
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知'){
        //item[i][5] = item[i][5].toFixed(2);
      }
      else{
          item[i][5] = '';
      }
      if (item[i][3] == '未知'){
          item[i][3] = '';
      }
      if (item[i][4] == '未知'){
          item[i][4] = '';
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      // global_index
      if(global_index == 2){
          html += '<td class="center" style="width:100px">'+ item[i][6] +'</td>';
          //[i][6]预留敏感词
      }
      html += '<td class="center" style="width:100px"><a style="cursor:pointer;" name="details" id="'+ item[i][0] +'" title="'+ item[i][1] +'">详情</a></td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    // global_index
    if (global_index == 2){
        $('#recommend_table_new').dataTable({
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "recommend_boot",
            "aoColumnDefs":[ {"bSortable": false, "aTargets":[8]}],
            "oLanguage": {
                "sLengthMenu": "_MENU_ 每页",
            }
        });
    }
    else{
        $('#recommend_table_new').dataTable({
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "recommend_boot",
            "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
            "oLanguage": {
                "sLengthMenu": "_MENU_ 每页",
            }
        });
    }
    // page control start
    recommend_pre_page = 1;
    recommend_choose_uids = new Array();
    // page control end
    
    $('[name="details"]').click(function(){
      var detail_uid = $(this).attr('id');
      var detail_uname = $(this).attr('title');
      var detail_url;
      // global_index
      if(global_index == 2){
        detail_url = '/recommentation/sensitive_show_in_more/?uid=' + detail_uid;
      }else{
        detail_url = '/recommentation/influence_show_in_more/?uid=' + detail_uid;
      }
      call_ajax_request(detail_url, show_details);
      function show_details(data){
        if(data['time_trend'].length==0){
          $('#line_chart').empty();
          $('#line_chart').append('<div style="text-align:center">暂无数据！</div>');
        }
        else{
          //$('#line_chart').empty();
          var line_chart_xaxis = [];
          for(var k in data['time_trend'][0])
            line_chart_xaxis.push(new Date(parseInt(data['time_trend'][0][k])*1000).format("MM-dd hh:mm"));
          var line_chart_yaxis = data['time_trend'][1];
          draw_line_chart(line_chart_xaxis.reverse(), line_chart_yaxis.reverse(), 'line_chart', detail_uname);
        }

        $('#place').empty();
        if(data['activity_geo'].length==0)
          $('#place').append('<h4 style="text-align:center">活跃地点</h4><div style="text-align:center">暂无数据！</div>');
        else{
          var place_html = '';
          place_html += '<h4 style="text-align:center">活跃地点</h4>';
          place_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          place_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">地点</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          place_html += '<tbody>';
          for(var m in data['activity_geo']){
            if(parseInt(m)<5){
              place_html += '<tr>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(m)+1) +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][0] +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][1] +'</td>';
              place_html += '</tr>';
            }
          }
          place_html += '</tbody>';
          place_html += '</table>';

          $('#place').append(place_html);
        }

        $('#hashtag').empty();
        if(data['hashtag'].length==0)
          $('#hashtag').append('<h4 style="text-align:center">HashTag</h4><div style="text-align:center">暂无数据！</div>');
        else{
          var hashtag_html = '';
          hashtag_html += '<h4 style="text-align:center">HashTag</h4>';
          hashtag_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          hashtag_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">HashTag</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          hashtag_html += '<tbody>';
          for(var n in data['hashtag']){
            if(parseInt(n)<5){
              hashtag_html += '<tr>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(n)+1) +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][0] +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][1] +'</td>';
              hashtag_html += '</tr>';
            }
          }
          hashtag_html += '</tbody>';
          hashtag_html += '</table>';
          $('#hashtag').append(hashtag_html);
        }

        $('#details_modal').modal();
      }
    });
}
function draw_history(data){
    //console.log(data);
    var div = "#history";
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    var html = '';
    html += '<table id="history_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:140px">用户ID</th><th>昵称</th><th>注册地</th><th style="width:100px">粉丝数</th>';
    html += '<th style="width:100px">微博数</th><th style="width:100px">影响力</th>';
    // global_index
    if(global_index == 2){
        html += '<th style="width:100px">敏感度</th>';
    }
    html = '<th>计算状态</th></tr></thead>';
    html += '<tbody>';
    var item = data;
    for(var i in item){
      item[i] = replace_space(item[i]);
      console.log('here2');
      if(item[i][5]!='未知'){
        //item[i][5] = item[i][5].toFixed(2);
      }
      else{
        item[i][5] = '';
      }
      if (item[i][3] == '未知'){
          item[i][3] = '';
      }
      if (item[i][4] == '未知'){
          item[i][4] = '';
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      var in_status;
      if(item[i][7]==2)
        in_status = "预约计算";
      else if(item[i][7]==3)
        in_status = "正在计算";
      else
        in_status = "计算完成";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      // global_index
      if(global_index == 2){
        html += '<td class="center" style="width:100px">'+ item[i][6] +'</td>';
        //[i][6]预留敏感词
      }
      html += '<td class="center">'+ in_status +'</td>';
      html += '</tr>';
    }
    console.log('here2');
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    console.log('here3');
    $('#history_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "history_boot",
        //"aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
}
function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}
function bindButtonClick(){
  $('input[name="important"]').click(function(){
      //console.log($("#recommend_date_select").val());
      var recommend_date;
      var history_recommend;
      global_index = $(this).val();
      console.log(global_index);
        
      date_initial();
      call_ajax_request(recommend_url_list[global_index]+date, draw_recommend);
      //call_ajax_request(history_url_list[global_index]+date, draw_history);

  });
  $('#recommend_date_button').click(function(){
      //console.log($("#recommend_date_select").val());
      var url_recommend_new = recommend_url_list[global_index] + $("#recommend_date_select").val();
      call_ajax_request(url_recommend_new, draw_recommend);
  });
  $('#history_date_button').click(function(){
      //console.log($("#history_date_select").val());
      var url_history_new = history_url_list[global_index] + $("#history_date_select").val();
      //console.log(url_history_new);
      //call_ajax_request(url_history_new, draw_history);
  });
    $('#recommend_button').click(function(){
          var cur_uids = [];
          $('input[name="in_status"]:checked').each(function(){
            cur_uids.push($(this).attr('value'));
          })
          recommend_choose_uids[recommend_pre_page] = cur_uids;
          var recommend_uids = [];
          for (var key in recommend_choose_uids){
              var temp_list = recommend_choose_uids[key];
              for (var i = 0;i < temp_list.length;i++){
                  recommend_uids.push(temp_list[i]);
              }
          }
          var recommend_date = $("#recommend_date_select").val()
          //console.log(recommend_date);
          //console.log(recommend_uids);
          var uids_trans = '';
          for(var i in recommend_uids){
              uids_trans += recommend_uids[i];
              if(i<(recommend_uids.length-1))
                uids_trans += ',';
          }
          if(recommend_uids.length == 0)
            alert("请选择至少一个用户！");
          else{
            var compute_time;
            var sure;
            if($('input[name="instant"]:checked').val()==1){
              compute_time = '1';
              sure = confirm('立即计算会消耗系统较多资源，您确定要立即计算吗？');
            }
            else{
                compute_time = '2';
                sure = confirm('您选择了预约计算，系统将在今日24:00自动启动计算！');
            }
            if (sure == true){
                  //console.log(compute_time);
                  $('#recommend').empty();
                  var waiting_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
                  $('#recommend').append(waiting_html);

                  var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + uids_trans + '&status=' + compute_time;
                  call_ajax_request(recommend_confirm_url, confirm_ok);
                  //console.log(recommend_confirm_url);
                  var url_recommend_new = recommend_url_list[global_index] + $("#recommend_date_select").val();
                  call_ajax_request(url_recommend_new, draw_recommend);

                  var url_history_new = history_url_list[global_index] + $("#history_date_select").val();
                  // call_ajax_request(url_history_new, draw_history);
            }
          }
    });
}

function date_initial(){
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
  recommend_date_html += '<option value="' + recommend_date[6] + '" selected="selected">' + recommend_date[6] + '</option>';
  $("#recommend_date_select").append(recommend_date_html);

  var history_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(tomorrow-24*60*60*1000*(7-i));
    history_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
  }
  $("#history_date_select").empty();
  var history_date_html = '';
  history_date_html += '<option value="' + history_date[0] + '">' + history_date[0] + '</option>';
  history_date_html += '<option value="' + history_date[1] + '">' + history_date[1] + '</option>';
  history_date_html += '<option value="' + history_date[2] + '">' + history_date[2] + '</option>';
  history_date_html += '<option value="' + history_date[3] + '">' + history_date[3] + '</option>';
  history_date_html += '<option value="' + history_date[4] + '">' + history_date[4] + '</option>';
  history_date_html += '<option value="' + history_date[5] + '">' + history_date[5] + '</option>';
  history_date_html += '<option value="' + history_date[6] + '" selected="selected">' + history_date[6] + '</option>';
  history_date_html += '<option value="all">全部</option>';
  $("#history_date_select").append(history_date_html);
}
var tomorrow = new Date(2013,8,8);
var now_date = new Date(tomorrow-24*60*60*1000);
var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());

// page control start
var recommend_pre_page = 1;
var recommend_choose_uids = new Array();
// page control end

var global_index = 1;
var recommend_url_list = new Array();
recommend_url_list[1] = '/recommentation/show_influence_list/?date=';
recommend_url_list[2] = '/recommentation/show_sensitive_list/?date=';
var history_url_list = new Array();
history_url_list[1] = '/recommentation/show_influence_history_in/?date=';
history_url_list[2] = '/recommentation/show_sensitive_history_in/?date=';
var date = '';
date_initial();
call_ajax_request(recommend_url_list[global_index]+date, draw_recommend);
//call_ajax_request(history_url_list[global_index]+date, draw_history);
bindButtonClick();
