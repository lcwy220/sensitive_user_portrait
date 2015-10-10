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
/*

//思想分析
$(document).ready(function(){
 		Draw_think_topic();
 		Draw_think_emotion();
 	})
        // 基于准备好的dom，初始化echarts图表
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
            text: '',
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
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}
function Draw_think_emotion(){
    var myChart = echarts.init(document.getElementById('pie_emotion')); 
    var option = {
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
*/
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
function draw(data){
    console.log(data);
    var personalData = data;
    drawBasic(personalData);
    drawInfluenceTrend(personalData.influence_trend);
    drawTimeTrend(personalData.time_trend);
    drawTrack(personalData.activity_geo_distribute);
}
var person_url = '/attribute/portrait_attribute/?uid=' + uid;
call_ajax_request(person_url, draw);
	
