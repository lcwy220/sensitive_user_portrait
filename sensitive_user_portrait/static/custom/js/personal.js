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
function date_format(date){
    var str = (parseInt(date.getMonth()) + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':00';
    return str;
}
function drawTimeTrend(trend_data){
    var weiboChart = echarts.init(document.getElementById('weiboTime')); 
    var time_series = new Array();
    var value_series = new Array();
	for (var i = 0; i < trend_data.length; i++){
       var item = trend_data[i];
       var date = new Date(item[0] * 1000);
       time_series.push(date_format(date));
       value_series.push(item[1]);
    }
    var Weibooption = {
        title : {
            text: '微博变动',
        },
        color: ['#87cefa'],
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['微博量'],
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : time_series
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
                data:value_series,
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
    weiboChart.setOption(Weibooption); 
}
//影响力走势图
function drawInfluenceTrend(trend_data){
    var influenceChart = echarts.init(document.getElementById('influence_chart')); 
    var time_series = new Array();
    var value_series = new Array();
    for (var i = 0; i < trend_data.length;i++){
        var item = trend_data[i];
        var date = item[0];
        time_series.push(date.substring(0,4) + '-' + date.substring(4,6) + '-' + date.substring(6,8));
        value_series.push(Math.round(item[1]));
    }
    var Influenceoption = {
        title : {
            text: '影响力变动',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['影响力']
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : time_series
            }
        ],
        yAxis : [
            {
                type : 'value',
            }
        ],
        series : [
            {
                name:'影响力',
                type:'line',
                data:value_series,
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
    influenceChart.setOption(Influenceoption); 
}
//一周轨迹分布
function drawTrack(track_data){
    $('.course_nr2 li').find('.shiji').slideDown(600);
    
    for(i = 0;i < track_data.length;i++){
        var item = track_data[i];
        var date = item[0];
		var city = item[1];
		document.getElementById('d'+(i+1)).innerHTML = date.substring(4,6) + '-' + date.substring(6,9);
		if(city.length > 0){
            document.getElementById('city'+(i+1)).innerHTML = city.join(',');
		}else{
			$('#city'+(i+1)).addClass('gray');
			document.getElementById('city'+(i+1)).innerHTML = '未发布微博';
		}
		
	}
}
//画表格
function drawRank(div_name, rank_data, more_div){
    if (!rank_data){
        rank_data = new Array();
    }
     $('#'+ div_name).empty();
        var html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th>';
        html += '<th style="text-align:center">次数</th>';
        html += '<th style="text-align:center">是否入库</th></tr>';
        var min_row = Math.min(5, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           var item = rank_data[i];
           var nickname;
           if ((item[1][0] == 'unknown') || (item[1][0] == '0')){
               nickname = '未知';
           }
           else{
               nickname = item[1][0];
           }
           var in_status;
           if (item[1][2] == 0){
               in_status = '否';
           }
           else{
               in_status = '是';
           }
         html += '<tr><th style="text-align:center">' + m + '</th>';
         html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
         html += '<th style="text-align:center">' + item[1][1] + '</th>';
         html += '<th style="text-align:center">' + in_status + '</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);  

	//更多
	$('#' + more_div).empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th>';
    html += '<th style="text-align:center">昵称</th>';
    html += '<th style="text-align:center">次数</th>';
    html += '<th style="text-align:center">是否入库</th></tr>';
	for (var i = 0; i < rank_data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       var item = rank_data[i];
       var nickname;
       if ((item[1][0] == 'unknown') || (item[1][0] == '0')){
           nickname = '未知';
       }
       else{
           nickname = item[1][0];
       }
       var in_status;
       if (item[1][2] == 0){
           in_status = '否';
       }
       else{
           in_status = '是';
       }
       html += '<tr><th style="text-align:center">' + m + '</th>';
       html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
       html += '<th style="text-align:center">' + item[1][1] + '</th>';
       html += '<th style="text-align:center">' + in_status + '</th></tr>';
    };
    html += '</table>'; 
    $('#' + more_div).append(html);                  
}

//思想分析
function Draw_think_topic(){
    // domain_value = [];
    // domain_key = [];
    // indicate = [];
    // for ( key in data['2']){
    //      indicator = {};
    //     domain_key.push(key);
    //     indicator['text'] = key;
    //     indicator['max'] = 20;
    //     indicate.push(indicator);
    //     domain_value.push(data['2'][key]);
    // }
    var myChart = echarts.init(document.getElementById('radar_domain')); 
    var option = {
        title : {
            text: '倾向性',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['倾向性']
        },
        toolbox: {
            show : true,
        },
        calculable : true,
        polar : [
            {
            indicator : [
                {text : '九一八', max  : 100},
                {text : '博鳌论坛', max  : 100},
                {text : 'APEC', max  : 100},
                {text : '两会', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
                type: 'radar',
                itemStyle: {
                    normal: {
                        areaStyle: {
                            type: 'default'
                        }
                    }
                },
                data : [
                    {
                        value : [97, 42, 88, 94, 90, 86],
                        name : '倾向性'
                    }
                ]
            }
        ]
    };                
    myChart.setOption(option); 
}
function Draw_think_emotion(){
    var myChart = echarts.init(document.getElementById('pie_emotion')); 
    var option = {
        title : {
            text: '心理状态',
            subtext: ''
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: false},
                dataView : {show: false, readOnly: false},
                magicType : {
                    show: false, 
                    type: ['pie', 'funnel']
                },
                restore : {show: false},
            }
        },
        calculable : false,
        series : [
            {
                name:'',
                type:'pie',
                selectedMode: 'single',
                radius : [0, 35],
                
                // for funnel
                x: '20%',
                width: '40%',
                funnelAlign: 'right',
                max: 1548,
                
                itemStyle : {
                    normal : {
                        label : {
                            position : 'inner'
                        },
                        labelLine : {
                            show : false
                        }
                    }
                },
                data:[
                    {value:5, name:'积极'},
                    {value:5, name:'中性'},
                    {value:12, name:'消极', selected:true}
                ]
            },
            {
                name:'',
                type:'pie',
                radius : [50, 70],
            
                // for funnel
                x: '60%',
                width: '35%',
                funnelAlign: 'left',
                max: 1048,
                
                data:[
                    {value:5, name:'积极'},
                    {value:5, name:'中性'},
                    {value:3, name:'生气'},
                    {value:4, name:'悲伤'},
                    {value:5, name:'其他'}
                ]
            }
        ]
    }
    myChart.setOption(option);  
}
function drawBasic(personalData){
    var APsum = document.getElementById('APsum');
    APsum.innerHTML = personalData.all_count;
    var IPsum = document.getElementById('IPsum');
    IPsum.innerHTML = personalData.all_count;
    var FPsum = document.getElementById('FPsum');
    FPsum.innerHTML = personalData.all_count;
    var SPsum = document.getElementById('SPsum');
    SPsum.innerHTML = personalData.all_count;
    var value = 'activeness' in personalData?personalData['activeness'].toFixed(2):'无此数据';
    $('#APnum').html(value);
    var value = 'importance' in personalData?personalData['importance'].toFixed(2):'无此数据';
    $('#IPnum').html(value);
    var value = 'influence' in personalData?personalData['influence'].toFixed(2):'无此数据';
    $('#FPnum').html(value);
    var value = 'sensitive' in personalData?personalData['sensitive'].toFixed(2):'无此数据';
    $('#SPnum').html(value);
    var value = 'activeness_rank' in personalData?personalData['activeness_rank']:'无此数据';
    $('#APrank').html(value);
    var value = 'importance_rank' in personalData?personalData['importance_rank']:'无此数据';
    $('#IPrank').html(value);
    var value = 'influence_rank' in personalData?personalData['influence_rank']:'无此数据';
    $('#FPrank').html(value);
    var value = 'sensitive_rank' in personalData?personalData['sensitive_rank']:'无此数据';
    $('#SPrank').html(value);
    var value = 'uname' in personalData?personalData['uname']:'无此数据';
    $('#nickname').html(value);
    var value = 'description' in personalData?personalData['description']:'无此数据';
    $('#portraitDetail').html(value);
    var value = 'uid' in personalData?personalData['uid']:'无此数据';
    $('#userId').html(value);
    var value = 'location' in personalData?personalData['location']:'无此数据';
    $('#userLocation').html(value);
    var value = 'fansnum' in personalData?personalData['fansnum']:'无此数据';
    $('#userFans').html(value);
    var value = 'friendsnum' in personalData?personalData['friendsnum']:'无此数据';
    $('#userFriend').html(value);
    var value = 'online_pattern' in personalData?personalData['online_pattern'][0][0]:'无此数据';
    $('#userOnline').html(value);
    
    var img = document.getElementById('portraitImg');
    if(personalData.photo_url == "unknown"){
        img.src =  "http://tp2.sinaimg.cn/1878376757/50/0/1";
    }else{
        img.src = personalData.photo_url;
    }
    var gender = document.getElementById('userGender');
    if(personalData.gender){
        gendernum = personalData.gender;
        if (gendernum == 1){
            gender.innerHTML = '男';
        }else{
            gender.innerHTML = '女';
        }
    }else{
        gender.innerHTML = "无此数据";
    }
        
    var domain = document.getElementById('userDomain');
    if(personalData.domain){
        var content = personalData.domain;
        domain.innerHTML = content.join(',');
        // domain.innerHTML = '媒体';
    }else{
        domain.innerHTML = "无此数据";
    }
        
    var topic = document.getElementById('userTopic');
    if(personalData.topic){
        var topicdict = personalData.topic;
        var str = '';
        for(var i = 0;i < topicdict.length;i++){
            if (i == (topicdict.length -1)){
                str += topicdict[i][0];
            }else{
                str = str + topicdict[i][0] +',';
            }
            
        }
        topic.innerHTML = str;
        // topic.innerHTML = '生活，娱乐';
    }else{
        topic.innerHTML = "无此数据";
    }
}
function draw_weibo(weibo_data){
   $('#statistic').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">原创微博数</th><th style="text-align:center">转发微博数</th>';
    html += '<th style="text-align:center">被转发总数</th><th style="text-align:center">被评论总数</th>';
    html += '<th style="text-align:center">单条被转发最大值</th><th style="text-align:center">单条被评论最大值</th>';
    html += '<th style="text-align:center">关注度</th></tr>';
    
    html += '<tr>';
    for (var i = 0;i < 7; i++){
        html += '<th style="text-align:center">' + i + '</th>';
    }
    html += '</tr></table>';
    $('#statistic').append(html);
}
function point2weibo(xnum, ts){
	var url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts[0];
    var delta;
    //console.log(url);
	base_call_ajax_request(url, draw_content);
    $('#date_zh').html(getDate_zh(ts));
    switch(xnum % 6)
    {
        case 0: delta = "00:00-04:00";break;
        case 1: delta = "04:00-08:00";break;
        case 2: delta = "08:00-12:00";break;
        case 3: delta = "12:00-16:00";break;
        case 4: delta = "16:00-20:00";break;
        case 5: delta = "20:00-24:00";break;
    }
    $('#time_zh').html(delta);
	function draw_content(data){
        var html = '';
        $('#weibo_text').empty();
        if(data==''){
            html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
        }else{
            for(i=0;i<data.length;i++){
                //console.log(data[i].text);
                html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i].text+"</span></div>";
            }

        }
        $('#weibo_text').append(html);
    }
}
function Draw_personal_weibo_date(){
    $('#personal_weibo_date').empty();
    html = '';
    html += '<select id="select_personal_weibo_date" style="width:120px;">';
    var timestamp = Date.parse(new Date());
    date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    html += '<option value="' + date + '" selected="selected">' + date + '</option>';      
    for (var i = 0; i < 6; i++) {
        timestamp = timestamp-24*3600*1000;
        date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
        html += '<option value="' + date + '">' + date + '</option>';
    }
    html += '</select>';
    $('#personal_weibo_date').append(html);
}


function draw(data){
    console.log(data);
    var personalData = data;
    drawBasic(personalData);
    drawInfluenceTrend(personalData.influence_trend);
    drawTimeTrend(personalData.time_trend);
    drawTrack(personalData.activity_geo_distribute);

    var rank_list = new Array();
    rank_list['repost'] = 'retweet';
    rank_list['retweeted'] = 'follow';
    rank_list['top_at'] = 'at';
    var more_div_list = new Array();
    more_div_list['repost'] = 'more_repost';
    more_div_list['retweeted'] = 'more_retweeted';
    more_div_list['top_at'] = 'more_at';
    for (var div_name in rank_list){
        var key = rank_list[div_name];
        var more_div = more_div_list[div_name];
        drawRank(div_name, data[key][0], more_div);
    }
    // unfinished
    Draw_think_topic();
    Draw_think_emotion();
    draw_weibo('ere');
}
var person_url = '/attribute/portrait_attribute/?uid=' + uid;
call_ajax_request(person_url, draw);

Draw_personal_weibo_date();
