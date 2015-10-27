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

function Search_weibo(){
  this.ajax_method = 'GET';
}

Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  
  Draw_basic: function(data){
    console.log(data);
    if (data['photo_url'] == 'unknown'){
       photo_url = "http://tp2.sinaimg.cn/1878376757/50/0/1";
    }else{
       photo_url = data['photo_url'];
           };
    if (data['politics_trend'] = 'left'){
        politics_trend = '偏左';
    }
    else if(data['politics_trend'] = 'right'){
        politics_trend = '偏右'; 
    }
    else{
        politics_trend = '中性';
    }
    if ((data['uname'] =='unknown') || (data['uname'] =='0')){
      uname = "未知";
    }
    else{
      uname = data['uname'];
    }
    global_uname = uname;
    $('#portrait_info').empty();
    html = '';
    html += '<div class="PortraitImg" ><span class="sensitive_name"></span></div>';
    html += '<div style="text-align:left;height:30px;margin-top:20px;float:left;">';
    html += '<span style="margin-right:30px"><img src=' + photo_url + '></span>';
    html += '<span style="margin-right:30px">昵称:<span><a target="_blank" href="/index/personal/?uid=' + data['uid'] + '">' + uname + '</a></span></span>';
    html += '<span style="margin-right:30px">政治倾向:<span>' + politics_trend + '</span></span>';
    html += '<span style="margin-right:20px">敏感度:<span>' + data['sensitive'].toFixed(2) + '</span></span>';
    html += '<span style="margin-right:20px">领域类别:<span>' + data['domain'] + '</span></span>';
    html += '</div>';
    html += '<div style="float:right;margin-top:10px;"><span><a target="_blank" href="/index/personal/?uid=' + data['uid'] + '">返回普通属性页面</a></span></div>';
    $('#portrait_info').append(html);
  draw_statictics_info_table(data);
  draw_influence_chart_info(data);
  draw_location_7_info(data);
  draw_today_sensi_word(data);
  draw_hashtag_cloud(data);
  draw_sensi_word_cloud(data);
  draw_sentiment_trend(data);
  var hashtag_table = data['sensitive_hashtag'];
  var sensiword_table = data['sensitive_words'];
  draw_hashtag_sensiword_table('hash_detail_body',hashtag_table);
  draw_hashtag_sensiword_table('sensi_detail_body',sensiword_table);
  var repost_table = data['sensitive_follow'];
  var retweeted_table = data['sensitive_retweet'];
  var top_at_table = data['sensitive_at'];
  draw_mutual_info('repost', repost_table);
  draw_mutual_info('retweeted', retweeted_table);
  draw_mutual_info('top_at', top_at_table);
  draw_more_mutual_info('more_repost_body', repost_table)
  draw_more_mutual_info('more_retweeted_body', retweeted_table);
  draw_more_mutual_info('more_rank_at_body', top_at_table);
  },
  Draw_sensi_word_table: function(data){
    $('#sensi_word_table').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:450px">';
    html += '<tr><th style="text-align:center;width:50px;">排名</th><th style="text-align:center;width:50px;">敏感词</th>';
    html += '<th style="text-align:center;width:50px;">词频</th><th style="text-align:center;width:50px;">等级</th><th style="text-align:center;width:50px;">类别</th></tr>';
    for (var i = 0; i < data.length; i++){
       var s = (i+1).toString();
       var m = i.toString();
       html += '<tr><th style="text-align:center;">' + s + '</th>';
       html += '<th style="text-align:center;">' + data[m]['0'] + '</th>';
       html += '<th style="text-align:center;">' + data[m]['1'] + '</th>';
       html += '<th style="text-align:center;">' + data[m]['2'] + '</th>';
       html += '<th style="text-align:center;">' + data[m]['3'] + '</th></tr>';      
    };
    html += '</table>'; 
    $('#sensi_word_table').append(html);
  },
  Draw_sort_sensitive_text: function(data){
    var page_num = 5;
    var total_pages = 0;
    if (data.length < page_num) {
          page_num = data.length
          page_sensitive_weibo( 0, page_num, data);
      }
      else {
          page_sensitive_weibo( 0, page_num, data);
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        page_icon(1,5,0);
    }else{
        page_icon(1,pageCount,0);
    }
    
    $("#pageGro li").live("click",function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#pageGro li.on").html())          
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        page_sensitive_weibo(start_row,end_row,data);
    });

    $("#pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index > 0){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html())  
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_sensitive_weibo(start_row,end_row,data);
    });
    

    $("#pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html()) 
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_sensitive_weibo(start_row,end_row,data);
    });
}
}

