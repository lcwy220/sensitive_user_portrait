// function month_process(data){
//     console.log(data,'eee');

//     $('#active_geo').append("<div>");
//     for(var i in data){
//         $('#active_geo').append("日期：" + data[i][0] + "，位置：" + data[i][1]);
//     }
//     $('#active_geo').append("</div>");
// }
function show_geo_track(data){
    console.log(data,'ddd');


var myDate = new Date(); //获取今天日期
myDate.setDate(myDate.getDate() - 7);
var dateArray = []; 
var dateTemp; 
var flag = 1; 
for (var i = 0; i < 7; i++) {
    dateTemp = (myDate.getFullYear()-1)+'-'+(myDate.getMonth()+1)+"-"+myDate.getDate();
    dateArray.push(dateTemp);
    myDate.setDate(myDate.getDate() + flag);
}
console.log(dateArray);

    $('#active_geo').empty();
    var html = '';
    html += '<table id="select_track_weibo_user" style="table-layout:auto" class="table table-bordered table-striped table-condensed datatable" >';
    html += '<thead><tr style="text-align:center;"> ';
    html += '<th style="width:160px;">用户ID</th>';
    html += '<th style="width:170px;">昵称</th><th>注册地</th>';
    for(j=0;j<dateArray.length;j++){
        html +='<th style="width:170px;">'+dateArray[j]+'</th>';
    }
    html += '</thead>';
    html += '<tbody>';
    for (i=0;i<data.length;i++){
        html += '<tr>';
        //var time0 = new Date(item[i][1]*1000).format('yyyy/MM/dd hh:mm')
        if(data[i][1]=='unknown'){
            data[i][1] = '未知';
        }
        html += '<td >'+data[i][0]+'</td>';
        html += '<td>'+data[i][1]+'</td>';
        html += '<td>'+data[i][3]+'</td>';
        for(var k=0;k<data[i][6].length;k++){
            html += '<td>'+data[i][6][k][1]+'</td>';
        }
        html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';

    $('#active_geo').append(html);
    $('#select_track_weibo_user').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "aaSorting": [[ 1, "desc" ]],
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[5]}],
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
}
/*
function track_init(){
    require.config({
        paths: {
            echarts: '/static/js/bmap/js'
        },
        packages: [
            {
                name: 'BMap',
                location: '/static/js/bmap',
                main: 'main'
            }
        ]
    });

    require(
    [
        'echarts',
        'BMap',
        'echarts/chart/map'
    ],
    function (echarts, BMapExtension) {
        // 初始化地图
        var BMapExt = new BMapExtension($('#user_geo_map')[0], BMap, echarts,{
            enableMapClick: false
        });
        var map = BMapExt.getMap();
        var container = BMapExt.getEchartsContainer();
        var startPoint = {
            x: 85.114129,
            y: 50.550339
        };

        var point = new BMap.Point(startPoint.x, startPoint.y);
        map.centerAndZoom(point, 5);
        //map.enableScrollWheelZoom(true);
    }
);
}
*/

