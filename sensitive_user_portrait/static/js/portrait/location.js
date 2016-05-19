function getFullDate(tm){
    var tt = new Date(parseInt(tm)*1000).format("yyyy-MM-dd hh:mm:ss");
    return tt;
}
function getYearDate(tm){
    var tt = new Date(parseInt(tm)*1000).format("yyyy-MM-dd");
    return tt;
}
function getDate(tm){
    var tt = new Date(parseInt(tm)*1000).format("MM-dd hh:mm");
    return tt;
}
function getDate_zh(tm){
    var tt = new Date(parseInt(tm)*1000).format("MM-dd");
    return tt;
}
function getDate_ms(tm){
    var tt = new Date(parseInt(tm)*1000).format("hh:mm");
    return tt;
}
function bind_time_option(){
    $('input[name=weibotrends]').change(function(){
        var selected_type = $(this).val();
        global_time_type = selected_type;
        if (global_time_type == 'day'){
            week_chart(global_active_data.day_trend);
        }
        else{
            week_chart(global_active_data.week_trend);
        }
    });
}
function activity_call_ajax_request(url, callback){
    $.ajax({
        url:url,
        method:'GET',
        dataType:'json',
        async:false,
        success:callback,
    });
}
function geo_track(data){
    var geo_data = data.week_geo_track;
	var date = [];
	var citys = [];
	for(var key in geo_data){
		date.push(getDate_zh(key));
        citys.push(geo_data[key][0])
	}
	for(i=0;i<date.length;i++){
		document.getElementById('d'+(i+1)).innerHTML = date[i];
    }
    for(i=0;i<citys.length;i++){
		if(citys[i]){
			document.getElementById('city'+(i+1)).innerHTML = citys[i][0];
		}else{
			$('#city'+(i+1)).addClass('gray');
			document.getElementById('city'+(i+1)).innerHTML = '未发布微博';
		}
		
	}
}


