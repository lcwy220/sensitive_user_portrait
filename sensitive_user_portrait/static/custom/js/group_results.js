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
        method: 'get',
        dataType: 'json',
        success: callback
    });
}

function basic_influence(div,data){
    $(div).empty();
    var domain_html = '';
    domain_html += '<p style="margin-top:30px;margin-left:10px;">群体名称：';
    domain_html += '<span id="groupName" style="margin-right:10px;">' + data['task_name'] + '</span>';
    domain_html += '群组人数：<span id="members_count" style="margin-right:10px;">' + data['count'] + '</span>';
    domain_html += '提交时间：<span id="endTime" style="margin-right:10px;">' + data['submit_date'] + '</span>';
    if (data['status'] == 1){
        domain_html += '监控状态：<span id="status" style="margin-right:10px;">监控停止</span>';
    }
    else {
        domain_html += '监控状态：<span id="stauts" style="margin-right:10px;">正在监控</span>';
    }
    domain_html += '备注：<span id="remarks">' + data['state'] + '</span>';
    domain_html += '<span type="button"data-toggle="modal" data-target="#user_list" style="font-size:16px;cursor: pointer; float:right"><u>查看用户列表</u></span></p>';
    $(div).append(domain_html);

    var user_list = data['uid_list'];
    draw_table(user_list);
}

function draw_linechart(id,data,type,flag){
    // $('#'+id).empty();
    // $('#'+id).empty();
    var myChart = echarts.init(document.getElementById(id)); 
    var option = {
    title : {
        text : '',
        subtext : ''
    },
    tooltip : {
        trigger: 'item',
    },

    // toolbox: {
    //     show : true,
    //     feature : {
    //         mark : {show: true},
    //         dataView : {show: true, readOnly: false},
    //         restore : {show: true},
    //         saveAsImage : {show: true}
    //     }
    // },
    dataZoom: {
        show: true,
        start : 70
    },
    legend : {
        data : data[0]
    },
    grid: {
        y2: 80
    },
    xAxis : [
        {
            type : 'time',
            splitNumber:10
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series :data[1]
    };
    myChart.setOption(option);
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param){
                var data = param.data;
                if(type == 'active'){
                    var count_weibo_url = '/group/get_count_weibo/?task_name='+name+ '&sensitive_status='+data['type']+'&timestamp='+data['xAxis'].getTime()/1000;
                    call_ajax_request(count_weibo_url, draw_count_weibo);
                }
                if(type=='sentiment'){
                    var sentiment_weibo_url = '/group/get_sentiment_weibo/?task_name='+name+ '&sensitive_status='+flag+'&sentiment='+data['type']+'&timestamp='+data['xAxis'].getTime()/1000;
                    console.log(sentiment_weibo_url);
                    call_ajax_request(sentiment_weibo_url, draw_sentiment_weibo);
                }
                if(type=='sensitivity'){
                    var sentiment_weibo_url = '/group/get_sensitive_word/?task_name='+name+ '&timestamp='+data['xAxis'].getTime()/1000;
                    call_ajax_request(sentiment_weibo_url, draw_sentivity_word);
                }
            }
            myChart.on(ecConfig.EVENT.CLICK,focus)
            myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {});
        }
    )                   
}

function draw_count_weibo(data){
    $('#weibo_count').empty();
    var html = '';  
    html += '<div class="group_weibo_font">';  
    if (data.length == 0){
        $('#weibo_count').html('暂无微博数据');
        return;
    }else{
        for(var i = 0; i < data.length; i++){
            var uid = data[i][0];
            var uname = data[i][1];
            var date = data[i][2];
            var location = data[i][3];
            var message = data[i][4];
            html += '<div style="padding:10px;font-size:13px;background: whitesmoke;margin-bottom: 10px">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;发布:&nbsp;'+ message + '</p>';
            html += '<p style="color:darkred;height:10px;"><span style="float:right">' + date + '&nbsp;&nbsp;' + location + '&nbsp;&nbsp;'+ '</span></p>';
            html += '</div>'
        }
    }
    html += '</div>';
    $('#weibo_count').append(html);
}

