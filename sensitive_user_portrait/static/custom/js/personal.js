//微博时间走势图

/*
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


	 $('#weiboTime').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '微博时间走势图',
			align:'left',
			fontSize:'20',
        },
        subtitle: {
            text: '',
            x: -20
        },
        lang: {
                printChart: "打印",
                downloadJPEG: "下载JPEG 图片",
                downloadPDF: "下载PDF文档",
                downloadPNG: "下载PNG 图片",
                downloadSVG: "下载SVG 矢量图",
                exportButtonTitle: "导出图片"
            },
        xAxis: {
            //categories: data_time,
			categories:['00:00','04:00','08:00','12:00','16:00','20:00'],
            labels:{
              rotation: 0,
                        step: 6,
                        x:0,
                        y:30,
            }
        },
        yAxis: {
			min:0,
            title: {
                text: '微博总量 (条)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        plotOptions:{
            series:{            
                cursor:'pointer',
                events:{
                    click:function(event){
                        //point2weibo(event.point.x, trend[event.point.x]);
						alert('ad');
                    }
                }
            }
        },
        tooltip: {
            valueSuffix: '条',
            xDateFormat: '%H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            //data: data_count
			data:[1,2,5,3,6,8]
        }]
    });
  

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
*/

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
$('.course_nr2 li').find('.shiji').slideDown(600);

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
		
	}

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
	