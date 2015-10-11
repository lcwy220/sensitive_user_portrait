//影响力走势图
var influenceChart = echarts.init(document.getElementById('influence_chart')); 
        
    var Influenceoption = {
        title : {
            text: '影响力走势图',
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
                //data : line_chart_dates
				data:['2015-09-01','2015-09-02','2015-09-03','2015-09-04','2015-09-05','2015-09-06','2015-09-07']
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
                //data:dataFixed,
				data:[345,23,55,25,897,34,88,100],
				
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
//一周轨迹分布
$('.course_nr2').find('.shiji').slideDown(600);

for(i=0;i<7;i++){
		document.getElementById('d'+(i+1)).innerHTML = '09-01';
    }
for(i=0;i<7;i++){
		document.getElementById('city'+(i+1)).innerHTML = '北京';
		/*
        console.log(citys[i]);
		if(citys[i]){
			document.getElementById('city'+(i+1)).innerHTML = citys[i][0];
		}else{
			$('#city'+(i+1)).addClass('gray');
			document.getElementById('city'+(i+1)).innerHTML = '未发布微博';
		}
		*/
		
	}// JavaScript Document

//敏感词
var sensitive_words = ['a1', 'b1', '1c', '1d'];
var word_length = sensitive_words.length;
var addwords = ''
for(i=0;i<word_length;i++){
    addwords = addwords+'<span>'+sensitive_words[i]+',</span>'
}
document.getElementById('sensi_words').innerHTML = addwords

//hashtag云
var hashtag_cloud = echarts.init(document.getElementById('hashtag_cloud'));

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

var hashtag_data = {
    title: {
        text: '',
        
    },
    tooltip: {
        show: true
    },
    series: [{
        name: 'hashtag云',
        type: 'wordCloud',
        size: ['90%', '90%'],
        textRotation : [0, 45, 90, -45],
        textPadding: 0,
        autoSize: {
            enable: true,
            minSize: 14
        },
        data: [
            {
                name: "敏感词",
                value: 10000,
                itemStyle: {
                    normal: {
                        color: 'black'
                    }
                }
            },
            {
                name: "hashtag",
                value: 6181,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "我我哦我",
                value: 4386,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Jurassic World",
                value: 4055,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Charter Communications",
                value: 2467,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Chick Fil A",
                value: 2244,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Planet Fitness",
                value: 1898,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Pitch Perfect",
                value: 1484,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Express",
                value: 1112,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Home",
                value: 965,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Johnny Depp",
                value: 847,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Lena Dunham",
                value: 582,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Lewis Hamilton",
                value: 555,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "KXAN",
                value: 550,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Mary Ellen Mark",
                value: 462,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Farrah Abraham",
                value: 366,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Rita Ora",
                value: 360,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Serena Williams",
                value: 282,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "NCAA baseball tournament",
                value: 273,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Point Break",
                value: 265,
                itemStyle: createRandomItemStyle()
            }
        ]
    }]
};
hashtag_cloud.setOption(hashtag_data);                 

//敏感词云
var sensiword_cloud = echarts.init(document.getElementById('sensi_word_cloud'));
var sensicloud_data = {
    title: {
        text: '',
        
    },
    tooltip: {
        show: true
    },
    series: [{
        name: 'hashtag云',
        type: 'wordCloud',
        size: ['80%', '80%'],
        textRotation : [0, 45, 90, -45],
        textPadding: 0,
        autoSize: {
            enable: true,
            minSize: 14
        },
        data: [
            {
                name: "敏感词",
                value: 10000,
                itemStyle: {
                    normal: {
                        color: 'black'
                    }
                }
            },
            {
                name: "hashtag",
                value: 6181,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "我我哦我",
                value: 4386,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Jurassic World",
                value: 4055,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Charter Communications",
                value: 2467,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Chick Fil A",
                value: 2244,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Planet Fitness",
                value: 1898,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Pitch Perfect",
                value: 1484,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Express",
                value: 1112,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Home",
                value: 965,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Johnny Depp",
                value: 847,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Lena Dunham",
                value: 582,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Lewis Hamilton",
                value: 555,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "KXAN",
                value: 550,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Mary Ellen Mark",
                value: 462,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Farrah Abraham",
                value: 366,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Rita Ora",
                value: 360,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Serena Williams",
                value: 282,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "NCAA baseball tournament",
                value: 273,
                itemStyle: createRandomItemStyle()
            },
            {
                name: "Point Break",
                value: 265,
                itemStyle: createRandomItemStyle()
            }
        ]
    }]
};
sensiword_cloud.setOption(sensicloud_data);  


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
            data : ['周一','周二','周三','周四','周五','周六','周日']
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
            data:[120, 132, 101, 134, 90, 230, 210]
        },
        {
            name:'消极',
            type:'line',
            stack: '总量',
            data:[220, 182, 191, 234, 290, 330, 310]
        },
        {
            name:'中性',
            type:'line',
            stack: '总量',
            data:[150, 232, 201, 154, 190, 330, 410]
        }
    ]
};               
emotion_charts.setOption(emotion_data);