$('input[name="origin_re"]').click(function(){
var weibo_category = $('input[name="origin_re"]:checked').val();
var sort = $('input[name="seq_method"]:checked').val();
var sort_sensitive_text = "/attribute/sort_sensitive_text/?uid=" + uid + "&weibo_category=" + weibo_category + "&sort=" + sort;
Search_weibo.call_sync_ajax_request(sort_sensitive_text, Search_weibo.ajax_method, Search_weibo.Draw_sort_sensitive_text);
});

$('input[name="seq_method"]').click(function(){
var weibo_category = $('input[name="origin_re"]:checked').val();
var sort = $('input[name="seq_method"]:checked').val();
var sort_sensitive_text = "/attribute/sort_sensitive_text/?uid=" + uid + "&weibo_category=" + weibo_category + "&sort=" + sort;
Search_weibo.call_sync_ajax_request(sort_sensitive_text, Search_weibo.ajax_method, Search_weibo.Draw_sort_sensitive_text);
});

  function page_sensitive_weibo(start_row,end_row,data){
    var weibo_num = end_row - start_row;
    $('#weibo_content2').empty();
    if (weibo_num == 0){
        $('#weibo_content2').html('暂无微博数据');
        return;
    }
    var html = "";
    html += '<div class="group_weibo_font">';
    var colors = ['white', 'whitesmoke'];
    for (var s = start_row; s < end_row; s++){
        var timestamp = new Date(parseInt(data[s][0])*1000).format("yyyy-MM-dd hh:mm:ss");
        var geo = data[s][1];
        var text = data[s][2];
        var emotion_sort = data[s][5];
        if (emotion_sort == 0){
            emotion = '中性';
        }
        else if(emotion_sort == 1){
            emotion = '积极';
        }
        else{
            emotion = '消极';
        }
        var sensi_words_weibo = data[s][3];
        var retweeted_line_detail = data[s][4];
        var sensi_words_str = '';
        for (var i=0; i < sensi_words_weibo.length;i++){
            sensi_words_str += sensi_words_weibo[i] +'&nbsp;&nbsp;&nbsp;&nbsp;';
        }
        if (retweeted_line_detail != 0){
            var re_line = '<span style="margin-left:30px;"><a style="cursor:pointer;" data-toggle="modal"  data-target="#retweeted_line'+s+'">转发链</a></span>';
        }
        else{
            var re_line = '';
        }
        if (retweeted_line_detail.length != 0){
            var re_line_str='<p>';
            for (var i = retweeted_line_detail.length -1; i > -1 ; i--){
                re_line_str += retweeted_line_detail[i] +'&nbsp;&nbsp;<img style="width:40px;height:30px;" src="/static/custom/images/Arrow-icon.png">&nbsp;&nbsp;';
            }
            re_line_str += global_uname + '</p>';
            drawmodal(s,re_line_str);
        }

        html += '<div style="padding:10px;background:' + colors[(s+1)%2] + ';font-size:13px">';
        // html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
        html += '<p style="color:black;">'  + text + '</p>';
        html += '<p style="color:darkred;">敏感词：' + sensi_words_str +'&nbsp;&nbsp;情绪:<span style="color:red">'+ emotion + re_line+ '</span><span style="float:right">' + timestamp + '&nbsp;&nbsp;' + geo + '&nbsp;&nbsp;'+ '</span></p>';
        html += '</div>'
    }
    html += '</div>'; 
    $('#weibo_content2').append(html);
  }
  function draw_statictics_info_table(data){
    $('#statictics_info').empty();
    html = '';
    html += '<table class="statictics" width="750" border="1">';
    html += ' <tr>';
    html += '<td style="text-align:center" class="col_1">统计信息</td><td style="text-align:center">敏感/微博总数</td><td style="text-align:center">敏感/总转发</td><td style="text-align:center" >敏感/总评论</td>';
    html += '</tr>';
    html += '<tr>';
    html += '<td style="text-align:center"  class="col_1">原创</td>';
    html += '<td style="text-align:center"><span style="color:red">' + data['sensitive_origin_weibo_number'] + '</span>/<span>' + data['origin_weibo_total_number'] + '</span></td>';
    html += '<td style="text-align:center"><span style="color:red">' + data['sensitive_origin_weibo_retweeted_total_number'] + '</span>/<span>' + data['origin_weibo_retweeted_total_number'] + '</span></td>';
    html += '<td style="text-align:center"><span style="color:red">' + data['sensitive_origin_weibo_comment_total_number'] + '</span>/<span>' + data['origin_weibo_comment_total_number'] + '</span></td>';
    html += '</tr>';
    html += '<tr>';
    html += '<td style="text-align:center"  class="col_1">转发</td>';
    html += '<td style="text-align:center"> <span class="re_sensitive" style="color:red">' + data['sensitive_retweeted_weibo_number'] + '</span>/<span class="re_total">' + data['retweeted_weibo_total_number'] + '</span></td>';
    html += '<td style="text-align:center"><span class="re_sensitive" style="color:red">' + data['sensitive_retweeted_weibo_retweeted_total_number'] + '</span>/<span class="re_total">' + data['retweeted_weibo_retweeted_total_number'] + '</span></td>';
    html += '<td style="text-align:center"><span class="re_sensitive" style="color:red">' + data['sensitive_retweeted_weibo_comment_total_number'] + '</span>/<span class="re_total">' + data['retweeted_weibo_comment_total_number'] + '</span></td>';
    html += '</tr>';
    html += '</table>';
    $('#statictics_info').append(html);
  }
