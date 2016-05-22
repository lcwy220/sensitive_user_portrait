function g_basic(){
  this.ajax_method = 'GET';
}

g_basic.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  }
}

function draw_basic(data){
	console.log("group basic data: ");
	console.log(data);
	Draw_totalnumber(data);

    var topics = data['topic'];
    var domains = data['domain'];
    var politics = data['politics'];

    if(topics.length == 0){
        //$('#showmore_topic_influ').css('display', 'none');
        $('#group_topic').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(topics,'group_topic', 'influ_topic_WordList','showmore_topic');
    };
    if(domains.length == 0){
        //$('#showmore_domain_influ').css('display', 'none');
        $('#group_domain').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(domains,'group_domain', 'influ_domain_WordList','showmore_domain');
    }
    if(politics.length == 0){
        //$('#showmore_domain_influ').css('display', 'none');
        $('#group_politics').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        Draw_topic_group_spread(politics,'group_politics', 'influ_politics_WordList','showmore_politics');
    }

    var div_name = 'sensitiveCloud';
    var c_title = '敏感词';
    var cloud_data = data['sensitive_words'];
    drawSensitiveCloud(div_name, c_title, cloud_data);
    var div_name = 'hashtagCloud';
    var c_title = '微话题';
    var cloud_data = data['hashtag'];
    drawSensitiveCloud(div_name, c_title, cloud_data);
    var div_name = 'psychologyState';
    var c_title = '关键词';
    var cloud_data = data['keywords'];
    drawSensitiveCloud(div_name, c_title, cloud_data);
    
    var influ_his = data['influence_his'];
    if(influ_his[1][1] == 0 & influ_his[1][5] == 1){
        $('#influ_distribution').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        draw_influ_distribution(influ_his,'influ_distribution', '影响力排名');
    }

    var sensitive_his = data['sensitive_his'];
    if(sensitive_his[1][1] == 0 & sensitive_his[1][5] == 1){
        $('#group_sensitive_distribution').append('<div style="padding-top: 40%;margin-left:40%;">暂无数据</div>');
    }else{
        draw_influ_distribution(sensitive_his,'group_sensitive_distribution', '敏感度排名');
    }

    $('#sen_words').empty();
    var html = '';
    html += '<table id="modal_online_pattern" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">敏感微话题</th><th style="text-align:center">词频</th></tr>';
    for (var i = 0; i < data['sensitive_hashtag'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['sensitive_hashtag'][s]['0'] +  '</th><th style="text-align:center">' + data['sensitive_hashtag'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#sen_words').append(html);  


}

//影响力分布
function draw_influ_distribution(data,radar_div, title){
    //console.log(data);
    var mychart1 = echarts.init(document.getElementById(radar_div));
    var y_axi = data[0];
    var x_axi = data[1];
    var xdata = [];
    var ydata = [];
    var count_sum = 0;
    for (var i =0; i < y_axi.length;i++){
        count_sum += y_axi[i];
        if(y_axi[i]!=0){
            xdata.push(data[1][i] + '-' + data[1][i+1]);
            ydata.push(data[0][i]);
        }
    }
    /*
    for (i = 0; i< data[1].length-1; i++){
        xdata.push(data[1][i] + '-' + data[1][i+1]);
    };
    */
    var option = {
    tooltip : {
        trigger: 'axis',
        formatter: "{a}<br/>{b} : {c}"
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            //scale: true,
            name : title,
            data : xdata
        }
    ],
    series : [
        {
            name:title,
            type:'bar',
            data:ydata
        }
    ]
    };
    mychart1.setOption(option);
}

//词云
function createRandomItemStyle() {
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

function drawSensitiveCloud(div_name, c_title, cloud_data){
 // console.log(c_title,cloud_data);
    var sensitiveChart = echarts.init(document.getElementById(div_name)); 
    function getCloudData(cloud_data){
        var chart_data = new Array();
        for (var i = 0;i < cloud_data.length;i++){
            var item = cloud_data[i];
            var item_dict =  {
                name: item[0],
                value: item[1] * 100,
                itemStyle: createRandomItemStyle()
            };
            chart_data.push(item_dict);
        }
        return chart_data;
    }
    
    var optionSensitive = {
        title: {
            text: c_title,
        },
        tooltip: {
            show: true
        },
        series: [{
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            data: []
        }]
    };
    var chart_data = getCloudData(cloud_data);
    optionSensitive["series"][0]["data"] = chart_data;
    sensitiveChart.setOption(optionSensitive);
}	  

function Draw_totalnumber(data){
    $('#totalnumber').empty();
    html = '';
    html += '<a class="well top-block" style="height: 200px;width: 200px;border-radius: 450px;margin-top: 40px;margin-left: 50px;">';
    html += '<div><img src="/static/img/user_group.png" style="height:40px;margin-top:40px"></div>';
    html += '<div>群组总人数</div>'
    html += '<div>' + data['count'] + '</div></a>';
    $('#totalnumber').append(html);
}
function toarray(a,b){
	this.names=a;
	this.num=b;
}
function draw_tag(data){
	var mychart1 = echarts.init(document.getElementById('group_tag'));
	var item = data['user_tag'];
	var items = [];
	var tagname= [];
	var tagvalue = [];
	for (var k in item){
		items.push(new toarray(k,item[k]));
	}
	items.sort(function(a,b){return a.num-b.num});
	for (var i=0;i< items.length;i++){
		tagname.push(items[i].names);
		tagvalue.push(items[i].num);
	}
	var option = {
    tooltip : {
        trigger: 'axis',
        formatter:"{b} : {c}",
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            data :tagname
        }
    ],
    series : [
        {
            // name:'2011年',
            type:'bar',
            data:tagvalue
        }
    ]
};
  mychart1.setOption(option);
}

function Draw_topic_group_spread(data, radar_div, motal_div, show_more){
  var topic = [];
  var html = '';
 // console.log(data);
    if(data[0][1] == 0){
      $('#'+ motal_div).empty();
      $('#'+ motal_div).empty();
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      $('#'+ radar_div).append(html);
      $('#'+ motal_div).append(html);
    }else{
      var topic_sta = [];
      var topic_name_sta = [];
      for(var i=0;i<data.length;i++){
        if(data[i][1] != 0){
          topic_sta.push(data[i][1]/data[0][1]);
          topic_name_sta.push(data[i][0]);
        }
      };
      $('#'+ motal_div).empty();
  if(topic_sta.length == 0){
      $('#'+ motal_div).empty();
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      //$('#'+ more_div).append(html);
      $('#'+ radar_div).append(html);
      $('#'+ motal_div).append(html);
      $('#'+ show_more).empty();
  }else{
      html = '';
      html += '<table class="table table-striped table-bordered">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">概率</th></tr>';
      for (var i = 0; i < topic_sta.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + topic_name_sta[i] +  '&psycho_status=&domain&topic" target="_blank">' + topic_name_sta[i] +  '</a></th><th style="text-align:center">' + topic_sta[i].toFixed(2) + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ motal_div).append(html);
    };



    var legends = [];
    for(i=0;i<data.length;i++){
      var cons={};
      name=data[i][0];
      value=data[i][1];
      cons.name=name;
      cons.value=value;
      legends.push[name];
      topic.push(cons);
    }
var myChart2 = echarts.init(document.getElementById(radar_div));
var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient : 'vertical',
        x : 'left',
        data:legends
    },
    toolbox: {
        //show : true,
        feature : {
           // mark : {show: true},
            //dataView : {show: true, readOnly: false},
            magicType : {
                //show: true, 
                type: ['pie', 'funnel'],
                option: {
                    funnel: {
                        x: '5%',
                        width: '40%',
                        funnelAlign: 'left',
                        max: 1548
                    }
                }
            },
            //restore : {show: true},
            //saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'访问来源',
            type:'pie',
            radius : '40%',
            center: ['45%', '60%'],
            data:topic
        }
    ]
};
                    
  //   var topic_val = [];
  //   topic_val.push(topic_name_sta);
  //   topic_val.push(topic_sta);
  //   var topic_result = [];
  //   topic_result = get_radar_data(topic_val);
  // var topic_name = topic_result[0];
  // var topic_value = topic_result[1];
  // console.log(topic_result);
  // var myChart2 = echarts.init(document.getElementById(radar_div));
  // var option = {
  //   // title : {
  //   //   text: '用户话题分布',
  //   //   subtext: ''
  //   // },
  //     tooltip : {
  //       show: true,
  //       trigger: 'axis',
  //       formatter:  function (params){
  //         var res  = '';
  //         var indicator = params.indicator;
  //         //console.log(params);
  //         res += params['0'][3]+' : '+(params['0'][2]/10).toFixed(2);
  //         return res;
  //         }
  //       },
  //     toolbox: {
  //       show : true,
  //       feature : {
  //           mark : {show: true},
  //           dataView : {show: true, readOnly: false},
  //           restore : {show: true},
  //           saveAsImage : {show: true}
  //       }
  //     },
  //     calculable : true,
  //     polar : [
  //      {
  //       indicator :topic_name,
  //       radius : 90
  //      }
  //     ],
  //     series : [
  //      {
  //       name: '话题分布情况',
  //       type: 'radar',
  //       itemStyle: {
  //        normal: {
  //         areaStyle: {
  //           type: 'default'
  //         }
  //        }
  //       },
  //      data : [
  //       {
  //        value : topic_value,
  //        //name : '用户话题分布'
  //       }
  //      ]
  //     }]
  // };
  myChart2.setOption(option);
}
}

function get_radar_data (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];
  for(var i=0; i<topic[0].length;i++){
    topic_value.push(topic[1][i].toFixed(2)*10)
    topic_name.push(topic[0][i]);
  };
  // var topic_value2 = [];
  // var topic_name2 = [];
  // for(var i=0; i<8;i++){ //取前8个最大值
  //   a=topic_value.indexOf(Math.max.apply(Math, topic_value));
  //   topic_value2.push(topic_value[a].toFixed(3));
  //   topic_name2.push(topic_name[a]);
  //   topic_value[a]=0;
  // }
  var topic_name3 = [];
  var max_topic = 8;
  if(topic_value.length<8){
    max_topic = topic_value.length;
  }
  for(var i=0;i<max_topic;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3)+1;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}

//var basic_name=document.getElementById('').text();
//var basic_name=$("#stickynote").text();
var g_basic = new g_basic();
var basic_url='/group/show_group_result/?task_name='+name + '&submit_user=' + submit_user + '&module=basic';
g_basic.call_sync_ajax_request(basic_url,g_basic.ajax_method,draw_basic);

