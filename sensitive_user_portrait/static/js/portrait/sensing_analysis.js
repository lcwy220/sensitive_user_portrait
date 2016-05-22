function call_sync_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: true,
      success:callback
    });
}


function sensing_participate_table (head, data, div_name) {
    $('#'+div_name).empty();
	var html = '';
    if(data.length==0){
    html += '无已入库用户';
    }else{
	html += '<table id="'+div_name+'_table"  class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
		html += '<th style="text-align:center">'+head[i]+'</th>';
	}
	html += '</tr></thead>';
	html += '<tbody>';
	for(var i=0; i<data.length; i++){
		html += '<tr>';
		html += '<td style="text-align:center;vertical-align:middle;"><a class="undlin" target="_blank" href="/index/personal/?uid=' + data[i][0] + '">'+ data[i][0] + '</a></td>';
		if(data[i][1]=='unknown'){
            var u_name=data[i][0]
        }else{
            var u_name=data[i][1]
        }
        html += '<td style="text-align:center;vertical-align:middle;">' + u_name + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
		html += '<td  style="text-align:center;vertical-align:middle;">'+data[i][4][0]+'</td>';
		html += '</td><td style="text-align:center;vertical-align:middle;">' + data[i][5].toFixed(2) + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][6].toFixed(2) + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][7].toFixed(2) + '</td>';
		html += '</tr>';
	}
	html += '</tbody></table>';
}
	$('#'+div_name).append(html);
}

function sen_out_table (head, data, div_name) {
    $('#'+div_name).empty();
    var html = '';
    if(data.length==0){
        html += '无未入库用户';
    }else{
        html += '<div><table id="'+div_name+'_table"  class="table table-bordered table-striped table-condensed datatable">';
        html += '<thead><tr>';
        for(var i=0; i<head.length; i++){
            html += '<th style="text-align:center">'+head[i]+'</th>';
        }
        html += '<th style="text-align:center"><input name="sen_out_choose_all" id="sen_out_choose_all" type="checkbox" value="" onclick="sen_out_choose_all()" /></th>'
        html += '</tr></thead>';
        html += '<tbody>';
    for(var i=0; i<data.length; i++){
        html += '<tr>';
        html += '<td style="text-align:center;vertical-align:middle;"><a class="undlin" target="_blank" href="http://weibo.com/u/' + data[i][0] + '">'+ data[i][0] + '</a></td>';
		if(data[i][1]=='unknown'){
            var u_name=data[i][0]
        }else{
            var u_name=data[i][1]
        }
        html += '<td style="text-align:center;vertical-align:middle;">' + u_name + '</td>';
        if(data[i][2].length==0){
            html += '<td style="text-align:center;vertical-align:middle;">--</td>';
        }else{
            html += '<td style="text-align:center;vertical-align:middle;">' + data[i][2] + '</td>';}
            html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
            html += '<td style="text-align:center;vertical-align:middle;">' + data[i][4] + '</td>';
             html += '<td style="text-align:center;vertical-align:middle;"><input name="sen_out_list_option" class="search_result_option" type="checkbox" value="' + data[i][0] + '" /></td>';
            html += '</tr>';
    }
    html += '</tbody></table></div>';
    html += ' <button class="portrait_button" style="margin-left:10px;width:80px;height:40px;float:right;" name="sen_out_list_button" id="sen_out_list_button" title="推荐入库"  onclick="sen_out_list_button();">选择入库</button>';
    }
    $('#'+div_name).append(html);
}

function page_icon(page,count,eq, div_name){
	var ul_html = "";
	for(var i=page; i<=count; i++){
		ul_html += "<li>"+i+"</li>";
	}
	$("#"+div_name+" #pageGro ul").empty();
	$("#"+div_name+" #pageGro ul").append(ul_html);
	$("#"+div_name+" #pageGro ul li").eq(eq).addClass("on");
}