function draw_sentiment_weibo(data){
    $('#weibo_sentiment').empty();
    var html = '';  
    html += '<div class="group_weibo_font">';  
    if (data.length == 0){
        $('#weibo_sentiment').html('暂无微博数据');
        return;
    }else{
        for(var i = 0; i < data.length; i++){
            var uid = data[i][0];
            var uname = data[i][1];
            var date = data[i][2];
            var location = data[i][3];
            var message = data[i][4];
            html += '<div style="padding:10px;font-size:13px;background: whitesmoke;margin-bottom: 10px">';
            html += '<p style="color:black;"><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;发布:&nbsp;'+ message + '</p>';
            html += '<p style="color:darkred; height:10px"><span style="float:right">' + date + '&nbsp;&nbsp;' + location + '&nbsp;&nbsp;'+ '</span></p>';
            html += '</div>'
        }
    }
    html += '</div>';
    $('#weibo_sentiment').append(html);
}

function draw_sentivity_word(data){
    $('#weibo_sentivity').empty();
    var html = '';
    html += '<table id="delete_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>序号</th><th>关键词</th></tr></thead>';
    html += '<tbody>';
    for(var i=0; i<data.length; i++){
      html += '<tr id=' + data[i][0] +'>';
      html += '<td class="center" >'+ i +'</td>';
      html += '<td class="center">'+ data[i][0] + '</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#weibo_sentivity').append(html);
}

function draw_table(data){
    $('#more_influence').empty();
    var html = '';
    html += '<table id="delete_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th></tr></thead>';
    html += '<tbody>';
    for(var i in data){
      html += '<tr id=' + data[i][0] +'>';
      html += '<td class="center" >'+ data[i][0] +'</td>';
      html += '<td class="center">'+ data[i][1] + '</td>';
      html += '<td class="center">'+ data[i][2] + '</td>';
      html += '<td class="center" style="width:100px;">'+ data[i][3] + '</td>';
      html += '<td class="center" style="width:100px;">'+ data[i][4] + '</td>';
      html += '<td class="center" style="width:100px;">'+ data[i][5] + '</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#more_influence').append(html);
}

function draw_barchart(id,data,type){
    var myChart = echarts.init(document.getElementById(id)); 
    console.log(data[1]);
    var option = {
        timeline:{
            data:data[0],
            label : {
                formatter : function(s) {
                    return s.slice(0, 12);
                }
            },
            autoPlay : true,
            playInterval : 1000
        },
        options:data[1],
        // options:[
        //     {
        //         title : {
        //             text: '',
        //         },
        //         tooltip : {
        //             trigger: 'axis'
        //         },
        //         legend: {
        //             data:['敏感','不敏感']
        //         },
        //         toolbox: {
        //             show : true,
        //             feature : {
        //                 mark : {show: true},
        //                 dataView : {show: true, readOnly: false},
        //                 magicType: {show: true, type: ['line', 'bar']},
        //                 restore : {show: true},
        //                 saveAsImage : {show: true}
        //             }
        //         },
        //         calculable : true,
        //         xAxis : [
        //             {
        //                 type : 'value',
        //                 boundaryGap : [0, 0.01]
        //             }
        //         ],
        //         yAxis : [
        //             {
        //                 type : 'category',
        //                 data : ['巴西','印尼','美国','印度','中国','世界人口(万)']
        //             }
        //         ],
        //         series : [
        //             {
        //                 name:'敏感',
        //                 type:'bar',
        //                 data:[18203, 23489, 29034, 104970, 131744, 630230]
        //             },
        //             {
        //                 name:'不敏感',
        //                 type:'bar',
        //                 data:[18203, 23489, 29034, 104970, 131744, 630230]
        //             },
        //         ]},
        //         {
        //         title : {'text':'2003全国宏观经济指标'},
        //         series : [
        //             {'data': [18203, 239, 29034, 104970, 131744, 630230]},
        //             {'data': [18203, 239, 29034, 104970, 131744, 630230]},
       
        //         ]
        //     },


        // ]
    };                    
                                                 
    myChart.setOption(option);                
}

function draw_stackbar(id){
    var myChart = echarts.init(document.getElementById(id)); 
    var option = {
        timeline:{
            data:[
               '2002-01-01','2003-01-01',
            ],
            label : {
                formatter : function(s) {
                    return s.slice(0, 4);
                }
            },
            autoPlay : true,
            playInterval : 1000
        },
        options:[
            {
                title : {
                    text: '世界人口总量',
                },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['微博数']
                },
                toolbox: {
                    show : true,
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
                        data : ['巴西','印尼','美国','印度','中国','世界人口(万)']
                    }
                ],
                series : [
                    {
                        name:'微博数',
                        type:'bar',
                        data:[18203, 23489, 29034, 104970, 131744, 630230]
                    },
                ]},
                {
                title : {'text':'2003全国宏观经济指标'},
                series : [
                    {'data': [18203, 239, 29034, 104970, 131744, 630230]},
       
                ]
            },


        ]
    };
                                       
    myChart.setOption(option);                
}