function  active_chart(data){
    global_active_data = data;
	//console.log.log(global_active_data);
	/*
    var tag_vector = data.tag_vector;
    //active time
    var name = tag_vector[0][0];
    var value;
    var active_date = tag_vector[0][1][0][0]/(15*60*16);
   switch(active_date)
   {
        case 0: value = "00:00-04:00";break;
        case 1: value = "04:00-08:00";break;
        case 2: value = "08:00-12:00";break;
        case 3: value = "12:00-16:00";break;
        case 4: value = "16:00-20:00";break;
        case 5: value = "20:00-24:00";break;
   }
   global_tag_vector.push([name, value]);
   //active type
   global_tag_vector.push(tag_vector[1]);
    
    var this_desc= '';
    this_desc += "<span>" + data.description[0] + "</span><span style='color:red;'>" + data.description[1] + "</span>"; //description
    this_desc += "<span>" + data.description[2] + "</span><span style='color:red;'>" + data.description[3] + "</span>。"; //description
    $('#saysay').html(this_desc);
	*/
    if (global_time_type == 'day'){
		//console.log.log("day");
       week_chart(data.day_trend);
    }
    // week
    else{
		//console.log.log("week");
        week_chart(data.week_trend);
    }
}
function week_chart(trend_data){
    var trend = trend_data;
	//console.log.log(trend);
    var data_count=[];
    var data_time = [];
    var date_zhang = [];
    if (global_time_type == 'day'){
        for(i=0;i<trend.length;i++){
            var time = getDate(pre_time+trend[i][0]);
            //console.log.log(pre_time);
            var count = trend[i][1];
            var date_zh =getYearDate(pre_time+trend[i][0]);
            data_time.push(time);
            data_count.push(count);
            date_zhang.push(date_zh);
        }
        $('#time_zh').html('00:00-00:30');
        $('#date_zh').html(date_zhang[0]);
        var dateStr = getFullDate(pre_time+trend[0][0]);
        var ts = get_unix_time(dateStr);
        //console.log.log('ts',ts);
        var url ="/attribute/activity_weibo/?uid="+uid+"&type="+global_time_type+"&start_ts="+ts;
        //console.log.log(url);
        activity_call_ajax_request(url, draw_content); // draw_weibo
    }
    else{
        for(i=0;i<trend.length;i++){
            var time = getDate(trend[i][0]);
            var count = trend[i][1];
            var date_zh =getYearDate(trend[i][0])
            data_time.push(time);
            data_count.push(count);
            date_zhang.push(date_zh);
        }
        $('#time_zh').html('00:00-04:00');
        $('#date_zh').html(date_zhang[0]);
        var dateStr = getFullDate(trend[0][0]);
        var ts = get_unix_time(dateStr);
        var url ="/attribute/activity_weibo/?uid="+uid+"&type="+global_time_type+"&start_ts="+ts;
        //console.log.log(url);
        activity_call_ajax_request(url, draw_content); // draw_weibo
    }
	//Draw_trend:
	 $('#Activezh').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '',
			align:'left',
			fontSize:'20',
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
            categories: data_time,
            labels:{
              formatter: function(){
                  if (global_time_type == 'day'){
                      return this.value.split(' ')[1];
                  }
                  else{
                      return this.value;
                  }
              },
              rotation: 0,
              step: 6,
              x:0,
              y:30,
            }
        },
        yAxis: {
			min:0,
            allowDecimals: false,
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
                        point2weibo(event.point.x, trend[event.point.x]);
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
            align: 'center',
            verticalAlign: 'top',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            data: data_count
        }]
    });
}
//微博文本默认数据
function point2weibo(xnum, ts){
	//console.log.log("fdghjkl;'l;kjhgfd");
    //console.log.log(xnum);
    var delta = '';
    if (global_time_type == 'day'){
        var url ="/attribute/activity_weibo/?uid="+uid+"&type="+global_time_type+"&start_ts="+(pre_time+ts[0]);
        //console.log.log(url);
        person_call_ajax_request(url, draw_content); //draw weibo

        var a = Math.floor(xnum / 2);
        var b = xnum % 2;
        delta += (a<10?"0"+a+":":a+":");
        delta += (b==0?"00-":"30-");
        if (b == 0){
            delta += (a<10?"0"+a+":":a+":");
            delta += "30";
        }
        else{
            a += 1;
            delta += (a<10?"0"+a+":":a+":");
            delta += "00";
        }
        $('#date_zh').html(getYearDate(pre_time+ts[0]));
    }
    else{
        var url ="/attribute/activity_weibo/?uid="+uid+"&type="+global_time_type+"&start_ts="+ts[0];
        person_call_ajax_request(url, draw_content); //draw weibo
        switch(xnum % 6)
        {
            case 0: delta = "00:00-04:00";break;
            case 1: delta = "04:00-08:00";break;
            case 2: delta = "08:00-12:00";break;
            case 3: delta = "12:00-16:00";break;
            case 4: delta = "16:00-20:00";break;
            case 5: delta = "20:00-24:00";break;
        }
        $('#date_zh').html(getYearDate(ts[0]));
    }
    $('#time_zh').html(delta);
}
function draw_content(data){
	//console.log.log(data);
    var html = '';
    $('#weibo_text').empty();
    if(data[0].length==0 && data[1].length==0){
        html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data[1].length;i++){
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;color:red;'><span>"+data[1][i].text+"</span><br></div>";
        }
		for(i=0;i<data[0].length;i++){
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[0][i].text+"</span><br></div>";
        }

    }
    $('#weibo_text').append(html);
}