function sen_out_choose_all(){
  $('input[name="sen_out_list_option"]').prop('checked', $("#sen_out_choose_all").prop('checked'));
}
//上一页
function pageUp(pageNum, pageCount, div_name){
	switch(pageNum){
		case 1:
		break;
		case 2:
			page_icon(1,5,0, div_name);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,2, div_name);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,3, div_name);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,1, div_name);
		break;
	}
}

//下一页
function pageDown(pageNum,pageCount, div_name){
	switch(pageNum){
		case 1:
			page_icon(1,5,1, div_name);
		break;
		case 2:
			page_icon(1,5,2, div_name);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,4, div_name);
		break;
		case pageCount:
		break;
		default:
			page_icon(pageNum-2,pageNum+2,3, div_name);
		break;
	}
}

//点击跳转页面
function pageGroup(pageNum,pageCount, div_name){
	switch(pageNum){
		case 1:
			page_icon(1,5,0, div_name);
		break;
		case 2:
			page_icon(1,5,1, div_name);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,3, div_name);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,4, div_name);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,2, div_name);
		break;
	}
}

function Draw_num_weibo (data){
    console.log(data);
	Draw_group_weibo(data, 'num_weibo', 'num_related_weibo');
    $('#num_weibo').css("display", 'block');
}

function Draw_sen_weibo (data){
    Draw_group_weibo(data, 'num_weibo', 'sen_num_related_weibo');
    $('#num_weibo').css("display", 'block');
}
function Draw_mood_weibo (data){
	Draw_group_weibo(data, 'mood_weibo', 'mood_related_weibo');
    $('#mood_weibo').css("display", 'block');
}

function Draw_sensi_weibo (data){
	Draw_group_weibo(data, 'sensi_weibo', 'sensi_related_weibo');
    $('#sensi_weibo').css("display", 'block');
}