function analysis_count(data1,data2,data3,data4){
    var legend_data = ['敏感', '不敏感'];
    var temp_data_0 = [];
    var temp_data_1 = [];
    var point_data_0 = [];
    var point_data_1 = [];
    for(var i = 0; i < data1.length; i++){
        temp_data_0.push([new Date(data1[i][0]*1000),data1[i][1]]);
        temp_data_1.push([new Date(data2[i][0]*1000),data2[i][1]]);
    }

    for(var i = 0; i < data3.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':data1[data3[i]][1], 'xAxis':new Date(data1[data3[i]][0]*1000),'yAxis':data1[data3[i]][1],'type':0});
    }
    for(var i = 0; i < data4.length; i++){
        point_data_1.push({'name':'拐点'+i, 'value':data2[data4[i]][1], 'xAxis':new Date(data2[data4[i]][0]*1000),'yAxis':data2[data4[i]][1],'type':1});
    }
    var series_0 = {'name':'不敏感', 'type':'line', 'smooth':true, 'data':temp_data_0,'markPoint':{'data':point_data_0}};
    var series_1 = {'name':'敏感', 'type':'line', 'smooth':true,'data': temp_data_1,'markPoint':{'data':point_data_1}};
    var data = [legend_data, [series_0, series_1]];
    return data;
}

function analysis_img(data1,data2,data3,data4){
    var legend_data = ['原创', '转发'];
    var temp_data_0 = [];
    var temp_data_1 = [];
    var point_data_0 = [];
    var point_data_1 = [];
    for(var k in data1){
        temp_data_0.push([new Date(k*1000),data1[k]]);
    }
    for(var m in data2){
        temp_data_1.push([new Date(m*1000),data2[m]]);
    }
    console.log(temp_data_0);
    for(var i = 0; i < data3.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':temp_data_0[data3[i]][1], 'xAxis':temp_data_0[data3[i]][0],'yAxis':temp_data_0[data3[i]][1],'type':0});
    }
    for(var i = 0; i < data4.length; i++){
        point_data_1.push({'name':'拐点'+i, 'value':temp_data_1[data4[i]][1], 'xAxis':temp_data_1[data4[i]][0],'yAxis':temp_data_1[data4[i]][1],'type':1});
    }
    var series_0 = {'name':'原创', 'type':'line', 'smooth':true, 'data':temp_data_0,'markPoint':{'data':point_data_0}};
    var series_1 = {'name':'转发', 'type':'line', 'smooth':true,'data': temp_data_1,'markPoint':{'data':point_data_1}};
    var data = [legend_data, [series_0, series_1]];
    return data;
}

function analysis_sensitive(data1,data2){
    var legend_data = ['敏感度变动'];
    var temp_data_0 = [];
    var point_data_0 = [];
    for(var i = 0; i < data1.length; i++){
        temp_data_0.push([new Date(data1[i][0]*1000),data1[i][1]]);
    }
    for(var i = 0; i < data2.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':data1[data2[i]][1], 'xAxis':new Date(data1[data2[i]][0]*1000),'yAxis':data1[data2[i]][1]});
    }
    var series_0 = {'name':'敏感度变动', 'type':'line', 'smooth':true, 'data':temp_data_0,'markPoint':{'data':point_data_0}};
    var data = [legend_data, [series_0]];
    return data;
}

