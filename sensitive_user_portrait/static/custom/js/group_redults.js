function draw_linechart(id){
    var myChart = echarts.init(document.getElementById(id)); 
    var option = {
    title : {
        text : '时间坐标折线图',
        subtext : 'dataZoom支持'
    },
    tooltip : {
        trigger: 'item',
        formatter : function (params) {
            var date = new Date(params.value[0]);
            data = date.getFullYear() + '-'
                   + (date.getMonth() + 1) + '-'
                   + date.getDate() + ' '
                   + date.getHours() + ':'
                   + date.getMinutes();
            return data + '<br/>'
                   + params.value[1] + ', ' 
                   + params.value[2];
        }
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
        data : ['series1']
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
    series : [
        {
            name: 'series1',
            type: 'line',
            showAllSymbol: true,
            symbolSize: function (value){
                return Math.round(value[2]/10) + 2;
            },
            data: (function () {
                var d = [];
                var len = 0;
                var now = new Date();
                var value;
                while (len++ < 200) {
                    d.push([
                        new Date(2014, 9, 1, 0, len * 10000),
                        (Math.random()*30).toFixed(2) - 0,
                        (Math.random()*100).toFixed(2) - 0
                    ]);
                }
                return d;
            })()
        }
    ]
};
    myChart.setOption(option);                   
}


function draw_barchart(id){
    console.log("fsdfsd")
    var myChart1 = echarts.init(document.getElementById(id)); 
    option = {
    timeline:{
        data:[
            '2002-01-01','2003-01-01','2004-01-01','2005-01-01'
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
                'text':'2002全国宏观经济指标',
                'subtext':'数据来自国家统计局'
            },
            tooltip : {'trigger':'axis'},
            legend : {
                x:'right',
                'data':['GDP','金融','房地产','第一产业','第二产业','第三产业'],
                'selected':{
                    'GDP':true,
                    '金融':false,
                    '房地产':true,
                    '第一产业':false,
                    '第二产业':false,
                    '第三产业':false
                }
            },
            toolbox : {
                'show':true, 
                orient : 'vertical',
                x: 'right', 
                y: 'center',
                'feature':{
                    'mark':{'show':true},
                    'dataView':{'show':true,'readOnly':false},
                    'magicType':{'show':true,'type':['line','bar','stack','tiled']},
                    'restore':{'show':true},
                    'saveAsImage':{'show':true}
                }
            },
            calculable : true,
            grid : {'y':80,'y2':100},
            yAxis : [{
                'type':'category',
                'axisLabel':{'interval':0},
                'data':[
                    '北京','\n天津','河北','\n山西','内蒙古','\n辽宁','吉林','\n黑龙江',
                    '上海','\n江苏','浙江','\n安徽','福建','\n江西','山东','\n河南',
                    '湖北','\n湖南','广东','\n广西','海南','\n重庆','四川','\n贵州',
                    '云南','\n西藏','陕西','\n甘肃','青海','\n宁夏','新疆'
                ]
            }],
            xAxis : [
                {
                    'type':'value',
                    'name':'GDP（亿元）',
                    'max':53500
                },
                {
                    'type':'value',
                    'name':'其他（亿元）'
                }
            ],
            series : [
                {
                    'name':'GDP',
                    'type':'bar',
                    'markLine':{
                        symbol : ['arrow','none'],
                        symbolSize : [4, 2],
                        itemStyle : {
                            normal: {
                                lineStyle: {color:'orange'},
                                barBorderColor:'orange',
                                label:{
                                    position:'left',
                                    formatter:function(params){
                                        return Math.round(params.value);
                                    },
                                    textStyle:{color:'orange'}
                                }
                            }
                        },
                        'data':[{'type':'average','name':'平均值'}]
                    },
                    'data': dataMap.dataGDP['2002']
                },
                {
                    'name':'金融','yAxisIndex':1,'type':'bar',
                    'data': dataMap.dataFinancial['2002']
                },
                {
                    'name':'房地产','yAxisIndex':1,'type':'bar',
                    'data': dataMap.dataEstate['2002']
                },
                {
                    'name':'第一产业','yAxisIndex':1,'type':'bar',
                    'data': dataMap.dataPI['2002']
                },
                {
                    'name':'第二产业','yAxisIndex':1,'type':'bar',
                    'data': dataMap.dataSI['2002']
                },
                {
                    'name':'第三产业','yAxisIndex':1,'type':'bar',
                    'data': dataMap.dataTI['2002']
                }
            ]
        },
        {
            title : {'text':'2003全国宏观经济指标'},
            series : [
                {'data': dataMap.dataGDP['2003']},
                {'data': dataMap.dataFinancial['2003']},
                {'data': dataMap.dataEstate['2003']},
                {'data': dataMap.dataPI['2003']},
                {'data': dataMap.dataSI['2003']},
                {'data': dataMap.dataTI['2003']}
            ]
        },
        {
            title : {'text':'2004全国宏观经济指标'},
            series : [
                {'data': dataMap.dataGDP['2004']},
                {'data': dataMap.dataFinancial['2004']},
                {'data': dataMap.dataEstate['2004']},
                {'data': dataMap.dataPI['2004']},
                {'data': dataMap.dataSI['2004']},
                {'data': dataMap.dataTI['2004']}
            ]
        },
        {
            title : {'text':'2005全国宏观经济指标'},
            series : [
                {'data': dataMap.dataGDP['2005']},
                {'data': dataMap.dataFinancial['2005']},
                {'data': dataMap.dataEstate['2005']},
                {'data': dataMap.dataPI['2005']},
                {'data': dataMap.dataSI['2005']},
                {'data': dataMap.dataTI['2005']}
            ]
        }
    ]
};
                    
    myChart1.setOption(option);                
}


$(document).ready(function(){
    draw_linechart('active');
    draw_linechart('emotion');
    draw_linechart('sensitivity');
    draw_linechart('user');
    draw_barchart('location');
    draw_barchart('hashtag');
})