function Draw_group_weibo(data, div_name, sub_div_name){
    var page_num = 5;
    $('#' + sub_div_name).css('height', 'auto');
    if (data.length < page_num) {
        $('#'+ div_name + ' #pageGro').css('display', 'none');
    	if (data.length == 0) {
    		$('#' + sub_div_name).empty();
    		$('#' + sub_div_name).append('暂无相关微博')
    	}else{
	        page_num = data.length;
	        page_group_weibo( 0, page_num, data, div_name, sub_div_name);
    	}
      }
      else {
        $('#' + sub_div_name).css('height', '315px');
        $('#'+ div_name + ' #pageGro').css('display', 'block');
          page_group_weibo( 0, page_num, data, div_name, sub_div_name);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        page_icon(1,5,0, div_name);
    }else{
        page_icon(1,pageCount,0, div_name);
    }
    
    $("#"+div_name+" #pageGro li").live("click", function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount, div_name);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      var page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        page_group_weibo(start_row,end_row,data, div_name, sub_div_name);
    });

    $("#"+div_name+" #pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());
            pageUp(pageNum,pageCount, div_name);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index > 0){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index-1).addClass("on");
            }
        }
      var page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data, div_name, sub_div_name);
    });
    

    $("#" + div_name + " #pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());

            pageDown(pageNum,pageCount, div_name);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index+1).addClass("on");
            }
        }
      var page = parseInt($("#"+div_name+" #pageGro li.on").html()) 
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data, div_name, sub_div_name);
    });
}
function page_group_weibo(start_row, end_row, data, div_name, sub_div_name){
    var highlight_words = []; //高亮词数组
    weibo_num = end_row - start_row;
    $('#'+ sub_div_name).empty();
    var html = "";
    html += '<div id="weibo_list" class="weibo_list weibo_list_height scrolls tang-scrollpanel" style="margin:0;">';
	html += '<div id="content_control_height" class="tang-scrollpanel-wrapper" style="margin:0;">';
	html += '<div class="tang-scrollpanel-content" style="margin:0;">';
	html += '<ul>';
    for (var i = start_row; i < end_row; i += 1){
        var s = (i+1).toString();
        var weibo = data[i][0]
        var uid = weibo[0];
        var name = weibo[1];
        var date = weibo[5];
        var text = weibo[3];
        var geo = weibo[6];
        var attitude = weibo[4];
        var weibo_type = weibo[7];
        var weibo_type_s = '';
        if(weibo_type == 1){
            weibo_type_s = '原创';

        }
        if(weibo_type == 2){
            weibo_type_s = '评论';

        }
        if(weibo_type == 3){
            weibo_type_s = '转发';

        }
        var re_count = weibo[8];
        var com_count = weibo[9];
        var mid=weibo[13];
        var profile_image_url = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        if (!geo){
           geo = '未知';
        }
        geo = geo.split('&').join('\t');
        if (name == 'unknown'){
            name = '未知';
        }
        if (attitude == 0){
        	var attitude_s = '中性';
        };
        if (attitude == 1){
        	attitude_s = '积极';
        };
        if (attitude == 2){
        	attitude_s = '悲伤';
        };
        if (attitude == 3){
        	attitude_s = '焦虑';
        }
        if (attitude == 4){
        	attitude_s = '悲伤';
        }
        if (attitude == 5){
        	attitude_s = '厌恶';
        }
        if (attitude == 6){
        	attitude_s = '消极其他';
        }
        if (attitude == 7){
        	attitude_s = '消极';
        }
        var user_link = 'http://weibo.com/u/' + uid;
        if(data[i].length==1){
        html += '<li class="item" style="float:left;padding:5px 0;">';
        html += '<div class="weibo_detail">';
        html += '<p style="text-align:left;margin-bottom:0;">' +s +'、【'+weibo_type_s+'】-&nbsp;昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo + ')&nbsp;&nbsp;';
        html += '发布内容:&nbsp;&nbsp;<span class="weibo_text">' + text + '</span></p>';
        html += '</div>';
        html += '<div class="weibo_info"style="width:100%">';
        html += '<div class="weibo_pz" style="margin:0px;padding-left:10px;width:80%;float:left">';
        html += '<div class="m">';
        html += '<u>' + date + '</u>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + user_link + '">用户</a>&nbsp;&nbsp;';
        if(re_count == undefined){
        html += '</div></div><div style="width:20%;float:left"><span style="color:#666">&nbsp;</span>';
        }else{
        html += '</div></div><div style="width:20%;float:left"><span style="color:#666">转发数(' + re_count +')&nbsp;&nbsp;|&nbsp;&nbsp;评论数('+com_count+')</span>';
       }// html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</li>';
    }else{
        html += '<li class="item">';
        html += '<div class="weibo_detail">';
        html += '<p style="text-align:left;margin-bottom:0;">' +s +'、【'+weibo_type_s+'】-&nbsp;昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo + ')&nbsp;&nbsp;';
        html += '发布内容:&nbsp;&nbsp;<span class="weibo_text">' + text + '</span></p>';
        html += '</div>';
        html += '<div class="weibo_info"style="width:100%">';
        html += '<div class="weibo_pz" style="margin:0px;padding:left:10px;width:80%;float:left">';
        html += '<div class="m">';
        html += '<u>' + date + '</u>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + user_link + '">用户详情</a>&nbsp;&nbsp;-<a href="javascript:void(0)" id="show_sim" value="'+mid+'">相似微博</a>';
        html += '</div></div><div style="width:20%;float:left"><span style="color:#666">转发数(' + re_count +')&nbsp;&nbsp;评论数('+com_count+')</span>';
        html += '</div>';
        html += '</div>';
        html += '</li>';
        html += '<div id="'+mid+'" style="display:none;margin-left:20px">';
        for( var j=1;j<data[i].length;j++){
        var weibo = data[i][j];
        var uid = weibo[0];
        var name = weibo[1];
        var date = weibo[5];
        var text = weibo[3];
        var geo = weibo[6];
        var attitude = weibo[4];
        var weibo_type = weibo[7];
        var weibo_type_s = '';
        if(weibo_type == 1){
            weibo_type_s = '原创';

        }
        if(weibo_type == 2){
            weibo_type_s = '评论';

        }
        if(weibo_type == 3){
            weibo_type_s = '转发';

        }
        var re_count = weibo[8];
        var com_count = weibo[9];
        var profile_image_url = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        if (!geo){
           geo = '未知';
        }
        geo = geo.split('&').join('\t');
        if (name == 'unknown'){
            name = '未知';
        }
        if (attitude == 0){
        	var attitude_s = '中性';
        };
        if (attitude == 1){
        	attitude_s = '积极';
        };
        if (attitude == 2){
        	attitude_s = '悲伤';
        };
        if (attitude == 3){
        	attitude_s = '焦虑';
        }
        if (attitude == 4){
        	attitude_s = '悲伤';
        }
        if (attitude == 5){
        	attitude_s = '厌恶';
        }
        if (attitude == 6){
        	attitude_s = '消极其他';
        }
        if (attitude == 7){
        	attitude_s = '消极';
        }
        var user_link = 'http://weibo.com/u/' + uid;
        html += '<li class="item">';
        html += '<div class="weibo_detail">';
        html += '<p style="text-align:left;margin-bottom:0;width:1000px">【'+weibo_type_s+'】-&nbsp;昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo + ')&nbsp;&nbsp;';
        html += '发布内容:&nbsp;&nbsp;<span class="weibo_text">' + text + '</span></p>';
        html += '</div>';
        html += '<div class="weibo_info"style="width:100%">';
        html += '<div class="weibo_pz" style="margin:0px;padding:left:10px;width:80%;float:left">';
        html += '<div class="m">';
        html += '<u>' + date + '</u>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + user_link + '">用户详情</a>&nbsp;&nbsp;';
        html += '</div></div><div style="width:20%;float:left"><span style="color:#666">转发数(' + re_count +')&nbsp;&nbsp;评论数('+com_count+')</span>';
        html += '</div>';
        html += '</div>';
        html += '</li>';

        }
        html += '</div>'
    }
    }
    html += '<div id="TANGRAM_54__slider" class="tang-ui tang-slider tang-slider-vtl" style="height: 100%;">';
    html += '<div id="TANGRAM_56__view" class="tang-view" style="width: 6px;">';
    html += '<div class="tang-content"><div id="TANGRAM_56__inner" class="tang-inner"><div id="TANGRAM_56__process" class="tang-process tang-process-undefined" style="height: 0px;"></div></div></div>';
    html += '<a id="TANGRAM_56__knob" href="javascript:;" class="tang-knob" style="top: 0%; left: 0px;"></a></div>';
    html += '<div class="tang-corner tang-start" id="TANGRAM_54__arrowTop"></div><div class="tang-corner tang-last" id="TANGRAM_54__arrowBottom"></div></div>';

    html += '</ul>';
    html += '</div>';
    html += '</div>';
    html += '</div>';   
    html += '</div>'; 
    $('#'+sub_div_name).append(html);

