var name = 'testtask';
var global_data = {};
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

function ajax_method(){
    this.ajax_method = 'GET';
}
//ajax get data 
ajax_method.prototype = {
    call_sync_ajax_request:function(url, method, callback){
        $.ajax({
            url: url,
            method: method,
            dataType: 'json',
            success: callback
        });
    },
}

function basic_influence(div,data){
    $(div).empty();
    var domain_html = '';
    domain_html += '<p style="margin-top:30px;margin-left:10px;">群体名称：';
    domain_html += '<span id="groupName">' + data['task_name'] + '</span>';
    domain_html += '；提交时间：<span id="endTime">' + data['submit_date'] + '</span>';
    domain_html += '；备注：<span id="remarks">' + data['state'] + '</span>';
    domain_html += '<span type="button"data-toggle="modal" data-target="#user_list" style="font-size:16px;cursor: pointer"><u>用户列表1</u></span></p>';
    $(div).append(domain_html);
}

function draw_linechart(id,data,type){
    // $('#'+id).empty();
    // $('#'+id).empty();
    var myChart = echarts.init(document.getElementById(id)); 
    var option = {
    title : {
        text : '时间坐标折线图',
        subtext : 'dataZoom支持'
    },
    tooltip : {
        trigger: 'item',
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
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
                console.log(data);
                console.log(data['type']);
                console.log(data['xAxis'].getTime());
                if(type == 'active'){
                    var count_weibo_url = '/group/get_count_weibo/?task_name='+name+ '&sensitive_status='+data['type']+'&timestamp='+data['xAxis'].getTime()/1000;
                    console.log(count_weibo_url);
                    group_results.call_sync_ajax_request(count_weibo_url, group_results.ajax_method, draw_count_weibo);
                }
            }

            myChart.on(ecConfig.EVENT.CLICK,focus)
            myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {});
        }
    )                   
}

function draw_count_weibo(data){
    console.log(data);
}

function draw_barchart(id,data){
    console.log("fsdfsd");
    var myChart = echarts.init(document.getElementById(id)); 
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
    console.log("fsdfsd")
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
    }
    for(var i = 0; i < data2.length; i++){
        temp_data_1.push([new Date(data2[i][0]*1000),data2[i][1]]);
    }

    for(var i = 0; i < data3.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':data1[data3[i]][1], 'xAxis':new Date(data1[data3[i]][0]*1000),'yAxis':data1[data3[i]][1],'type':0});
    }
    for(var i = 0; i < data4.length; i++){
        point_data_1.push({'name':'拐点'+i, 'value':data2[data4[i]][1], 'xAxis':new Date(data2[data4[i]][0]*1000),'yAxis':data2[data4[i]][1],'type':1});
    }
    console.log(point_data_0);
    console.log(point_data_1);
    var series_0 = {'name':'不敏感', 'type':'line', 'smooth':true, 'data':temp_data_0,'markPoint':{'data':point_data_0}};
    var series_1 = {'name':'敏感', 'type':'line', 'smooth':true,'data': temp_data_1,'markPoint':{'data':point_data_1}};
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
    }
    for(var i = 0; i < data2.length; i++){
        temp_data_1.push([new Date(data2[i][0]*1000),data2[i][1]]);
    }
    for(var i = 0; i < data3.length; i++){
        temp_data_2.push([new Date(data3[i][0]*1000),data3[i][1]]);
    }
    for(var i = 0; i < data4.length; i++){
        temp_data_3.push([new Date(data4[i][0]*1000),data4[i][1]]);
    }
    for(var i = 0; i < data5.length; i++){
        temp_data_4.push([new Date(data5[i][0]*1000),data5[i][1]]);
    }

    for(var i = 0; i < data6.length; i++){
        point_data_0.push({'name':'拐点'+i, 'value':data1[data6[i]][1], 'xAxis':new Date(data1[data6[i]][0]*1000),'yAxis':data1[data6[i]][1]});
    }
    for(var i = 0; i < data7.length; i++){
        point_data_1.push({'name':'拐点'+i, 'value':data2[data7[i]][1], 'xAxis':new Date(data2[data7[i]][0]*1000),'yAxis':data2[data7[i]][1]});
    }
    for(var i = 0; i < data8.length; i++){
        point_data_2.push({'name':'拐点'+i, 'value':data3[data8[i]][1], 'xAxis':new Date(data3[data8[i]][0]*1000),'yAxis':data3[data8[i]][1]});
    }
    for(var i = 0; i < data9.length; i++){
        point_data_3.push({'name':'拐点'+i, 'value':data4[data9[i]][1], 'xAxis':new Date(data4[data9[i]][0]*1000),'yAxis':data4[data9[i]][1]});
    }
    for(var i = 0; i < data10.length; i++){
        point_data_4.push({'name':'拐点'+i, 'value':data5[data10[i]][1], 'xAxis':new Date(data5[data10[i]][0]*1000),'yAxis':data5[data10[i]][1]});
    }

    console.log(point_data_0);
    console.log(point_data_1);
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
    }
    console.log(xAxis_data);
    console.log(y_data);
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
                        data : xAxis_data[0]
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
  return [time_data, options];
}