function draw_influence_chart_info(data){
    data_x = [];
    data_y = [];
    for (var i = 0; i < data['sensitive_time_distribute'].length; i++) {
        var s = i.toString();
        value_x = new Date(parseInt(data['sensitive_time_distribute'][s]['0'])*1000).format("MM-dd hh:mm");
        value_y = data['sensitive_time_distribute'][s]['1'];
        data_x.push(value_x);
        data_y.push(value_y);
       }
    var influenceChart = echarts.init(document.getElementById('influence_chart_info'));         
    var Influenceoption = {
        title : {
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['微博量']
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                //data : line_chart_dates
                data:data_x
            }
        ],
        yAxis : [
            {
                type : 'value',
            }
        ],
        series : [
            {
                name:'微博量',
                type:'line',
                //data:dataFixed,
                data:data_y,
                
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
        // 为echarts对象加载数据
    influenceChart.setOption(Influenceoption); 
}

function draw_location_7_info(data){
    $('#location_7_info').empty();
    html = '';
    html += '<h3 style="margin-left:40px;">一周活动轨迹</h3><div class="clearfix course_nr"><ul class="course_nr2" style="margin:0px;">';
    for (var i =0;i < data['sensitive_geo_distribute'].length; i++){
        s = i.toString();
        distribute_date = data['sensitive_geo_distribute'][s]['0'];
        if (data['sensitive_geo_distribute'][s]['1'].length == 0){
            distribute_geo = '无地理位置数据';
        }
        else{
            distribute_geo_total = data['sensitive_geo_distribute'][s]['1'];
            distribute_geo = distribute_geo_total['0']['0'];
        }      
        html += '<li class="shiji">';
        html += '<p><span class="ico">' + distribute_date + '</span>&nbsp&nbsp&nbsp---<span>' + distribute_geo + '</span></p>';
        html += '</li>';
    }
    html += '</ul></div>';
    $('#location_7_info').append(html);
}

function draw_today_sensi_word(data){
    $('#today_sensitive_word').empty();
    html = ''
    html += '今日敏感词：<strong>';
    for (var key in data['today_sensitive_words']){
        html += '<span>' + key + '&nbsp&nbsp</span>';
    }
    html += '</strong>'
    $('#today_sensitive_word').append(html);
}


function draw_hashtag_cloud(data){
    if (data['sensitive_hashtag'].length == 0){
        $('#hashtag_cloud').html('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;暂无数据');
    }
    else{
        keyword = [];
    for (i=0;i<data['sensitive_hashtag'].length;i++){
      s=i.toString();
      word = {};
      word['name'] = data['sensitive_hashtag'][s]['0'];
      word['value'] = data['sensitive_hashtag'][s]['1'];
      word['itemStyle'] = createRandomItemStyle();
      keyword.push(word);
    }
    var myChart = echarts.init(document.getElementById('hashtag_cloud'));
    var option = {
    title: {
        text: '',
    },
    tooltip: {
        show: true
    },
    series: [{
        name: '关键词',
        type: 'wordCloud',
        size: ['80%', '80%'],
        textRotation : [0, 45, 90, -45],
        textPadding: 0,
        autoSize: {
            enable: true,
            minSize: 15
        },
        data:keyword
    }]
};
                    
      myChart.setOption(option);
    }
    
}


function draw_sensi_word_cloud(data){
    if (data['sensitive_words'].length == 0){
        $('#sensi_word_cloud').html('暂无数据');
    }
    else{
        keyword = [];
        for (i=0;i<data['sensitive_words'].length;i++){
          s=i.toString();
          word = {};
          word['name'] = data['sensitive_words'][s]['0'];
          word['value'] = data['sensitive_words'][s]['1'];
          word['itemStyle'] = createRandomItemStyle();
          keyword.push(word);
        }
        var myChart = echarts.init(document.getElementById('sensi_word_cloud'));
        var option = {
        title: {
            text: '',
        },
        tooltip: {
            show: true
        },
        series: [{
            name: '关键词',
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 15
            },
            data:keyword
        }]
    };
                        
          myChart.setOption(option);
      }
}

function createRandomItemStyle(){
      
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
}

function draw_sentiment_trend(data){
    $('#sentiment_index_influence').empty();
    html = ''
    html += '负面指数：<strong>' + data['negetive_index'].toFixed(2) +'</strong>&nbsp;&nbsp;';
    html += '负面影响力：<strong>' + data['negetive_influence'].toFixed(2) +'</strong>';
    $('#sentiment_index_influence').append(html);
   negative_trend = data['sentiment_trend']['negetive'];
   neutral_trend = data['sentiment_trend']['neutral'];
   positive_trend = data['sentiment_trend']['positive'];
   negetive_trend_data = [];
   neutral_trend_data = [];
   positive_trend_data = [];
   date_data = [];
   for (var i = 0 ;i < negative_trend.length; i++){
      s = i.toString();
      negetive_data = negative_trend[s]['0'];
      negetive_trend_data.push(negetive_data); 
      neutral_data = neutral_trend[s]['0'];
      neutral_trend_data.push(neutral_data);
      positive_data = positive_trend[s]['0'];
      positive_trend_data.push(positive_data);
      date = negative_trend[s]['1'];
      date_data.push(date);
   }
   var emotion_charts = echarts.init(document.getElementById('emotion_chart'));
   var emotion_data = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['积极','消极','中性']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : date_data
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'积极',
            type:'line',
            stack: '总量',
            data:positive_trend_data
        },
        {
            name:'消极',
            type:'line',
            stack: '总量',
            data:negetive_trend_data
        },
        {
            name:'中性',
            type:'line',
            stack: '总量',
            data:neutral_trend_data
        }
    ]
};        
emotion_charts.setOption(emotion_data); 
}
//请求数据
var Search_weibo = new Search_weibo();
var global_uname;