mid_click();

}
function mid_click(){
    $('a[id^="show_sim"]').click(function(e){
    var mid=$(this).attr('value');
    $('#'+mid).css('display','block');
    
    });
}
mid_click();
function draw_sensi_line_charts(data, div_name, legend_data){
	var line1 = data[1];
	var line2 = data[2];
     if(data[0].length < 100){
         var zoom = true;
         var zoom_start = 0;
      }else{
          var zoom = true;
          var zoom_start = 100 - parseInt(100/data[0].length*100);
      }
	var myChart = echarts.init(document.getElementById(div_name)); 
	var option = { 
	    tooltip : {
	        trigger: 'axis',
	        show : true,
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
	        start : zoom_start
	    },
	    legend : {
	        data : legend_data,
	        x:'center'
	    },
	    grid: {
	        y2: 70
	    },
	    xAxis : [
	        {
	            data :data[0],
	            type : 'category',
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
	            name: legend_data[0],
	            type: 'line',
	            showAllSymbol : true,
               	symbolSize:3,
               	symbol: 'circle',	          
	            data: line1
	        },
	        {
	            name: legend_data[1],
	            type: 'line',
	            showAllSymbol : true,
	            symbolSize:3,
               	symbol: 'circle',
	            data: line2
	        }//,
	    ]
	};
	 require([
            'echarts'
        ],
        function(ec){
			var ecConfig = require('echarts/config');
			function eConsole(param) {
			    if (typeof param.seriesIndex != 'undefined') {			    
				    var timestamp2 = Date.parse(new Date(param.name));
					timestamp2 = timestamp2 / 1000;
				    sensi_click_time = timestamp2;
                    var sensi_index;
				    if (param.seriesIndex==0){
			    		sensi_index = 2;
			    	}else if(param.seriesIndex == 1){
			    		sensi_index = 3;
			    	}else if(param.seriesIndex == 2){
			    		sensi_index = 2;
			   		}
					//微博 or 感知	
					$('input[name="sensi_select"]').off('click').click(function(){
                        if($('input[name="sensi_select"]:checked').val()=='1'){ 
                            $('#sensi_related_weibo_event').css('display', 'block');
                            $('#sensi_related_weibo_all').css('display', 'none');
                        }else{
                            $('#sensi_related_weibo_event').css('display', 'none');
                            $('#sensi_related_weibo_all').css('display', 'block');
                        }
					});	
					
				}
			}

		myChart.on(ecConfig.EVENT.CLICK, eConsole);
	});

	// 为echarts对象加载数据 
    myChart.setOption(option); 

}