//敏感微博
var origin_time=[['origin_time','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]
var origin_cmt=[['origin_cmt','新闻新闻新闻新新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]
var origin_re=[['origin_re','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]
var retweeted_time=[['retweeted_time','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]
var retweeted_cmt=[['retweeted_cmt','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]
var retweeted_re=[['retweeted_re','新闻闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链'],['name','新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻新闻','palce','date','情绪','转发链']]


$('#weibo_content2').empty();
var html = "";
var data = origin_time;
var weibo_num = origin_time.length;
    html += '<div class="group_weibo_font">';
    for (var i = 0; i < weibo_num; i += 1){
        var s=i.toString();
        var uname = data[s][0]
        var text = data[s][1]
        var palce = data[s][2];
        var date = data[s][3];
        var emotin = data[s][4];
        timestamp = data[s]['timestamp'];
        //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="background:whitesmoke;font-size:14px;padding:10px;">';
        }
        else{
            html += '<div style="font-size:14px;padding:10px;">';
        }
            //html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p><strong style="color:red;margin-right:10px;">' + emotin +'</strong>' + uname + '&nbsp;&nbsp;发布:&nbsp;&nbsp;<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:5px"><font color:#e0e0e0>' + date + '</font><span style="margin-left:20px;"><img src="/static/custom/images/location.png" style="width:10px;" />&nbsp;&nbsp;'+ palce +'</span></p>';
            html += '</div>';
        
    }
    html += '</div>'; 
    $('#weibo_content2').append(html);

$('input[name="origin_re"]').click(function(){
    var html = "";
    if($('input[name="origin_re"]:checked').val()==2){
        if($('input[name="seq_method"]:checked').val()==1){
            data = retweeted_time;
            weibo_num = retweeted_time.length;
        }else if($('input[name="seq_method"]:checked').val()==2){
            data = retweeted_re;
            weibo_num = retweeted_re.length;
        }else if($('input[name="seq_method"]:checked').val()==3){
            data = retweeted_cmt;
            weibo_num = retweeted_cmt.length;
        }
        
        $('#weibo_content2').empty();

        html += '<div class="group_weibo_font">';
        for (var i = 0; i < weibo_num; i += 1){
            var s=i.toString();
            var uname = data[s][0]
            var text = data[s][1]
            var palce = data[s][2];
            var date = data[s][3];
            var emotin = data[s][4];
            timestamp = data[s]['timestamp'];
            //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
            if (i%2 ==0){
                html += '<div style="background:whitesmoke;font-size:14px;padding:10px;">';
            }
            else{
                html += '<div style="font-size:14px;padding:10px;">';
            }
                //html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
                html += '<p><strong style="color:red;margin-right:10px;">' + emotin +'</strong>' + uname + '&nbsp;&nbsp;发布:&nbsp;&nbsp;<font color=black>' + text + '</font></p>';
                html += '<p style="margin-top:5px"><font color:#e0e0e0>' + date + '</font><span style="margin-left:20px;"><img src="/static/custom/images/location.png" style="width:10px;" />&nbsp;&nbsp;'+ palce +'</span><a style="float:right;margin-right:30px;" data-toggle="modal" data-target="#retweeted_line" href="remote.html">转发链</a></p>';
                html += '</div>';
            
        }
        html += '</div>'; 
        $('#weibo_content2').append(html);
    }else{
        if($('input[name="seq_method"]:checked').val()==1){
            data = origin_time;
            weibo_num = origin_time.length;
        }else if($('input[name="seq_method"]:checked').val()==2){
            data = origin_re;
            weibo_num = origin_re.length;
        }else if($('input[name="seq_method"]:checked').val()==3){
            data = origin_cmt;
            weibo_num = origin_cmt.length;
        }
        $('#weibo_content2').empty();
        html += '<div class="group_weibo_font">';
        for (var i = 0; i < weibo_num; i += 1){
            var s=i.toString();
            var uname = data[s][0]
            var text = data[s][1]
            var palce = data[s][2];
            var date = data[s][3];
            var emotin = data[s][4];
            timestamp = data[s]['timestamp'];
            //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
            if (i%2 ==0){
                html += '<div style="background:whitesmoke;font-size:14px;padding:10px;">';
            }else{
                html += '<div style="font-size:14px;padding:10px;">';
            }
            //html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p><strong style="color:red;margin-right:10px;">' + emotin +'</strong>' + uname + '&nbsp;&nbsp;发布:&nbsp;&nbsp;<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:5px"><font color:#e0e0e0>' + date + '</font><span style="margin-left:20px;"><img src="/static/custom/images/location.png" style="width:10px;" />&nbsp;&nbsp;'+ palce +'</span></p>';
            html += '</div>'; 
        }    
        html += '</div>'; 
        $('#weibo_content2').append(html);}
})


$('input[name="seq_method"]').click(function(){
    var html = "";
    if($('input[name="origin_re"]:checked').val()==2){
        if($('input[name="seq_method"]:checked').val()==1){
            data = retweeted_time;
            weibo_num = retweeted_time.length;
        }else if($('input[name="seq_method"]:checked').val()==2){
            data = retweeted_re;
            weibo_num = retweeted_re.length;
        }else if($('input[name="seq_method"]:checked').val()==3){
            data = retweeted_cmt;
            weibo_num = retweeted_cmt.length;
        }
        $('#weibo_content2').empty();

        html += '<div class="group_weibo_font">';
        for (var i = 0; i < weibo_num; i += 1){
            var s=i.toString();
            var uname = data[s][0]
            var text = data[s][1]
            var palce = data[s][2];
            var date = data[s][3];
            var emotin = data[s][4];
            timestamp = data[s]['timestamp'];
            //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
            if (i%2 ==0){
                html += '<div style="background:whitesmoke;font-size:14px;padding:10px;">';
            }
            else{
                html += '<div style="font-size:14px;padding:10px;">';
            }
                //html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
                html += '<p><strong style="color:red;margin-right:10px;">' + emotin +'</strong>' + uname + '&nbsp;&nbsp;发布:&nbsp;&nbsp;<font color=black>' + text + '</font></p>';
                html += '<p style="margin-top:5px"><font color:#e0e0e0>' + date + '</font><span style="margin-left:20px;"><img src="/static/custom/images/location.png" style="width:10px;" />&nbsp;&nbsp;'+ palce +'</span><a style="float:right;margin-right:30px;" data-toggle="modal" data-target="#retweeted_line" href="remote.html">转发链</a></p>';
                html += '</div>';
            
        }
        html += '</div>'; 
        $('#weibo_content2').append(html);
    }else{
        if($('input[name="seq_method"]:checked').val()==1){
            data = origin_time;
            weibo_num = origin_time.length;
        }else if($('input[name="seq_method"]:checked').val()==2){
            data = origin_re;
            weibo_num = origin_re.length;
        }else if($('input[name="seq_method"]:checked').val()==3){
            data = origin_cmt;
            weibo_num = origin_cmt.length;
        }
        $('#weibo_content2').empty();
        html += '<div class="group_weibo_font">';
        for (var i = 0; i < weibo_num; i += 1){
            var s=i.toString();
            var uname = data[s][0]
            var text = data[s][1]
            var palce = data[s][2];
            var date = data[s][3];
            var emotin = data[s][4];
            timestamp = data[s]['timestamp'];
            //date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
            if (i%2 ==0){
                html += '<div style="background:whitesmoke;font-size:14px;padding:10px;">';
            }else{
                html += '<div style="font-size:14px;padding:10px;">';
            }
            //html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p><strong style="color:red;margin-right:10px;">' + emotin +'</strong>' + uname + '&nbsp;&nbsp;发布:&nbsp;&nbsp;<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:5px"><font color:#e0e0e0>' + date + '</font><span style="margin-left:20px;"><img src="/static/custom/images/location.png" style="width:10px;" />&nbsp;&nbsp;'+ palce +'</span></p>';
            html += '</div>'; 
        }    
        html += '</div>'; 
        $('#weibo_content2').append(html);}
})
var table_data=[{'word':'敏感词1','frency':20,'word_level':'leve1','word_class':'b类词'},{'word':'敏感词2','frency':18,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词3','frency':17,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词4','frency':12,'word_level':'leve2','word_class':'a类词'},{'word':'敏感词5','frency':10,'word_level':'leve1','word_class':'b类词'},{'word':'敏感词6','frency':9,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词7','frency':8,'word_level':'leve1','word_class':'a类词'},]   
//敏感词表格
//画表格


$('#show_sensi_word').click(function (){
    var word_level=$("#sensi_word_level").val();
    var word_class=$("#sensi_word_class").val();
    var choose_data=[];
    alert(word_level);
    //var need_data=[]
    if (word_level==0){
        if (word_class==1){
            choose_data = table_data;
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==3){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }
    }else if(word_level==1){
        if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1'){
                    choose_data.push(table_data[i])
                }

            }
            choose_data = table_data;
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1' & table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==3){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1' & table_data[i]['word_level']=='b类词'){
                    choose_data.push(table_data[i])
                }

            }
        }

        }else if(word_level==2){
        if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2' & table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==3){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2' & table_data[i]['word_level']=='b类词'){
                    choose_data.push(table_data[i])
                }

            }
        }

    }
drawRank('sensiword_table',choose_data);   

    })

function drawRank(div_name, rank_data){
    if (!rank_data){
        rank_data = new Array();
    }
    $('#'+ div_name).empty();
        html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">敏感词</th>';
        //html += '<th style="text-align:center">' + cname + '</th></tr>';
        var min_row = Math.min(10, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           var item = rank_data[i];
           var nickname;
           if ((item['word'] == 'unknown') || (item['word'] == '0')){
               nickname = '未知';
           }
           else{
               nickname = item['word'];
           }
         html += '<tr><th style="text-align:center">' + m + '</th>';
         html += '<th style="text-align:center">' + nickname + '</a></th>';
         //html += '<th style="text-align:center">' + item[2].toFixed(2) + '</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);
        }  
drawRank('sensiword_table',table_data)