$(document).ready(function(){
    console.log(uid);
    var sensitive_attribute_url = "/attribute/portrait_sensitive_attribute/?uid=" + uid;
    Search_weibo.call_sync_ajax_request(sensitive_attribute_url, Search_weibo.ajax_method, Search_weibo.Draw_basic);
    get_level = $("#sensi_word_level").val();
    get_category = $("#sensi_word_class").val();
    var level_category_url = "/attribute/sort_sensitive_words/?uid=" + uid + "&level=" + get_level + "&category=" + get_category;
    Search_weibo.call_sync_ajax_request(level_category_url, Search_weibo.ajax_method, Search_weibo.Draw_sensi_word_table);


    var weibo_category = $('input[name="origin_re"]:checked').val();
    var sort = $('input[name="seq_method"]:checked').val();
    var sort_sensitive_text = "/attribute/sort_sensitive_text/?uid=" + uid + "&weibo_category=" + weibo_category + "&sort=" + sort;
    Search_weibo.call_sync_ajax_request(sort_sensitive_text, Search_weibo.ajax_method, Search_weibo.Draw_sort_sensitive_text);
})

function draw_hashtag_sensiword_table(div,data){
    $('#'+div).empty();
    html = '';
    if (data.length == 0){
        $('#'+div).html('暂无数据');
    }
    else{
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">序号</th><th style="text-align:center">敏感词</th>';
        html += '<th style="text-align:center">词频</th><th style="text-align:center">等级</th><th style="text-align:center">类别</th></tr>';
        for (var i = 0; i < data.length; i++) {
           var s = (i+1).toString();
           var m = i.toString();
           html += '<tr><th style="text-align:center;">' + s + '</th>';
           html += '<th style="text-align:center;">' + data[m]['0'] + '</th>';
           html += '<th style="text-align:center;">' + data[m]['1'] + '</th>';
           html += '<th style="text-align:center;">' + data[m]['2'] + '</th>';
           html += '<th style="text-align:center;">' + data[m]['3'] + '</th></tr>';      
        };
        html += '</table>'; 
    }
    $('#'+div).append(html);
  }