function draw_mood_line_charts(data, div_name, legend_data){
	var line1 = data[1];
	var line2 = data[2];
	var line3 = data[3];
     if(data[0].length < 100){
         var zoom = true;
         var zoom_start = 0;
      }else{
          var zoom = true;
          var zoom_start = 100 - parseInt(100/data[0].length*100);
      }
	var myChart = echarts.init(document.getElementById(div_name)); 
	var option = {  
        tooltip : {
	        trigger: 'axis',
	        show : true,
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
	        start : zoom_start
	    },
	    legend : {
	        data : legend_data,
	        x:'center'
	    },
	    grid: {
	        y2: 70
	    },
	    xAxis : [
	        {
	            data :data[0],
	            type : 'category',
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
	            name: legend_data[0],
	            type: 'line',
	            showAllSymbol : true,
	            symbolSize:3,
               	symbol: 'circle',
	            clickable: true,	          
	            data: line1
	        },
	        {
	            name: legend_data[1],
	            type: 'line',
	            showAllSymbol : true,
	            symbolSize:3,
               	symbol: 'circle',
	            data: line2
	        },
	        {
	            name: legend_data[2],
	            type: 'line',
	            showAllSymbol : true,
	            symbolSize:3,
               	symbol: 'circle',
	            data: line3
	        },
	    ]
	};
	 require([
            'echarts'
        ],
        function(ec){
			var ecConfig = require('echarts/config');
			function eConsole(param) {
			    if (typeof param.seriesIndex != 'undefined') {			    
				    var timestamp2 = Date.parse(new Date(param.name));
					timestamp2 = timestamp2 / 1000;
				    mood_click_time = timestamp2;
				    var index_type;
				    if (param.seriesIndex==0){
			    		index_type = 6;
			    	}else if(param.seriesIndex==1){
			    		index_type = 5;
			   		}else if(param.seriesIndex == 2){
			   			index_type = 4;
			   		};
				}
			}
		
		myChart.on(ecConfig.EVENT.CLICK, eConsole);
	});

	// 为echarts对象加载数据 
    myChart.setOption(option); 

}