function analysis_sentiment(data1,data2,data3,data4,data5,data6,data7,data8,data9,data10){
    var legend_data = ['积极', '消极','生气','焦虑','其他'];
    var temp_data_0 = [];
    var temp_data_1 = [];
    var temp_data_2 = [];
    var temp_data_3 = [];
    var temp_data_4 = [];
    var point_data_0 = [];
    var point_data_1 = [];
    var point_data_2 = [];
    var point_data_3 = [];
    var point_data_4 = [];

    for(var i = 0; i < data1.length; i++){
        temp_data_0.push([new Date(data1[i][0]*1000),data1[i][1]]);
        temp_data_1.push([new Date(data2[i][0]*1000),data2[i][1]]);
        temp_data_2.push([new Date(data3[i][0]*1000),data3[i][1]]);
        temp_data_3.push([new Date(data4[i][0]*1000),data4[i][1]]);
        temp_data_4.push([new Date(data5[i][0]*1000),data5[i][1]]);
    }
    for(var i = 0; i < data6.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':data1[data6[i]][1], 'xAxis':new Date(data1[data6[i]][0]*1000),'yAxis':data1[data6[i]][1],'type':126});
    }
    for(var i = 0; i < data7.length; i++){
        point_data_1.push({'name':'拐点'+i, 'value':data2[data7[i]][1], 'xAxis':new Date(data2[data7[i]][0]*1000),'yAxis':data2[data7[i]][1],'type':127});
    }
    for(var i = 0; i < data8.length; i++){
        point_data_2.push({'name':'拐点'+i, 'value':data3[data8[i]][1], 'xAxis':new Date(data3[data8[i]][0]*1000),'yAxis':data3[data8[i]][1],'type':128});
    }
    for(var i = 0; i < data9.length; i++){
        point_data_3.push({'name':'拐点'+i, 'value':data4[data9[i]][1], 'xAxis':new Date(data4[data9[i]][0]*1000),'yAxis':data4[data9[i]][1],'type':129});
    }
    for(var i = 0; i < data10.length; i++){
        point_data_4.push({'name':'拐点'+i, 'value':data5[data10[i]][1], 'xAxis':new Date(data5[data10[i]][0]*1000),'yAxis':data5[data10[i]][1],'type':130});
    }

    var series_0 = {'name':'积极', 'type':'line', 'smooth':true, 'data':temp_data_0,'markPoint':{'data':point_data_0}};
    var series_1 = {'name':'消极', 'type':'line', 'smooth':true,'data': temp_data_1,'markPoint':{'data':point_data_1}};
    var series_2 = {'name':'生气', 'type':'line', 'smooth':true, 'data':temp_data_2,'markPoint':{'data':point_data_2}};
    var series_3 = {'name':'焦虑', 'type':'line', 'smooth':true, 'data':temp_data_3,'markPoint':{'data':point_data_3}};
    var series_4 = {'name':'其他', 'type':'line', 'smooth':true, 'data':temp_data_4,'markPoint':{'data':point_data_4}};
    var data = [legend_data, [series_0, series_1, series_2, series_3, series_4]];
    return data;
}

function analysis_geo(data){
    var legend_data = ['不敏感'];
    var time_data = [];
    var xAxis_data = [];
    var y_data = []; 
    var length_data = []; 
    for(var k in data){
        time_data.push(k);
        var tempx_data = [];
        var tempy_data = [];
        for(loc in data[k]){
            tempx_data.push(loc);
            tempy_data.push(data[k][loc]);
        }
        xAxis_data.push(tempx_data);
        y_data.push(tempy_data);
        length_data.push(tempy_data.length);
    }
    var max_length = Math.max.apply(Math, length_data);
    console.log(max_length);
    for(var i = 0; i < y_data.length; i++){
        if(y_data[i].length < max_length){
            for(var j = y_data[i].length; j < max_length; j++){
                y_data[i].push(0);
                xAxis_data[i].push('');
            }
        }
    }

    if(xAxis_data.length == 0){
        return 0;
    }
    else {
        var options = [
            {
                title : {
                    text: '',
                },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:legend_data,
                },
                grid:{
                    x:100,
                },
                // toolbox: {
                //     show : true,
                //     feature : {
                //         mark : {show: true},
                //         dataView : {show: true, readOnly: false},
                //         magicType: {show: true, type: ['line', 'bar']},
                //         restore : {show: true},
                //         saveAsImage : {show: true}
                //     }
                // },
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
                        data : xAxis_data[0],
                    }
                ],
                series : [
                    {
                        name:'不敏感',
                        type:'bar',
                        data:y_data[0]
                    },
                ]
            },
        ];
        if(xAxis_data.length > 1){
                            
            for(var j = 1 ; j < xAxis_data.length; j++){
                var other_data = {        
                    yAxis: [
                            {
                                type : 'category',
                                data : xAxis_data[j]
                            }
                        ],
                    series: [
                        {'data': y_data[j]}  
                    ]
                };
                options.push(other_data);
            }
        }

    }
    console.log(options);
  return [time_data, options];
}

function test_data(data){
    user_name_data = data;
    add_head();
    draw_domain_portrait(data['profile']);
}

function draw_domain_portrait(data){
    user_data = data;
  $('#img').empty();
    num = 0 
    var html = '';
    html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
    html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding"></a></small></h1>';
    html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
    html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
  
    for (key in data){ 
       num ++;
       if (num < 7){
               if (data[key][1] == ''){
                  domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
               }else{
                  domain_top_user_portrait = data[key][1];
                };
              html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="img"  id='+key+'>';
              html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + data[key][0] +'"></div></li>';         
        }
      

    }
      html += '</ul></div></div>';
    $('#img').append(html);
    bind_portait();
}