var test_url = '/group/track_task_results/?task_name='+name;
var comment_url = '/group/track_task_results/?task_name='+name+'&module=comment_retweet';
function get_group_data(data){
    console.log(data);
    global_data = data;
    console.log('aaaa');
    console.log(global_data);
    var basic_data = data['basic'];
    var count_0_data = data['count_0'];
    var count_1_data = data['count_1'];
    var count_0_peak = data['count_0_peak'];
    var count_1_peak = data['count_1_peak'];
    var sensitive_data = data['sensitive_score'];
    var sensitive_peak = data['sensitive_score_peak'];
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

    var geo_0 = data['geo_0'];
    var geo_1 = data['geo_1'];
    var hashtag_0 = data['hashtag_0'];
    var hashtag_1 = data['hashtag_1'];

    var count_data = analysis_count(count_0_data, count_1_data,count_0_peak,count_1_peak);
    var sensitive = analysis_sensitive(sensitive_data, sensitive_peak);
    var sentiment = analysis_sentiment(sentiment_1_126,sentiment_1_127,sentiment_1_128,sentiment_1_129,sentiment_1_130,sentiment_1_126_peak, sentiment_1_127_peak, sentiment_1_128_peak,sentiment_1_129_peak,sentiment_1_130_peak);
    var option_data = analysis_geo(geo_0);
    var hashtag_data = analysis_geo(hashtag_0);
    console.log('sssssss');
    console.log(hashtag_data);
    basic_influence('#basic',basic_data);
    draw_linechart('active',count_data,'active');
    draw_linechart('sensitivity',sensitive,'sensitivity');
    draw_linechart('emotion',sentiment,'sentiment');
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
    bind_radio_input();
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
        console.log($(this).attr('value') );
        if($(this).attr('value') == 0){
            sentiment = analysis_sentiment(sentiment_0_126,sentiment_0_127,sentiment_0_128,sentiment_0_129,sentiment_0_130,sentiment_0_126_peak, sentiment_0_127_peak, sentiment_0_128_peak,sentiment_0_129_peak,sentiment_0_130_peak);
        }
        else{
            sentiment = analysis_sentiment(sentiment_1_126,sentiment_1_127,sentiment_1_128,sentiment_1_129,sentiment_1_130,sentiment_1_126_peak, sentiment_1_127_peak, sentiment_1_128_peak,sentiment_1_129_peak,sentiment_1_130_peak);
        }
        draw_linechart('emotion',sentiment,'sentiment');
    });

    $('input[name="location_0"]').click(function(){
        console.log($(this).attr('value') );
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
        console.log($(this).attr('value') );
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

var group_results = new ajax_method();

group_results.call_sync_ajax_request(test_url, group_results.ajax_method, get_group_data);
group_results.call_sync_ajax_request(comment_url, group_results.ajax_method, draw_count_weibo);




// draw_linechart('emotion');
// draw_linechart('sensitivity');
// draw_linechart('user');
// draw_barchart('location');
// draw_barchart('hashtag');
draw_stackbar('test');