function draw_num_line_charts(data, div_name, legend_data){
    var line1 = data[1];
	var line2 = data[2];
     if(data[0].length < 100){
         var zoom = true;
         var zoom_start = 0;
      }else{
          var zoom = true;
          var zoom_start = 100 - parseInt(100/data[0].length*100);
      }
	var myChart = echarts.init(document.getElementById(div_name)); 
	var option = {  
           tooltip : {
	        trigger: 'axis',
	        show : true,
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
	        start:zoom_start,
	    },
	    legend : {
	        data : legend_data,
	        x:'center'
	    },
	    grid: {
	        y2: 70
	    },
	    xAxis : [
	        {
	            data :data[0],
	            type : 'category',
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
	            name: legend_data[0],
	            type: 'line',
	            showAllSymbol : true,
	            symbolSize:3,
               	symbol: 'circle',
	            data: line1
	        },
	        {
	            name: legend_data[1],
	            type: 'line',
	            symbolSize:3,
               	symbol: 'circle',
	            showAllSymbol : true,
	            data: line2
	         }//,
	    ]
	};
	 require([
            'echarts'
        ],
        function(ec){
			var ecConfig = require('echarts/config');
			function eConsole(param) {
			    var timestamp2 = Date.parse(new Date(param.name));
				timestamp2 = timestamp2 / 1000;
			    num_click_time = timestamp2;
			    num_index = param.seriesIndex
			    var index_type;
                if (param.seriesIndex== 0){
			    	index_type = 0
			    };
                if(param.seriesIndex == 1){
                    index_type = 1
                };

                var num_line_url = '/social_sensing/get_text_detail/?task_name=' + task_name + '&ts=' + num_click_time + '&text_type='+index_type+'&user='+sensing_user;
                console.log(num_line_url);
                call_sync_ajax_request(num_line_url, Draw_num_weibo);
  
			}
		myChart.on(ecConfig.EVENT.CLICK, eConsole);
	});

	// 为echarts对象加载数据 
    myChart.setOption(option);
}

function sen_out_list_button(){
  var cur_uids = []
  var noneflag = true;
  $('input[name="sen_out_list_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
      if($(this).parent().prev().prev().prev().prev().text()=='未知'){
        noneflag = false;
      }
  });
  var recommend_date0 = choose_time_for_mode();    // choose_time_for_mode().format('yyyy-MM-dd');
  recommend_date0.setDate(recommend_date0.getDate()-1);
  var recommend_date = recommend_date0.format('yyyy-MM-dd');
  if(noneflag==false){
    alert('ID未知用户不能推荐入库！');
  }else{
  if (cur_uids.length == 0){
    alert("请选择至少一个用户！");
  }  else{
    var compute_url = '/recommentation/identify_in/?submit_user='+sensing_user+'&date='+recommend_date+'&uid_list='+cur_uids;
    call_sync_ajax_request(compute_url, confirm_ok);
  }
}
}
function confirm_ok(data){
  if(data)
    alert('操作成功！');
}
function show_warning_time(div_name, data){
	$('#' + div_name).empty();	
	var html = '';
	for(var i=0;i<data.length;i++){
		html += '<span style="width:150px;margin:10px;font-size:14px;">' + data[i][0] + '</span>';
		if(i%3 == 2){
			html += '<br>';
		}
	}
		$('#' + div_name).append(html);	
}

function deal_point_col(data, index){
	var data_list = new Array();
	for(var i=0;i<data.length; i++){
		var data_dict = {};
		data_dict.name = data[i][0];
		data_dict.xAxis=data[i][0];
		data_dict.yAxis= data[i][index];
		if(data[i][index] != 0){
			data_list.push(data_dict);
		}
	}
	return data_list;

}

function deal_point(data){
	var data_list = new Array();
	for(var i=0;i<data.length; i++){
		var data_dict = {};
		data_dict.name = data[i][0];
		data_dict.xAxis=data[i][0];
		data_dict.yAxis= data[i][1];
		data_list.push(data_dict);
	}
	return data_list;

}