function bind_portait(){
    $('.img').click(function(){
        console.log(user_name_data);
        var id = $(this).attr('id');
        var comment_index = id + '_comment';
        var retweet_index = id+ '_retweet';
        var comment_peak = id + '_comment_peak';
        var retweet_peak = id + '_retweet_peak';
        var comment_data = user_name_data[comment_index] ;
        var retweet_data = user_name_data[retweet_index];
        var comment_peak_data = user_name_data[comment_peak];
        var retweet_peak_data = user_name_data[retweet_peak];
        var img_data = analysis_img(comment_data,retweet_data,comment_peak_data,retweet_peak_data);
        draw_linechart('user',img_data,'user',0);
    });
}

function add_head(){
    console.log('aaaaaaa');
    $('#count_head').append('<h4 style="display:inline-block">(异常值为:'+global_data['count_abnormal']+')</h4>');
    $('#emtion_head').append('<h4 style="display:inline-block">(异常值为:'+global_data['sentiment_abnormal']+')</h4>');
    $('#location_head').append('<h4 style="display:inline-block">(异常值为:'+global_data['geo_abnormal']+')</h4>');
    $('#hashtag_head').append('<h4 style="display:inline-block">(异常值为:'+global_data['hashtag_abnormal']+')</h4>');
    $('#senstivity_head').append('<h4 style="display:inline-block">(异常值为:'+global_data['sensitive_abnormal']+')</h4>');
    $('#user_head').append('<h4 style="display:inline-block">(异常值为:'+user_name_data['abnormal_index'].toFixed(2)+')</h4>');
}

function get_group_data(data){
    console.log(data);
    global_data = data;
    basic_influence('#basic',data.basic);

    var count_0_data = data['count_0'];
    var count_1_data = data['count_1'];
    var count_0_peak = data['count_0_peak'];
    var count_1_peak = data['count_1_peak'];
    var count_data = analysis_count(count_0_data, count_1_data,count_0_peak,count_1_peak);
    draw_linechart('active',count_data,'active',0);

    /*
    var sentiment_0_126 = data['sentiment_0_126'];
    var sentiment_0_127 = data['sentiment_0_127'];
    var sentiment_0_128 = data['sentiment_0_128'];
    var sentiment_0_129 = data['sentiment_0_129'];
    var sentiment_0_130 = data['sentiment_0_130'];

    var sentiment_0_126_peak = data['sentiment_0_126_peak'];
    var sentiment_0_127_peak = data['sentiment_0_127_peak'];
    var sentiment_0_128_peak = data['sentiment_0_128_peak'];
    var sentiment_0_129_peak = data['sentiment_0_129_peak'];
    var sentiment_0_130_peak = data['sentiment_0_130_peak'];
    */
    bind_radio_input();
    var sentiment_1_126 = data['sentiment_1_126'];
    var sentiment_1_127 = data['sentiment_1_127'];
    var sentiment_1_128 = data['sentiment_1_128'];
    var sentiment_1_129 = data['sentiment_1_129'];
    var sentiment_1_130 = data['sentiment_1_130'];

    var sentiment_1_126_peak = data['sentiment_1_126_peak'];
    var sentiment_1_127_peak = data['sentiment_1_127_peak'];
    var sentiment_1_128_peak = data['sentiment_1_128_peak'];
    var sentiment_1_129_peak = data['sentiment_1_129_peak'];
    var sentiment_1_130_peak = data['sentiment_1_130_peak'];
    var sentiment = analysis_sentiment(sentiment_1_126,sentiment_1_127,sentiment_1_128,sentiment_1_129,sentiment_1_130,sentiment_1_126_peak, sentiment_1_127_peak, sentiment_1_128_peak,sentiment_1_129_peak,sentiment_1_130_peak);
    draw_linechart('emotion',sentiment,'sentiment', 1);
    
    var sensitive_data = data['sensitive_score'];
    var sensitive_peak = data['sensitive_score_peak'];

    var geo_0 = data['geo_0'];
    var geo_1 = data['geo_1'];
    var hashtag_0 = data['hashtag_0'];
    var hashtag_1 = data['hashtag_1'];
    /*
    var sensitive = analysis_sensitive(sensitive_data, sensitive_peak);
    var option_data = analysis_geo(geo_1);
    var hashtag_data = analysis_geo(hashtag_1);
    draw_linechart('sensitivity',sensitive,'sensitivity',0);
    if(option_data == 0){
        $('#location').append('<h3>当前数值为空<h3>');
    }else{
        draw_barchart('location', option_data,'location');
    }
    if(hashtag_data == 0){
        $('#hashtag').append('<h3>当前数值为空<h3>')
    }else{
        draw_barchart('hashtag', hashtag_data,'hashtag');
    }    
    */
}