function Draw_top_location(data){
	var timeline_data = [];
	var bar_data = [];
	var bar_data_x = [];
	var bar_data_y = [];
	for(var key in data){
		var key_time = new Date(parseInt(key)*1000).format("yyyy-MM-dd");
		timeline_data.push(key_time);
		bar_data.push(data[key]);
        //console.log(data[key]);
        //console.log(key_time);
        // var data_xx = [];
        // for(var j in data[key]){
        //     data_xx.push(j);
        // }
        //console.log(data_xx.length);
    }
    //console.log(timeline_data);
    //console.log(data.key.length)
	for(var i=0;i<bar_data.length;i++){
		var bar_data_x_single = [];
		var bar_data_y_single = [];
		// for(var key in bar_data[i]){
        for(var j=0; j<bar_data[i].length;j++){
            //var city = key.split('\t')
            //console.log(city.pop());
			//bar_data_x_single.push(key);
			bar_data_x_single.push(bar_data[i][j][0]);
			bar_data_y_single.push(bar_data[i][j][1]);
		}
		bar_data_x.push(bar_data_x_single);
		bar_data_y.push(bar_data_y_single);
	}
	
	var bar_data_2 = []
	for(var j=0;j<bar_data_x.length;j++){
        var bar_data_x_2 = []
        if(bar_data_x[j].length>45){
            bar_data_x[j].length = 45;
		}
		for(var i = 0;i<bar_data_x[j].length;i++){
            if(i%2 != 0){
                bar_data_x_2.push('\n'+bar_data_x[j][i]);
		    }else{
                bar_data_x_2.push(bar_data_x[j][i]);
            }
	    }
        bar_data_2.push(bar_data_x_2);
	}
	//console.log(bar_data_x);
	//console.log(bar_data_2);
	bar_data_x = bar_data_2;
	
		//console.log(timeline_data.length);
    var myChart = echarts.init(document.getElementById('top_active_geo_line')); 
    var option = {
        timeline:{
            data:timeline_data,
            // label : {
            //     formatter : function(s) {
            //         return s.slice(0, 4);
            //     }
            // },
            autoPlay : true,
            playInterval : 1000
        },
        toolbox : {
            'show':false, 
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
        options : (function () {
        	var option_data = [];
        	for(var i=0;i<timeline_data.length;i++){
        		var option_single_data = {};
        		option_single_data.title={'text': '' };
        		option_single_data.tooltip ={'trigger':'axis'};
        		option_single_data.calculable = true;
                option_single_data.grid = {'y':50,'y2':100};
                option_single_data.xAxis = [{
                    'type':'category',
                    'axisLabel':{'interval':0},
                    'data':bar_data_x[i]
                }];
                option_single_data.yAxis = [
                    {
                        'type':'value',
                        'name':'活跃次数',
                        //'max':53500
                    }
                ];
                option_single_data.series = [
                    {
                        'name':'活跃次数',
                        'type':'bar',
                        'barwidth':10,
                        'data': bar_data_y[i]
                    },

                ];
                option_data.push(option_single_data);
        	};
        	//console.log(option_data);
        	return option_data;
        }
        )()
    };
    myChart.setOption(option);
                    
}

/*
function moving_geo(data){
    //var data = {'北京&上海2': 150,'北京2&上海': 122,'北京2&上海2': 170,'北京4&上海2': 750, '北京5&上海': 120};
    var dealt_data = get_max_data(data);
    $('#move_location').empty();
    var from_city = [];
    var end_city = [];
    for(var i=0;i < dealt_data[0].length;i++){
        var city_split = dealt_data[0][i].split('&');
        var from_last_city = city_split[0].split('\t');
        var end_last_city = city_split[1].split('\t');
        from_city.push(from_last_city[from_last_city.length-1])
        end_city.push(end_last_city[end_last_city.length-1]);
    }
    var html = '';
    if (dealt_data[0].length == 0){
        html += '<span style="margin:20px;">暂无数据</span>';
        $('#geo_show_more').css('display', 'none');
        $('#move_location').css('height', '260px');
    }else{
        if(dealt_data[0].length < 5){
            $('#geo_show_more').css('display', 'none');
        };
            Draw_more_moving_geo(from_city, end_city, dealt_data);
            html += '<table class="table table-striped" style="width:100%;font-size:14px;margin-bottom:0px;">';
            html += '<tr><th style="text-align:center">起始地</th>';
            html += '<th style="text-align:right;width:30px;"></th>';
            html += '<th style="text-align:left">目的地</th>';
            html += '<th style="text-align:center">人次</th>';
            html += '</tr>';
            for (var i = 0; i < 5; i++) {
                html += '<tr>';
                html += '<td style="text-align:center;vertical-align: middle;">' + from_city[i] + '</td>';
                html += '<td style="text-align:center;"><img src="/../../static/img/arrow_geo.png" style="width:25px;"></td>';
                html += '<td style="text-align:center;vertical-align: middle;">' + end_city[i] + '</td>';
                html += '<td style="text-align:center;vertical-align: middle;">' + dealt_data[1][i] + '</td>';
            html += '</tr>'; 
            };
            html += '</table>'; 
        
    }
    $('#move_location').append(html);
}

function Draw_more_moving_geo(from_city, end_city, dealt_data){
    // var data = [['北京', '上海', 100], ['北京', '1上海', 100], ['北京', '上1海', 20],['北京', '1上海', 100],  ['北京', '上海', 30]];
    $('#move_location_more_detail').empty();
    var html = '';
    html += '<table class="table table-striped " font-size:14px">';
    html += '<tr><th style="text-align:center">起始地</th>';
    html += '<th style="text-align:right"></th>';
    html += '<th style="text-align:center">目的地</th>';
    html += '<th style="text-align:center">人次</th>';
    html += '</tr>';
    for (var i = 0; i < dealt_data[0].length; i++) {
        html += '<tr>';
        html += '<td style="text-align:center;vertical-align: middle;">' + from_city[i] + '</td>';
        html += '<td style="text-align:center;"><img src="/../../static/img/arrow_geo.png" style="width:30px;"></td>';
        html += '<td style="text-align:center;vertical-align: middle;">' + end_city[i] + '</td>';
        html += '<td style="text-align:center;vertical-align: middle;">' + dealt_data[1][i] + '</td>';
    html += '</tr>'; 
    };
    html += '</table>'; 
    $('#move_location_more_detail').append(html);
}
*/

function show_geo(data){
	console.log("geo data: ");
	console.log(data);
    //活跃地区分布
	Draw_top_location(data.activity_geo_disribution);

	//位置转移统计
    //moving_geo(data.activiy_geo_vary);
    //var data333 = {'北京&上海2': 150,'北京2&上海': 122,'北京2&上海2': 170,'北京4&上海2': 750, '北京5&上海': 120};
}

function geo_load(){
    var group_geo_url = '/group/show_group_result/?module=geo&task_name=' + task_name + '&submit_user=' + submit_user;
    call_sync_ajax_request(group_geo_url,ajax_method, show_geo);
    //var group_user_url = "/group/show_group_list/?task_name=" + task_name + "&submit_user=" + submit_user;
    //call_sync_ajax_request(group_user_url,ajax_method, show_geo_track);
    var group_user_url = "/group/show_group_member_track/?task_name=" + task_name + "&submit_user=" + submit_user;
    call_sync_ajax_request(group_user_url,ajax_method, show_geo_track);
}