function draw_daily_ip_table(ip_data){
    console.log(ip_data);
	var today_ip = document.getElementById('today_ip');
	if(ip_data.today_top_ip){
		today_ip.innerHTML = ip_data.today_top_ip;
		Draw_more_today(ip_data.today_ip_list,'more_today_ip');
	}else{
		today_ip.innerHTML = '暂无今日IP信息';
		$('#moreip').css('display','none');
        Draw_more_today('','more_today_ip');
	}
	var today_geo = document.getElementById('today_geo');
	if(ip_data.today_top_city){
		today_geo.innerHTML = ip_data.today_top_city;
		Draw_more_today(ip_data.today_geo_list,'more_today_geo');
	}else{
		today_geo.innerHTML = '暂无今日地点信息';
		$('#moregeo').css('display','none');
        Draw_more_today('','more_today_geo');
	}
	var today_sensitive_ip = document.getElementById('today_sensitive_ip');
	if(ip_data.today_top_sensitive_ip){
		today_sensitive_ip.innerHTML = ip_data.today_top_sensitive_ip;
		Draw_more_today(ip_data.today_sensitive_ip_list,'more_today_s_ip');
	}else{
		today_sensitive_ip.innerHTML = '暂无敏感IP信息';
		$('#moreSip').css('display','none');
        Draw_more_today('','more_today_s_ip');
	}
	var today_sensitive_geo = document.getElementById('today_sensitive_geo');
	if(ip_data.today_sensitive_top_city){
		today_sensitive_geo.innerHTML = ip_data.today_sensitive_top_city;
		Draw_more_today(ip_data.today_sensitive_geo_list,'more_today_s_geo');
	}else{
		today_sensitive_geo.innerHTML = '暂无敏感地点信息';
		$('#moreSgeo').css('display','none');
        Draw_more_today('','more_today_s_geo');
	}
	/*
    var tag_vector = ip_data.tag_vector;
    for (var n = 0; n < tag_vector.length; n++){
        var tag_name = tag_vector[n][0];
        if (tag_vector[n][1]){
            var tag_value = tag_vector[n][1] + '(' + tag_vector[n][2].split('\t').pop() + ')';
        }
        else{
            var tag_value = '暂无数据';
        }
        global_tag_vector.push([tag_name, tag_value]);
    }
    //var div_name = ['daily_ip','weekly_ip'];
    var this_desc = '';
	
    //console.log.log(ip_data.description);
	
    if (ip_data.description[1].length != 0){
        this_desc += "<span>" + ip_data.description[0] + "</span><span style='color:red;'>" + ip_data.description[1][0] + '(' + ip_data.description[1][1].split('\t').pop() +')' + "</span>"; //description
    }
    if (ip_data.description[3].length != 0){
        this_desc += "<span>" + ip_data.description[2] + "</span><span style='color:red;'>" + ip_data.description[3][0] + '(' + ip_data.description[3][1].split('\t').pop() + ')' + "</span>"; //description
    }
    if (ip_data.description[5]){
        this_desc += "<span>" + ip_data.description[4] + "</span><span style='color:red;'>" + ip_data.description[5][0] + '(' + ip_data.description[5][1].split('\t').pop() + ')' + "</span>"; //description
    }
    $('#ip_desc').html(this_desc + '。');
	
    if(this_desc == ''){
        $('#ip_conclusion').css('display', 'none');
    }
	*/
    var location_geo;
    // ip table
    $('#total_IP_rank').empty();
	var countDay =7;
	var now = new Date();
    weekstr = [];
	for(var i=0;i<countDay;i++){
		var date = new Date(now.getTime() - (7-i) * 24 * 3600 * 1000);
		var year = date.getFullYear();
		var month = date.getMonth() + 1;
		var day = date.getDate();
		var daystr = month+'月'+day+'日';
		weekstr.push(daystr);
	}
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
	html += '<tr><th style="text-align:center">时间</th>';
    html += '<th style="text-align:center">'+weekstr[0]+'</th>';
    html += '<th style="text-align:center">'+weekstr[1]+'</th>';
    html += '<th style="text-align:center">'+weekstr[2]+'</th>';
    html += '<th style="text-align:center">'+weekstr[3]+'</th>';
    html += '<th style="text-align:center">'+weekstr[4]+'</th>';
    html += '<th style="text-align:center">'+weekstr[5]+'</th>';
    html += '<th style="text-align:center">'+weekstr[6]+'</th>';
    html += '</tr>';
    html += '<tr><th style="text-align:center">一周IP</th>';
    for(var i=0;i<ip_data.ip_week_list.length;i++){
		if(ip_data.ip_week_list[i][0]){
			html += '<th style="text-align:center"><a style="cursor:pointer;" data-toggle="modal" data-target="#moredailyip'+i+'" >'+ip_data.ip_week_list[i][0][0]+'</a></th>';
			//console.log(ip_data.ip_week_list[i].length,ip_data.ip_week_list[i]);
			Draw_more(ip_data.ip_week_list[i],'daily_ip'+i);
		}else{
			html += '<th style="text-align:center">-</th>';
		}
	}
	html += '<tr><th style="text-align:center">一周位置</th>';
    for(var i=0;i<ip_data.geo_week_list.length;i++){
		if(ip_data.geo_week_list[i][0]){
			html += '<th style="text-align:center"><a style="cursor:pointer;" data-toggle="modal" data-target="#moredailygeo'+i+'" >'+ip_data.geo_week_list[i][0][0]+'</a></th>';
			//console.log(ip_data.geo_week_list[i].length,ip_data.geo_week_list[i]);
			Draw_more(ip_data.geo_week_list[i],'daily_geo'+i);
		}else{
			html += '<th style="text-align:center">-</th>';
		}
	}
	html += '<tr><th style="text-align:center">敏感IP</th>';
    for(var i=0;i<ip_data.sensitive_ip_week_list.length;i++){
		if(ip_data.sensitive_ip_week_list[i][0]){
			html += '<th style="text-align:center"><a style="cursor:pointer;" data-toggle="modal" data-target="#moredailyip'+i+'" >'+ip_data.sensitive_ip_week_list[i][0][0]+'</a></th>';
			Draw_more(ip_data.sensitive_ip_week_list[i],'daily_s_ip'+i);
		}else{
			html += '<th style="text-align:center">-</th>';
		}
	}
	html += '<tr><th style="text-align:center">敏感位置</th>';
    for(var i=0;i<ip_data.sensitive_geo_week_list.length;i++){
		if(ip_data.sensitive_geo_week_list[i][0]){
			html += '<th style="text-align:center"><a style="cursor:pointer;" data-toggle="modal" data-target="#moredailygeo'+i+'" >'+ip_data.sensitive_geo_week_list[i][0][0]+'</a></th>';
			Draw_more(ip_data.sensitive_geo_week_list[i],"daily_s_geo" + i);
		}else{
			html += '<th style="text-align:center">-</th>';
		}
	}
    html += '</tr>';
    html += '</table>'; 
    $('#total_IP_rank').append(html);
	/*
    // span ip
    $('#span_ip').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">时段</th><th style="text-align:center;">00:00-04:00</th>';
    html += '<th style="text-align:center">04:00-08:00</th>';
    html += '<th style="text-align:center">08:00-12:00</th>';
    html += '<th style="text-align:center">12:00-16:00</th>';
    html += '<th style="text-align:center">16:00-20:00</th>';
    html += '<th style="text-align:center">20:00-24:00</th>';
    html += '<th style="text-align:center"></th></tr>';

    location_geo = ip_data.day_ip;
    html += '<tr>';
    html += '<th style="text-align:center;">当日</th>';
    for (var i = 0; i < 6; i++) {
       var s = i.toString();
       html += '<th style="text-align:center">';
       if ((i in location_geo) && (location_geo[i].length != 0)){
           top_two = location_geo[i];
           span_daily_map_data.push(['时段'+(i+1),location_geo[i][0][2]]);
           for (var j = 0;j < top_two.length;j++){
               var ip_city = top_two[j][2].split('\t').pop();
               html += top_two[j][0] + '<br>(' + ip_city + ',' + top_two[j][1] + ')';
           }
       }
       else{
           html += '-';
       }
       html += '</th>';
    };
    //html += '<th style="text-align:center"><a id="span_daily_ip_map" href="#map">查看地图</a></th>';
    html += '</tr>';
    location_geo = ip_data.week_ip;
    html += '<tr>';
    html += '<th style="text-align:center;">最近7天</th>';
    for (var i = 0; i < 6; i++) {
       var s = i.toString();
       html += '<th style="text-align:center">';
       if ((i in location_geo) && (location_geo[i].length != 0)){
           top_two = location_geo[i];
           span_weekly_map_data.push(['时段'+(i+1),location_geo[i][0][2]]);
           for (var j = 0;j < top_two.length;j++){
               var ip_city = top_two[j][2].split('\t').pop();
               html += top_two[j][0] + '<br>(' + ip_city + ',' + top_two[j][1] + ')';
           }
       }
       else{
           html += '-';
       }
       html += '</th>';
    };
    //html += '<th style="text-align:center"><a href="#map" id="span_weekly_ip_map">查看地图</a></th>';
    html += '</tr>';
    html += '</table>'; 
    $('#span_ip').append(html);
		*/

}