function draw_mutual_info(div,data){
    $('#'+div).empty();
     html = '';
    if (data['1'] == 0){
     html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
     html += '<tr><th style="text-align:center">昵称</th>';
     html += '<th style="text-align:center">交互次数</th>';
     html += '<th style="text-align:center">是否入库</th></tr>';
    }
    else{
     html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
     html += '<tr><th style="text-align:center">昵称</th>';
     html += '<th style="text-align:center">交互次数</th>';
     html += '<th style="text-align:center">是否入库</th></tr>';
     var min_row = Math.min(5, data['0'].length);
     for (var i = 0; i < min_row; i++) {
       var s = (i+1).toString();
       var m = i.toString();
        if ((data['0'][m]['1']['0'] == 'unknown') || (data['0'][m]['1']['0'] == '0')){
           nickname = '未知';
       }
       else{
           nickname = data['0'][m]['1']['0'];
       }
       var in_status;
       if (data['0'][m]['1']['2'] == 0){
           in_status = '否';
       }
       else{
           in_status = '是';
       }
       html += '<tr>';
       html += '<th style="text-align:center;"><a target="_blank" href="/index/personal/?uid=' + data['0'][m]['0'] + '">' + nickname + '</a></th>';
       html += '<th style="text-align:center;">' + data['0'][m]['1']['1'] + '</th>';
       html += '<th style="text-align:center;">' + in_status + '</th></tr>';      
    };
    }
    html += '</table>';
    $('#'+div).append(html);
}

$('#show_sensi_word').click(function (){
    get_level = $("#sensi_word_level").val();
    get_category = $("#sensi_word_class").val();
    var level_category_url = "/attribute/sort_sensitive_words/?uid=" + uid + "&level=" + get_level + "&category=" + get_category;
    Search_weibo.call_sync_ajax_request(level_category_url, Search_weibo.ajax_method, Search_weibo.Draw_sensi_word_table);
    })
//转发链模态框
function drawmodal(id,data){
    var html = '<div class="modal fade" id="retweeted_line'+ id +'" tabindex="-1" role="dialog" aria-labelledby="sensi_detail_content"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"></button><h4 class="modal-title" id="sensi_detail_content">微博转发关系</h4></div><div class="modal-body" id="re_relation' + id + '">'+ data + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">关闭</button></div></div></div></div>';
    $('#weibo_re_modal').append(html);

}

function draw_more_mutual_info(div,data){
    $('#'+div).empty();
    html = '';
    if (data['1'] == 0){
        $('#'+div).html('暂无数据');
    }
    else
    {html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
     html += '<tr><th style="text-align:center">昵称</th>';
     html += '<th style="text-align:center">交互次数</th>';
     html += '<th style="text-align:center">是否入库</th></tr>';
     for (var i = 0; i < data['0'].length; i++) {
       var s = (i+1).toString();
       var m = i.toString();
        if ((data['0'][m]['1']['0'] == 'unknown') || (data['0'][m]['1']['0'] == '0')){
           nickname = '未知';
       }
       else{
           nickname = data['0'][m]['1']['0'];
       }
       var in_status;
       if (data['0'][m]['1']['2'] == 0){
           in_status = '否';
       }
       else{
           in_status = '是';
       }
       html += '<tr>';
       html += '<th style="text-align:center;"><a target="_blank" href="/index/personal/?uid=' + data['0'][m]['0'] + '">' + nickname + '</a></th>';
       html += '<th style="text-align:center;">' + data['0'][m]['1']['1'] + '</th>';
       html += '<th style="text-align:center;">' + in_status + '</th></tr>';      
    };
}
       $('#'+div).append(html);
}