function bind_radio_input(){
    var sentiment_0_126 = global_data['sentiment_0_126'];
    var sentiment_0_127 = global_data['sentiment_0_127'];
    var sentiment_0_128 = global_data['sentiment_0_128'];
    var sentiment_0_129 = global_data['sentiment_0_129'];
    var sentiment_0_130 = global_data['sentiment_0_130'];

    var sentiment_0_126_peak = global_data['sentiment_0_126_peak'];
    var sentiment_0_127_peak = global_data['sentiment_0_127_peak'];
    var sentiment_0_128_peak = global_data['sentiment_0_128_peak'];
    var sentiment_0_129_peak = global_data['sentiment_0_129_peak'];
    var sentiment_0_130_peak = global_data['sentiment_0_130_peak'];

    var sentiment_1_126 = global_data['sentiment_1_126'];
    var sentiment_1_127 = global_data['sentiment_1_127'];
    var sentiment_1_128 = global_data['sentiment_1_128'];
    var sentiment_1_129 = global_data['sentiment_1_129'];
    var sentiment_1_130 = global_data['sentiment_1_130'];

    var sentiment_1_126_peak = global_data['sentiment_1_126_peak'];
    var sentiment_1_127_peak = global_data['sentiment_1_127_peak'];
    var sentiment_1_128_peak = global_data['sentiment_1_128_peak'];
    var sentiment_1_129_peak = global_data['sentiment_1_129_peak'];
    var sentiment_1_130_peak = global_data['sentiment_1_130_peak'];
    var sentiment;
    var option_data;
    var geo_0 = global_data['geo_0'];
    var geo_1 = global_data['geo_1'];
    var hashtag_data ;
    var hashtag_0 = global_data['hashtag_0'];
    var hashtag_1 = global_data['hashtag_1'];
    $('input[name="count"]').click(function(){
        if($(this).attr('value') == 0){
            sentiment = analysis_sentiment(sentiment_0_126,sentiment_0_127,sentiment_0_128,sentiment_0_129,sentiment_0_130,sentiment_0_126_peak, sentiment_0_127_peak, sentiment_0_128_peak,sentiment_0_129_peak,sentiment_0_130_peak);
            draw_linechart('emotion',sentiment,'sentiment',0);
        }
        else{
            sentiment = analysis_sentiment(sentiment_1_126,sentiment_1_127,sentiment_1_128,sentiment_1_129,sentiment_1_130,sentiment_1_126_peak, sentiment_1_127_peak, sentiment_1_128_peak,sentiment_1_129_peak,sentiment_1_130_peak);
            draw_linechart('emotion',sentiment,'sentiment',1);
        }
    });

    $('input[name="location_0"]').click(function(){
        if($(this).attr('value') == 0){
            option_data = analysis_geo(geo_0);
        }
        else{
            option_data = analysis_geo(geo_1);
        }
        if(option_data == 0){
            $('#location').append('<h3>当前数值为空<h3>');
        }else{
            draw_barchart('location', option_data,'location');
        }
    });

    $('input[name="hashtag"]').click(function(){
        if($(this).attr('value') == 0){
            hashtag_data = analysis_geo(hashtag_0);
        }
        else{
            hashtag_data = analysis_geo(hashtag_1);
        }
        if(hashtag_data == 0){
            $('#hashtag').html('<h3>当前数值为空<h3>');
        }else{
            draw_barchart('hashtag', hashtag_data,'hashtag');
        }
    });
}

var name = 'testtask2';
var global_data = {};
var user_data ;
var user_name_data ;
var test_url = '/group/track_task_results/?task_name='+name;
var comment_url = '/group/track_task_results/?task_name='+name+'&module=comment_retweet';

call_ajax_request(test_url, get_group_data);
//call_ajax_request(comment_url, test_data);

// draw_linechart('emotion');
// draw_linechart('sensitivity');
// draw_linechart('user');
// draw_barchart('location');
// draw_barchart('hashtag');
// draw_stackbar('test');