function draw_online_pattern(data){
    if ('sort_result' in data){
        var online_data = data.sort_result;
        $('#online_pattern').empty();
        var html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">上网方式</th><th style="text-align:center">微博数</th></tr>';
        for (var i = 0; i < online_data.length; i++) {
           var s = i.toString();
           var m = i + 1;
           html += '<tr><th style="text-align:center">' + m;
           html += '</th><th style="text-align:center">' + online_data[i][0];
           html += '</th><th style="text-align:center">' + online_data[i][1];
           html +='</th></tr>';
        };
        html += '</table>'; 
        $('#online_pattern').append(html);                  
    }
}

function draw_activeness_chart(data){
	//console.log.log(data);
    //$('#activeness_desc').html("<span>" + data.description[0] + "</span><span style='color:red;'>" + data.description[1] + "</span>。");
    //global_tag_vector.push(['活跃类型', data.tag_vector]);
    var data_time = [];
    var data_count = [];
    var timeline = data.time_list;
    //var activeness = data.ave_activeness;
    for (var i = 0;i < timeline.length;i++){
        data_time.push(timeline[i][1]);
    }
    for (var i = 0;i < timeline.length;i++){
        data_count.push(parseFloat(timeline[i][2].toFixed(2)));
    }

    $('#activeness').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '',
			align:'left',
			fontSize:'20',
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
            categories: data_time,
            labels:{
                rotation: 0,
                step: 1,
                x:0,
                y:30,
            }
        },
        yAxis: {
			min:0,
            title: {
                text: '活跃度',
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '',
            xDateFormat: '%H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'center',
            verticalAlign: 'top',
            borderWidth: 0
        },
        series: [{
            name:'活跃度',
            data: data_count,
        }]
    });
}

