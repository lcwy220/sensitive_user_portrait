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