function show_warning_time_all(div_name, data){

	$('#' + div_name).empty();	
	var html = '';
	for(var i=0;i<data.length;i++){
		html += '<span style="width:150px;margin:10px;font-size:14px;">' + data[i] + '</span>';
		if(i%3 == 2){
			html += '<br>';
		}
	}
		$('#' + div_name).append(html);	
}

//高亮显示文本
  
	// 格式化关键词 
	function formatKeyword(content, keyword) 
	{ 
	    keyword = keyword.replace(/(^\s*)|(\s*$)/g, ""); 
	    if(keyword == '') 
	        return content; 
	    var reg = new RegExp('('+keyword+')', 'gi'); 
	    return content.replace(reg, '<span style="color:red"><b>$1</b></span>'); 
	} 
	 
	// 重绘内容区域 
	function refreshContent(div_name, contentID, keywords) 
	{ 
		var count_key = 0;

		$('#' + div_name +' .' + contentID).each(function(){
			var content = $(this).text() //document.getElementById(contentID).innerHTML; 
		    for(var i = 0; i < keywords[count_key].length; i ++) 
		    { 
		        var strKey = keywords[count_key][i].toString(); 
		        var arrKey = strKey.split(','); 
		        for(var j = 0; j < arrKey.length; j ++) 
		        { 
		            var key = arrKey[j]; 
		            content = formatKeyword(content, key); 
		        } 
		    } 
		    $(this).empty();
		    $(this).append(content);
		    count_key += 1;
		});

	} 

var num_legend = ['原创', '转发'];
var sensi_legend = [ '转发', '评论'];
//{name:'重合点', icon :'image://../../static/img/arrow.png'}];
var mood_legend = ['消极','中性', '积极'];
function social_sensing_all(data){
    console.log(data);

    var num_line_data = new Array();
    num_line_data[0]= data.time_series;
    num_line_data[1] = data.origin_weibo_list;
    num_line_data[2] = data.retweeted_weibo_list;
    draw_num_line_charts(num_line_data, 'num_line_charts', num_legend);

   var timestamp2 = Date.parse(new Date(data.time_series[data.time_series.length-1]));
   timestamp2 = timestamp2 / 1000;
   num_click_time = timestamp2;
   var num_line_url = '/social_sensing/get_text_detail/?task_name=' + task_name + '&ts=' + num_click_time + '&text_type=0&user='+sensing_user;
    call_sync_ajax_request(num_line_url, Draw_num_weibo);
    $('#num_related_weibo_all').css('display', 'block');
   
     $('#num_related_weibo_all').css('display', 'block');
     $('#select_style_order').css('display', 'block');
    participate_head=['用户ID','昵称','领域','话题','重要度','影响力','活跃度']
    var out_head=['用户ID','昵称','注册地','微博数','粉丝数'];
    var user_detail = new Array();
    user_detail = data.important_user_detail;
    var out_user =data.out_portrait_user_detail;
    sensing_participate_table(participate_head,user_detail,"sensing_participate_table");
    sen_out_table(out_head,out_user,"out_participate_table");
	//传感器模态框数据
	//备注信息
	var remark_info = data.warning_conclusion;
	$('#remark_info').empty();
	if(remark_info==undefined){
    $('#remark_info').append('无');
    }else{
    $('#remark_info').append(remark_info);
    }
}




function sensing_keywords_table_all(data){
	var keywords_head=['序号','关键词','频数'];
	sensing_keywords_table(keywords_head, data.slice(0, 10),"sensing_keywords_table");
	sensing_keywords_table(keywords_head,data,"modal_keywords_table");
}

var num_click_time;
var num_index;
var mood_click_time;
var mood_index;
var sensi_click_time;
var sensi_index;
user='admin';
$('#sensing_task_name').append(task_name);
var sensing_url = '';
sensing_url += '/social_sensing/get_warning_detail/?task_name='+task_name+'&user='+sensing_user+'&ts='+ts;
console.log(sensing_url);
call_sync_ajax_request(sensing_url, social_sensing_all);