function get_unix_time(dateStr){
    var newstr = dateStr.replace(/-/g,'/'); 
    var date =  new Date(newstr); 
    var time_str = date.getTime().toString();
    return time_str.substr(0, 10);
}

function activity_load(){
    bind_time_option();
    var url = '/attribute/location/?uid='+ uid + '&time_type=week';
    person_call_ajax_request(url, geo_track);
    //var url = '/attribute/online_pattern/?uid='+uid;
    //person_call_ajax_request(url,draw_online_pattern);
    var url = '/attribute/activeness_trend/?uid=' + uid;
    person_call_ajax_request(url, draw_activeness_chart);
}


function Draw_more(data,div){
	console.log(data);
	$('#'+div).empty();
	if(div=='daily_ip0'||div=='daily_ip1'||div=='daily_ip2'||div=='daily_ip3'||div=='daily_ip4'||div=='daily_ip5'||div=='daily_ip6'||div=='daily_s_ip0'||div=='daily_s_ip1'||div=='daily_s_ip2'||div=='daily_s_ip3'||div=='daily_s_ip4'||div=='daily_s_ip5'||div=='daily_s_ip6'){
		var words ='IP';
	}else{
		var words = '位置';
	}
	var html = '';
	html += '<table class="table table-striped table-bordered" >';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">'+words+'</th><th style="text-align:center">频数</th></tr>';
    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        var m = i + 1;
        html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data[i][0] +  '</th><th style="text-align:center">' + data[i][1] + '</th></tr>';
    };
    html += '</table>'; 
    $('#'+ div).append(html);
}
function Draw_more_today(data,div){
    console.log(data,div);
	$('#'+div).empty();
	if(div =='more_today_ip'|| div =='more_today_s_ip'){
		var words = 'IP';
	}else{
		var words = '位置';
	}
	var html = '';
	if(data.length==0){
		$('#'+ div).append("暂无数据");
	}else{
	html += '<table class="table table-striped table-bordered" >';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">'+words+'</th><th style="text-align:center">频数</th></tr>';
    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        var m = i + 1;
        html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data[i][0] +  '</th><th style="text-align:center">' + data[i][1] + '</th></tr>';
    };
    html += '</table>'; 
    $('#'+ div).append(html);
	}
}


var global_time_type = 'day';
var pre_time = choose_time_for_mode();
pre_time.setHours(0,0,0);
pre_time=Math.floor(pre_time.getTime()/1000) - 24*60*60;

var url = '/attribute/activity/?uid=' + uid;
var global_active_data;
tag_call_ajax_request(url, active_chart);

var daily_map_data = new Array();
var weekly_map_data = new Array();
var span_daily_map_data = new Array();
var span_weekly_map_data = new Array();
var url = '/attribute/ip/?uid=' + uid;
tag_call_ajax_request(url, draw_daily_ip_table);

