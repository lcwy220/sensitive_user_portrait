
var myDate = new Date();
var hh = myDate.getHours();
var mm =myDate.getMinutes();
var count_mm = Math.floor(mm/15);
var show_mm = count_mm * 15;
if(show_mm==0){
	show_mm = '00';
}
var show_time = hh.toString() + ':' + show_mm.toString();

function call_sync_ajax_request(url, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: true,
      success:callback
    });
}

//展示微博
function Draw_get_top_weibo(data, div_name){
    var html = '';
    $('#' + div_name).css('height',350);
    $('#' + div_name).css('overflow-y','auto');
    document.getElementById(div_name).style.border = "1px solid #77ACF4";
    $('#' + div_name).css('border-radius', 5);
    $('#' + div_name).empty();
    //console.log(div_name);
    if(data.length == 0){
        html += "<div style='margin-left:10px;width:100%;height:100px;'>用户未发布>任何微博</div>";
    }else{
        html += '<div id="weibo_list" class="weibo_list weibo_list_height scrolls tang-scrollpanel" style="margin:0;">';
        html += '<div id="content_control_height" class="tang-scrollpanel-wrapper" style="margin:0;">';
        html += '<div class="tang-scrollpanel-content" style="margin:0;">';
        html += '<ul>';
        for(var i=0;i<data.length;i++){
            s = (i+1).toString();
            var weibo = data[i]
            //var mid = weibo[0];
            var uid = weibo[0];
            var name = weibo[9];
            if(name == 'unknown'){
                name = uid;
            }
            var date = weibo[5];
            var text = weibo[2];
            var geo = weibo[6];
            var reposts_count = weibo[7];
            var comments_count = weibo[8];
            var sentiment_dict ={'0':'中性', '1':'积极', '2':'生气', '3':'焦虑', '4':'悲伤', '5':'厌恶', '6':'消极其他', '7':'消极'}
            var type_list = ['原创','评论','转发']
            if (geo == null){
                geo = '未知';
            }else{
                geo = geo.toString().split('&');
                if(geo.length <3){
                    var  geo_after = geo.join(' ');
                };
                if(geo.length >2){
                    geo = geo.slice(0, 4);
                    var geo_after = geo.join(' ');
                }
            }
            var weibo_link = weibo[10];
            var user_link = 'http://weibo.com/u/' + uid;
            html += '<li class="item">';
            html += '<div class="weibo_detail" style="width:100%">';
            html += '<p style="text-align:left;margin-bottom:0;margin-left:10px;">' +s +'、</span>昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo_after + ')&nbsp;&nbsp;发布内容：&nbsp;&nbsp;' + text + '</p>';
            html += '<div class="weibo_info" style="width:100%;margin-bottom:10px;">';
            html += '<div class="weibo_pz" style="margin-left:10px;">';
            //html += '<div id="topweibo_mid" class="hidden">'+mid+'</div>';
            html += '<div style="float:right;margin-right:5px;">';
            html += '<span class="retweet_count">转发数(' + reposts_count + ')</span>&nbsp;&nbsp;|&nbsp;&nbsp;';
            html += '<span class="retweet_count">评论数(' + comments_count + ')</span>&nbsp;&nbsp;';
            html += '</div>';
            html += '<div class="m">';
            html += '<u>' + date + '</u>&nbsp;-&nbsp;';
            html += '<a target="_blank" href="' + weibo_link + '">微博</a>&nbsp;-&nbsp;';
            html += '<a target="_blank" href="' + user_link + '">用户</a>';

            //html += type_list[weibo[3]-1] + '微博&nbsp;-&nbsp;';
            //html += sentiment_dict[weibo[4]];
            // html += '<a target="_blank" href="' + repost_tree_link + '">&nbsp;-&nbsp;转发树</a>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            html += '</li>';
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
    }
    $('#'+div_name).append(html);
}

function user_recom_in_modal(){
    var cur_uids = []
    var noneflag = true;
    $('input[name="user_out_check"]:checked').each(function(){
    //console.log($(this).attr('value'))
        cur_uids.push($(this).attr('value'));
        if($(this).attr('value') == 'undefined'){
            noneflag = false;
        }
    });
    var recommend_date0 = choose_time_for_mode();    // choose_time_for_mode().format('yyyy-MM-dd');
    recommend_date0.setDate(recommend_date0.getDate());
    var recommend_date = recommend_date0.format('yyyy-MM-dd');
    if(noneflag==false){
        alert('ID未知用户不能推荐入库！');
    }else{
        if (cur_uids.length == 0){
            alert("请选择至少一个用户！");
        }
        else{
            var compute_url = '/recommentation/identify_in/?submit_user='+username+'&date='+recommend_date+'&uid_list='+cur_uids;
            console.log(compute_url);
            call_sync_ajax_request(compute_url, confirm_ok);
        }
    }
}

function confirm_ok(data){
    if(data){
        alert('操作成功！');
        //window.location.reload();
    }else{
        alert('入库失败，请重试')
    }
}

function user_rank_timepicker(str){
	//var date_time = str.split(' ');
    var dates = str.split('/');
    var yy = parseInt(dates[0]);
    var mm = parseInt(dates[1]) - 1;
    var dd = parseInt(dates[2]);
    //var times = date_time[1].split(':');
    //var hh = parseInt(times[0]);
    //var minute = parseInt(times[1]);
    var final_date = new Date();
    final_date.setFullYear(yy,mm,dd);
    final_date.setHours(0,0);
    final_date = Math.floor(final_date.getTime()/1000); 
    console.log(final_date);
    return final_date;
}

function rank_task_status (data) {
	var data = data.data;
	//console.log(data);
	if (data.length == 0){
		$('#task_status').empty();
		var html = '<div style="text-align: center;background-color: #cccccc;">暂无任务</div>'
		$('#task_status').append(html);
	}else{
		var sort_scope = data.sort_scope;
		$('#task_status').empty();

		var html = '';
		html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
		html += '<thead>';
        html += '<th style="width:100px;text-align:center;">关键词</th>'
        html += '<th style="width:100px;text-align:center;">排序范围</th>'
        html += '<th style="width:180px;text-align:center;">时间范围</th>'
        html += '<th style="width:125px;text-align:center;">提交时间</th>'
        html += '<th style="width:100px;text-align:center;">排序指标</th>'
        html += '<th style="width:80px;text-align:center;">任务状态</th>'
        html += '<th style="width:50px;text-align:center;">操作</th>'
		html += '</thead>'
		for(var i=0;i<data.length;i++){
            sort_scope = scope_dict[data[i][8]];
            sort_norm = norm_dict[data[i][7]];
            var delete_this = '<span style="display:none;">'+data[i][9]+'</span><span class="delete_this"><b><u class="delete_key_result" style="cursor:pointer;">删除</u></b></span>';
            if(data[i][6] == -1){
                var status = '正在计算';
            }else if(data[i][6]== 1){
                var status = '<span><b><u class="show_key_result" style="cursor:pointer;">计算完成</u></b></span>';
            }else if(data[i][6] == 0){
                var status = '尚未计算';
            }
            html += '<tr>';
            html += '<td style="text-align:center;">'+data[i][1]+'</td>';
            html += '<td style="text-align:center;">'+sort_scope+'</td>';
            html += '<td style="text-align:center;">'+data[i][2]+' 至 '+data[i][3]+'</td>';
            html += '<td style="text-align:center;">'+data[i][5]+'</td>';
            html += '<td style="text-align:center;">'+sort_norm+'</td>';
            html += '<td style="text-align:center;"><span style="display:none;">'+data[i][9]+'</span>'+'<span style="display:none;">'+data[i][8]+'</span>'+status+'</td>';
            html += '<td style="text-align:center;">'+delete_this+'</td>';
            html += '</tr>';
		}
		html += '</table>';
		$('#task_status').append(html);
	}
}

function task_status (data) {
    var data = data.data;
    //console.log(data);
    if (data.length == 0){
        $('#task_status').empty();
        var html = '<div style="text-align: center;margin-top:30px;background-color: #cccccc;">暂无任务</div>'
        $('#task_status').append(html);
    }else{
        var sort_scope = data.sort_scope;
        $('#task_status').empty();

        var html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:900px;">';
        html += '<thead>';
        html += '<th style="width:100px;text-align:center;">关键词</th>'
        html += '<th style="width:100px;text-align:center;">排序范围</th>'
        html += '<th style="width:180px;text-align:center;">时间范围</th>'
        html += '<th style="width:125px;text-align:center;">提交时间</th>'
        html += '<th style="width:100px;text-align:center;">排序指标</th>'
        html += '<th style="width:80px;text-align:center;">任务状态</th>'
        html += '<th style="width:50px;text-align:center;">操作</th>'
        html += '</thead>'
        for(var i=0;i<data.length;i++){
            sort_scope = scope_dict[data[i].sort_scope];
            sort_norm = norm_dict[data[i].sort_norm];
            var delete_this = '<span style="display:none;">'+data[i].search_id+'</span><span class="delete_this"><b><u class="delete_key_result" style="cursor:pointer;">删除</u></b></span>';
            if(data[i].status == -1){
                var status = '正在计算';
            }else if(data[i].status == 1){
                var status = '<span><b><u class="show_key_result" style="cursor:pointer;">计算完成</u></b></span>';
            }else if(data[i].status == 0){
                var status = '尚未计算';

            }
            //console.log(data[i][1]);
            html += '<tr>';
            //html += '<td style="text-align:center;">'+data[i][1]+'</td>';
            html += '<tr>';
            html += '<td style="text-align:center;">'+data[i].keyword+'</td>';
            html += '<td style="text-align:center;">'+sort_scope+'</td>';
            html += '<td style="text-align:center;">'+data[i].start_time+' 至 '+data[i].end_time+'</td>';
            html += '<td style="text-align:center;">'+data[i].create_time+'</td>';
            html += '<td style="text-align:center;">'+sort_norm+'</td>';
            html += '<td style="text-align:center;"><span style="display:none;">'+data[i].search_id+'</span>'+'<span style="display:none;">'+data[i].sort_scope+'</span>'+status+'</td>';
            html += '<td style="text-align:center;">'+delete_this+'</td>';
            html += '</tr>';
        }
        html += '</table>';
        $('#task_status').append(html);
    }
}

function draw_all_rank_table(data){
	//console.log(data);
	var data = data;
		if(data == 0){
			$('#result_rank_table').empty();
			var html = '<div style="width: 900px;margin-left: 30px;text-align: center;font-size: 16px;background-color: #cccccc;margin-bottom: 30px;">暂无数据</div>';
				$('#result_rank_table').append(html);
		}else{
				var html = '';
                html += '<table id="rank_table" class="table table-bordered table-striped table-condensed datatable" style="margin-left:30px;width:900px;">';
                //html += '<table id="rank_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;" width:100%>';
                html += '<thead><th style="width:65px;text-align:center;">排名</th>';
                html += '<th style="text-align:center;">用户ID</th>';
                html += '<th style="text-align:center;">昵称</th>';
                html += '<th style="text-align:center;">是否入库</th>';
                html += '<th style="text-align:center;width:100px;">注册地</th>';
                html += '<th style="text-align:center;">粉丝数</th>';
                html += '<th style="text-align:center;">微博数</th>';
                html += '<th style="text-align:center;">影响力</th>';
                html += '<th style="text-align:center;">言论敏感度</th>';
                html += '<th style="min-width:40px;text-align:center;">入库</th>';
                html += '</thead>';
                for(var i=0;i<data.length;i++){
                    var uid = data[i].uid;
                    var uname = data[i].uname;
                    if(uname == 'unknown' || uname == null){
                        uname = uid;
                    }
                    var is_warehousing = '';
                    if(data[i].is_warehousing == true){
                        var user_url = '/index/personal/?uid='+uid;
                        is_warehousing = '是';
                    }else{
                        var user_url = '/index/personal_out/?uid='+uid;
                        is_warehousing = '否'
                    };
                    var location = data[i].location;
                    if(location == null){
                        location = '未知'
                    }
                    var fans = data[i].fans;
                    if(fans == null || fans == undefined){
                        fans = ''
                    }
                    if(data[i].weibo_count == undefined || data[i].weibo_count == null ){
                        var weibo_num = '';
                    }else{
                        var weibo_num = data[i].weibo_count;
                    };
                    var influcence = data[i].bci;
                    if(influcence == null || influcence == undefined){
                        influcence = '';
                    }else{
                        influcence = influcence.toFixed(2);
                    };
                    var sensitive = data[i].sen;
                    if(sensitive == null || sensitive == undefined){
                        sensitive = '';
                    }else{
                        sensitive = sensitive.toFixed(2);
                    };
                    html += '<tr>';
                    html += '<td style="text-align:center;">'+(i+1)+'</td>';
                    html += '<td style="text-align:center;"><a href='+user_url+ ' target="_blank">'+uid+'</a></td>';
                    //html += '<td style="text-align:center;"><a href="/index/personal/?uid='+uid+'" target="_blank">'+uid+'</a></td>';
                    html += '<td style="text-align:center;">'+uname+'</a></td>';
                    html += '<td style="text-align:center;">'+is_warehousing+'</td>';
                    html += '<td style="text-align:center;">'+location+'</td>';
                    html += '<td style="text-align:center;">'+fans+'</td>';
                    html += '<td style="text-align:center;">'+weibo_num+'</td>';
                    html += '<td style="text-align:center;">'+influcence+'</td>';
                    html += '<td style="text-align:center;">'+sensitive+'</td>';
                    if(data[i].is_warehousing == false){
                        html += '<td style="width:20px;text-align:center;"><input name="user_out_check" id="user_out_check" type="checkbox" value='+ uid +'></td>';
                    }else{
                        html += '<td style="text-align:center;">-</td>';
                    }
                    html += '</tr>';
				}
				html += '</table>';
				$('#result_rank_table').empty();
				$('#result_rank_table').append(html);
                $('#rank_table').dataTable({
                    "aoColumnDefs": [ {"sWidth": "5em", "aTargets":[0]}, {"sWidth": "7em", "aTargets":[3]}, {"sWidth": "10em", "aTargets":[2]},{"bSortable": false, "aTargets":[9]}],
                    "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
                    "sPaginationType": "bootstrap",
                    //"aoColumnDefs":[ {"bSortable": false, "aTargets":[1]}],
                    "oLanguage": {
                        "sLengthMenu": "每页 _MENU_ 条 ",
                    }
                });
		}
}

function draw_rank_table(data){
	if(data.length == 0){
		$('#result_rank_table').empty();
		var html = '<div style="text-align: center;font-size: 16px;background-color: #cccccc;margin-bottom: 30px;width: 900px;margin-left: 30px;">暂无数据</div>';
		$('#result_rank_table').append(html);

	}else{
		$('#result_rank_table').empty();
		var html = '';
		html += '<table id="rank_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
		html += '<thead><th style="text-align:center;">排名</th>';
		html += '<th style="text-align:center;">用户ID</th>';
		html += '<th style="text-align:center;">昵称</th>';
		html += '<th style="text-align:center;">注册地</th>';
		html += '<th style="text-align:center;">领域</th>';//其实是话题
		html += '<th style="text-align:center;">身份</th>';//其实是领域
		html += '<th style="text-align:center;">身份敏感度</th>';
		html += '<th style="text-align:center;">活跃度</th>';
		html += '<th style="text-align:center;">影响力</th>';
		html += '<th style="text-align:center;">言论敏感度</th></thead>';
		for(var i=0;i<data.length;i++){

			var uid = data[i].uid;
			var uname = data[i].uname;
			if(uname == 'unknown'){
				uname = uid
			}
			var location = data[i].location;
			if(location == 'unknown'){
				location = '未知'
			}
			var topic = '';
			topic = data[i].topic.split('&').join(',');
			var domain = data[i].domain;
			var imp = data[i].imp;
			if(imp == null){
				imp = 0;
			}
			var active = data[i].act;
			if(active == null){
				active = 0;
			}

			//var weibo_num = data[i].weibo_num;
			var influcence = data[i].bci;
			if(influcence == null){
				influcence = 0;
			}
			var sensi = data[i].sen;
			if(data[i].sen == null){
				sensi = 0;
			}

            html += '<tr>';
            html += '<td style="text-align:center;">'+(i+1)+'</td>';
            html += '<td style="text-align:center;"><a href="/index/personal/?uid='+uid+'" target="_blank">'+uid+'</a></td>';
            html += '<td style="text-align:center;">'+uname+'</td>';
            html += '<td style="text-align:center;">'+location+'</td>';
            html += '<td style="text-align:center;" title='+topic+'>'+topic.substr(0,20)+'...'+'</td>';
            html += '<td style="text-align:center;">'+domain+'</td>';
            html += '<td style="text-align:center;">'+imp.toFixed(2) +'</td>';
            html += '<td style="text-align:center;">'+active.toFixed(2)+'</td>';
            html += '<td style="text-align:center;">'+influcence.toFixed(2)+'</td>';
            html += '<td style="text-align:center;">'+sensi.toFixed(2)+'</td>';
            html += '</tr>';
        }
		html += '</table>';
		$('#result_rank_table').append(html);
        $('#rank_table').dataTable({
            "aoColumnDefs": [ {"sWidth": "4.5em" ,"aTargets":[0]},{"sWidth": "4.5em" ,"aTargets":[1]}, {"sWidth": "6em" ,"aTargets":[2]},{"sWidth": "6em" ,"aTargets":[3]},{"sWidth": "7em" ,"aTargets":[4]},{"sWidth": "5em" ,"aTargets":[5]},{"sWidth": "6.6em" ,"aTargets":[6]},{"sWidth": "4em" ,"aTargets":[7]},{"sWidth": "6em" ,"aTargets":[8]},{"sWidth": "6em" ,"aTargets":[9]}],
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "bootstrap",
            //"aoColumnDefs":[ {"bSortable": false, "aTargets":[1]}],
            "oLanguage": {
                "sLengthMenu": "每页 _MENU_ 条 ",
            }
        });
	}
}


//排序范围选择
$('#range_choose').change(function(){
	$('#range_choose_detail').empty();
	//库内-不限
	if($('#range_choose').val() == 'in_nolimit') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select  id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

        $('#time_choose').empty();
        var time_html = '';
        time_html += '<input name="time_range" type="radio" value="1" checked="checked"> 昨日';
        time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 7天';
        time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 30日';
        $('#time_choose').append(time_html);
    }
	//库内-领域
	if($('#range_choose').val() == 'in_limit_domain') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

        $('#time_choose').empty();
        var time_html = '';
        time_html += '<input name="time_range" type="radio" value="1" checked="checked"> 昨日';
        time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 7天';
        time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 30日';
        $('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose_detail_2">';
		html += '<option value="境内机构">境内机构</option>'
		html += '<option value="境外机构">境外机构</option>'
		html += '<option value="民间组织">民间组织</option>'
		html += '<option value="境外媒体">境外媒体</option>'
		html += '<option value="活跃人士">活跃人士</option>'
		html += '<option value="商业人士">商业人士</option>'
		html += '<option value="媒体人士">媒体人士</option>'
		html += '<option value="高校">高校</option>'
		html += '<option value="草根">草根</option>'
		html += '<option value="媒体">媒体</option>'
		html += '<option value="法律机构及人士">法律机构及人士</option>'
		html += '<option value="政府机构及人士">政府机构及人士</option>'
		html += '<option value="其他">其他</option>'
		html += '</select>'
	};
	//库内-话题
	if($('#range_choose').val() == 'in_limit_topic') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

        $('#time_choose').empty();
        var time_html = '';
        time_html += '<input name="time_range" type="radio" value="1" checked="checked"> 昨日';
        time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;"> 7天';
        time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;"> 30日';
        $('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose_detail_2">';
		html += '<option value="科技类">科技类</option>';
		html += '<option value="经济类">经济类</option>';
		html += '<option value="教育类">教育类</option>';
		html += '<option value="军事类">军事类</option>';
		html += '<option value="民生类_健康">民生类_健康</option>';
		html += '<option value="民生类_住房">民生类_住房</option>';
		html += '<option value="民生类_环保">民生类_环保</option>';
		html += '<option value="民生类_就业">民生类_就业</option>';
		html += '<option value="民生类_社会保障">民生类_社会保障</option>';
		html += '<option value="民生类_交通">民生类_交通</option>';
		html += '<option value="民生类_法律">民生类_法律</option>';
		html += '<option value="政治类_外交">政治类_外交</option>';
		html += '<option value="政治类_暴恐">政治类_暴恐</option>';
		html += '<option value="政治类_地区和平">政治类_地区和平</option>';
		html += '<option value="政治类_反腐">政治类_反腐</option>';
		html += '<option value="政治类_宗教">政治类_宗教</option>';
		html += '<option value="文体类_娱乐">文体类_娱乐</option>';
		html += '<option value="文体类_体育">文体类_体育</option>';
		html += '<option value="其他类">其他类</option>';
		html += '</select>';
	};
	//库内-关键词（修改时间范围）
	if($('#range_choose').val() == 'in_limit_keyword') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);
		date_init();

        var html = '';
        html += '<input id="keyword_hashtag" type="text" class="form-control" style="width:275px;height:25px;" placeholder="请输入关键词，多个词用空格分开">';
    };
	//hashtag库内
	if($('#range_choose').val() == 'in_limit_hashtag') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);
		date_init();

		var html = '';
        html += '<input id="keyword_hashtag" type="text" class="form-control" style="width:275px;height:25px;" placeholder="请输入微话题，多个话题用空格分开">';
    };
	//地理位置-库内
	if($('#range_choose').val() == 'in_limit_geo') {
		$('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="imp">身份敏感度</option>';
		sort_select += '<option value="act">活跃度</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="imp_change">突发重要度变动</option>';
		sort_select += '<option value="act_change">突发活跃度变动</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

        $('#time_choose').empty();
        var time_html = '';
        time_html += '<input name="time_range" type="radio" value="1" checked="checked"> 昨日';
        time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;">7天';
        time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;">30日';
        $('#time_choose').append(time_html);

		var html = '';
		html += '<select id="range_choose_detail_2">';
		html += '<option value="北京">北京</option>';
		html += '<option value="天津">天津</option>';
		html += '<option value="上海">上海</option>';
		html += '<option value="重庆">重庆</option>';
		html += '<option value="广东">广东省</option>';
		html += '<option value="浙江">浙江省</option>';
		html += '<option value="江苏">江苏省</option>';
		html += '<option value="福建">福建省</option>';
		html += '<option value="湖南">湖南省</option>';
		html += '<option value="湖北">湖北省</option>';
		html += '<option value="山东">山东省</option>';
		html += '<option value="辽宁">辽宁省</option>';
		html += '<option value="吉林">吉林省</option>';
		html += '<option value="云南">云南省</option>';
		html += '<option value="四川">四川省</option>';
		html += '<option value="安徽">安徽省</option>';
		html += '<option value="江西">江西省</option>';
		html += '<option value="黑龙江">黑龙江省</option>';
		html += '<option value="河北">河北省</option>';
		html += '<option value="陕西">陕西省</option>';
		html += '<option value="海南">海南省</option>';
		html += '<option value="河南">河南省</option>';
		html += '<option value="山西">山西省</option>';
		html += '<option value="内蒙古">内蒙古</option>';
		html += '<option value="广西">广西</option>';
		html += '<option value="贵州">贵州省</option>';
		html += '<option value="宁夏">宁夏</option>';
		html += '<option value="青海">青海省</option>';
		html += '<option value="新疆">新疆</option>';
		html += '<option value="西藏">西藏</option>';
		html += '<option value="甘肃">甘肃省</option>';
		html += '<option value="台湾">台湾省</option>';
		html += '<option value="香港">香港</option>';
		html += '<option value="澳门">澳门</option>';
		//html += '<option value="海外">海外</option>';
		html += '</select>';
	};
	//全网-all
	if($('#range_choose').val() == 'all_nolimit') {
        if($("input[name='time_range']:checked").val() == '0'){
            $('#sort_select').empty();
            var sort_select = '';
            sort_select += '<select id="sort_select_2">';
            sort_select += '<option value="retweeted">转发量</option>';
            sort_select += '<option value="comment">评论量</option>';
            sort_select += '</select>';
            $('#sort_select').append(sort_select);

        }else{
            $('#sort_select').empty();
            var sort_select = '';
            sort_select += '<select id="sort_select_2">';
            sort_select += '<option value="fans">粉丝数</option>';
            sort_select += '<option value="weibo_num">微博数</option>';
            sort_select += '<option value="bci">影响力</option>';
            sort_select += '<option value="ses">言论敏感度</option>';
            sort_select += '<option value="bci_change">突发影响力变动</option>';
            sort_select += '<option value="ses_change">突发敏感度变动</option>';
            sort_select += '</select>';
            $('#sort_select').append(sort_select);
        }

        $('#time_choose').empty();
        var time_html = '';
        time_html += '<span style="float:left; margin-right:15px;">';
        time_html += '<input name="time_range" type="radio" value="0" checked="checked"> 当日'
        time_html += '</span>';
        time_html += '<select id="time_choose_intime" style="display:block;float:left;margin-right:15px;">';
        time_html += '</select>';
        time_html += '<input name="time_range" type="radio" value="1">昨日';
        time_html += '<input name="time_range" type="radio" value="7" style="margin-left:20px;">7天';
        time_html += '<input name="time_range" type="radio" value="30" style="margin-left:20px;">30日';
        $('#time_choose').append(time_html);

	}
	//全网-关键词
	if($('#range_choose').val() == 'all_limit_keyword') {
		var html = '';
	    html += '<input id="keyword_hashtag" type="text" class="form-control" style="width:275px;height:25px;" placeholder="请输入关键词，多个词用英文逗号分开">';
	    $('#sort_select').empty();
		var sort_select = '';
		sort_select += '<select id="sort_select_2">';
		sort_select += '<option value="fans">粉丝数</option>';
		sort_select += '<option value="weibo_num">微博数</option>';
		sort_select += '<option value="bci">影响力</option>';
		sort_select += '<option value="ses">言论敏感度</option>';
		sort_select += '<option value="bci_change">突发影响力变动</option>';
		sort_select += '<option value="ses_change">突发敏感度变动</option>';
		sort_select += '</select>';
		$('#sort_select').append(sort_select);

		$('#time_choose').empty();
	    var time_html = '';
	    time_html += '<input id="weibo_from" type="text" class="form-control" style="width:145px; display:inline-block;height:25px;">&nbsp;-&nbsp;';
		time_html += '<input id="weibo_to" type="text" class="form-control" style="width:145px; display:inline-block;height:25px">';	    
		$('#time_choose').append(time_html);
		date_init();

		var html = '';
	    html += '<input id="keyword_hashtag" type="text" class="form-control" style="width:275px;height:25px;" placeholder="请输入关键词，多个词用英文逗号分开">';

	};
	$('#range_choose_detail').append(html);
});

//筛选条件初始化时间
function date_init(){
	var date = choose_time_for_mode();
	//console.log(date)
	date.setHours(0,0,0,0);
	var max_date = date.format('yyyy/MM/dd');
	var current_date = date.format('yyyy/MM/dd');
	var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24;
	var min_date_ms = new Date()
	min_date_ms.setTime(from_date_time*1000);
	var from_date = min_date_ms.format('yyyy/MM/dd');
        if(global_test_mode==0){
        $('#time_choose #weibo_from').datetimepicker({value:from_date,step:1440,format:'Y/m/d',timepicker:false});
        $('#time_choose #weibo_to').datetimepicker({value:from_date,step:1440,format:'Y/m/d',timepicker:false});
        $('#user_time_choose_modal #user_weibo_from_modal').datetimepicker({value:from_date,step:1440,format:'Y/m/d',timepicker:false});
        $('#user_time_choose_modal #user_weibo_to_modal').datetimepicker({value:from_date,step:1440,format:'Y/m/d',timepicker:false});
        $('#user_search_date #user_weibo_modal').datetimepicker({value:from_date,step:1440,format:'Y/m/d',timepicker:false});

    }else{
        $('#time_choose #weibo_from').datetimepicker({value:from_date,step:1440,minDate:'-1970/01/30',format:'Y/m/d',timepicker:false,maxDate:'+1970/01/01'});
        $('#time_choose #weibo_to').datetimepicker({value:from_date,step:1440,minDate:'-1970/01/30',format:'Y/m/d',timepicker:false,maxDate:'+1970/01/01'});
        $('#user_time_choose_modal #user_weibo_from_modal').datetimepicker({value:from_date,step:1440,minDate:'-1970/01/30',maxDate:'+1970/01/01',format:'Y/m/d',timepicker:false});
        $('#user_time_choose_modal #user_weibo_to_modal').datetimepicker({value:from_date,step:1440,minDate:'-1970/01/30',maxDate:'+1970/01/01',format:'Y/m/d',timepicker:false});
        $('#user_search_date #user_weibo_modal').datetimepicker({value:from_date,step:1440,minDate:'-1970/01/30',maxDate:'+1970/01/01',format:'Y/m/d',timepicker:false});

    }
    var real_date = new Date();
    real_date = real_date.format('yyyy/MM/dd');
    //console.log(real_date);
    $('#user_search_date #user_weibo_modal').datetimepicker({value:real_date,step:1440,format:'Y/m/d',timepicker:false});
}
$('#user_time_checkbox').click(function(){
    if($(this).is(':checked')){
        $('#user_time_choose_modal #user_weibo_from_modal').attr('disabled',false);
        $('#user_time_choose_modal #user_weibo_to_modal').attr('disabled',false);
    }
    else{
        $('#user_time_choose_modal #user_weibo_from_modal').attr('disabled', true);
        $('#user_time_choose_modal #user_weibo_to_modal').attr('disabled', true);
    }
});
$('#user_time_checkbox_submit').click(function(){
    if($(this).is(':checked')){
        $('#user_search_date #user_weibo_modal').attr('disabled',false);
    }
    else{
        $('#user_search_date #user_weibo_modal').attr('disabled', true);
    }
});
function submit_offline(data){
    //console.log(data)
    if(data.flag == true){
        alert('提交成功！已添加至离线任务');
        var task_url = '/user_rank/search_task/?username='+username;
        console.log(task_url)
        call_sync_ajax_request(task_url, task_status);
    }else if(data == 'more than limit'){
        alert('提交任务数超过用户限制，请等待结果计算完成后提交新任务！');
    }else{
        alert('添加失败，请重试！')
    }
}
function draw_key_rank(data){
    var num = data.number;
    $('#rec_num_range').empty();
    $('#rec_num_range').append(num);
    draw_key_rank_table(data);
    Draw_get_top_weibo(data.text_results, 'rank_weibo');
}

function draw_in_key_rank(data){
    var num = data.number;
    $('#rec_num_range').empty();
    $('#rec_num_range').append(num);
    draw_in_key_rank_table(data);
    Draw_get_top_weibo(data.text_results, 'rank_weibo');
}
function draw_key_rank_table(data){
    //console.log(data);
    if(data.length == 0){
        $('#result_rank_table').empty();
        var html = '<div style="width: 900px;margin-left: 30px;text-align: center;font-size: 16px;background-color: #cccccc;margin-bottom: 30px;">暂无数据</div>';
        $('#result_rank_table').append(html);
    }else{

        //结果分析默认值
        var sort_norm = data.sort_norm;
        var sort_scope = data.sort_scope;
        var key = data.keyword;
        var time_range = data.start_time + '至' +data.end_time;
        $('#rec_range').empty();
        $('#rec_rank_by').empty();
        $('#rec_time_range').empty();
        $('#rec_range').append(scope_dict[sort_scope]);
        $('#rec_range').append('-'+key);

        $('#rec_rank_by').append(norm_dict[sort_norm]);
        $('#rec_time_range').append(time_range);

        var data = data.result;
        draw_all_rank_table(data);
    }
}
function draw_in_key_rank_table(data){
    //console.log(data);
    if(data.length == 0){
        $('#result_rank_table').empty();
        var html = '<div style="text-align: center;font-size: 16px;background-color: #cccccc;margin-bottom: 30px;width: 900px;margin-left: 30px;">暂无数据</div>';
        $('#result_rank_table').append(html);
    }else{
        var scope_dict ={'all_limit_keyword':'全网-按关键词','in_limit_keyword':'库内-按关键词','in_limit_hashtag':'库内-按微话题'}
        var norm_dict ={'weibo_num': '微博数','fans': '粉丝数','bci': '影响力','bci_change':'突发影响力变动','ses':'言论敏感度','ses_change':'突发敏感度变动','imp':'>身份敏感度','imp_change':'突发重要度变动','act':'活跃度','act_change':'突发活跃度变动'}
        var sort_norm = data.sort_norm;
        var sort_scope = data.sort_scope;
        var key = data.keyword;
        //console.log(sort_scope);
        //console.log('sort_norm',sort_norm);
        var time_range = data.start_time + '至' +data.end_time;

        $('#rec_range').empty();
        $('#rec_rank_by').empty();
        $('#rec_time_range').empty();
        $('#rec_range').append(scope_dict[sort_scope]);
        $('#rec_range').append('-'+key);
        $('#rec_rank_by').append(norm_dict[sort_norm]);
        $('#rec_time_range').append(time_range);

        var data = data.result;
        draw_rank_table(data);
    }
}
function del(data){
    if(data.flag == true){
        alert('删除成功！');
        var task_url = '/user_rank/search_task/?username='+username;
        call_sync_ajax_request(task_url, task_status);
    }else{
        alert('删除失败，请再试一次！');
    }
}


function temporal_rank_table(data){
    //console.log(data);
    $('#result_rank_table').empty();
    var html = '';
    html += '<table id="rank_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-left:30px;width:900px;">';
    html += '<thead><th style="text-align:center;">排名</th>';
    html += '<th style="text-align:center;">用户ID</th>';
    html += '<th style="text-align:center;">昵称</th>';
    html += '<th style="text-align:center;">是否入库</th>';
    html += '<th style="text-align:center;">注册地</th>';
    html += '<th style="text-align:center;">粉丝数</th>';
    html += '<th style="text-align:center;">微博数</th>';
    html += '<th style="text-align:center;">转发量</th>';
    html += '<th style="text-align:center;">评论量</th>';
    html += '<th style="min-width:40px;text-align:center;">入库</th></thead>';
    for(var i=0;i<data.length;i++){
        var uid = data[i][0];
        var uname = data[i][1];
       if(uname == ''){
            uname = data[i][0];
        }
        var sign_loca = data[i][3];
        if(sign_loca == ''){
            sign_loca = '未知'
        }
        if(data[i][7]==1){ //是否入库
            var user_url = '/index/personal/?uid='+uid;
            var ifin = '是';
        }else{
            var user_url = '/index/personal_out/?uid='+uid;
            var ifin = '否';
        }
        if(data[i][4]==''){//fans
            data[i][4]= '';
        }
        if(data[i][5]==''){//retweeted
            data[i][5]= '';
        }
        if(data[i][6]==''){//comment
            data[i][6]= '';
        }
        if(data[i][2]==''){//weibo
            data[i][2]= '';
        }

        html += '<tr>';
        html += '<td style="text-align:center;">'+(i+1)+'</td>';
        if(data[i][7]==1){
        html += '<td style="text-align:center;"><a href='+user_url+' target="_blank">'+uid+'</a></td>';}
        else{
        html += '<td style="text-align:center;"><a href='+user_url+' target="_blank">'+uid+'</a></td>';
        }
        html += '<td style="text-align:center;">'+uname+'</td>';
        html += '<td style="text-align:center;">'+ifin+'</td>';
        html += '<td style="text-align:center;">'+sign_loca+'</td>';
        html += '<td style="text-align:center;">'+data[i][4]+'</td>';
        html += '<td style="text-align:center;">'+data[i][2]+'</td>';
        html += '<td style="text-align:center;">'+data[i][5]+'</td>';
        html += '<td style="text-align:center;">'+data[i][6]+'</td>';
        if(data[i][7] == 0){
             html += '<th style="width:20px;text-align:center;"><input name="user_out_check" id="user_out_check" type="checkbox" value='+ uid +'></th>';
        }else{
             html += '<td style="text-align:center;">-</td>';
        }
        html += '</tr>';
    }
    html += '</table>';
    $('#result_rank_table').append(html);
    $('#rank_table').dataTable({
            "aoColumnDefs": [ {"sWidth": "5em", "aTargets":[0]}, {"sWidth": "7em", "aTargets":[3]}, {"sWidth": "10em", "aTargets":[2]},{"bSortable": false, "aTargets":[9]}],
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "bootstrap",
            //"aoColumnDefs":[ {"bSortable": false, "aTargets":[1]}],
            "oLanguage": {
                "sLengthMenu": "每页 _MENU_ 条 ",
            }
        });
    $('#recom_in').css('display','block');
}
function submit_rank(){
    $('#recom_in').css('display','none');
    var number_sort = $("input[name='sort_num_range']:checked").val();
    //console.log(number_sort);
    var s = [];
    var show_scope = $('#range_choose option:selected').text();
    var show_arg = $('#range_choose_detail_2 option:selected').text();
    var show_norm = $('#sort_select_2 option:selected').text();
    var keyword = $('#keyword_hashtag').val();
    var sort_scope = $('#range_choose option:selected').val();
    var sort_norm = $('#sort_select_2 option:selected').val();
    var arg = $('#range_choose_detail_2 option:selected').val();
    var day_select = $("input[name='time_range']:checked").val();
    //console.log(sort_scope);
    //console.log(day_select);
    //全网实时
    if(sort_scope=='all_nolimit' && day_select == '0'){
      // $('#task_zh').css('display','none');
    //  $('#task_status').css('display','none');
    //  $('#task_search_zh').css('display','none');

        $('#rec_range').empty();
        $('#rec_range').append($('#range_choose option:selected').text());
        $('#rec_rank_by').empty();
        $('#rec_rank_by').append($('#sort_select_2 option:selected').text());
        $('#rec_time_range').empty();
        $('#rec_num_range').empty();
        $('#rec_num_range').append(number_sort);

        var time_choose = document.getElementsByName('time_range_in');
        //console.log(time_choose)
        for(var i=0;i<time_choose.length;i++){
            if(time_choose[i].selected){
                var time_choose_val = time_choose[i].value;
                $('#rec_time_range').empty();
                //$('#rec_time_range').append('当日');
                if(time_choose_val==0){
                   $('#rec_time_range').append('当日最新排名');
                }
                if(time_choose_val==1){
                   $('#rec_time_range').append('00:00-06:00');
                }
                if(time_choose_val==2){
                    $('#rec_time_range').append('06:00-12:00');
                }
                if(time_choose_val==3){
                    $('#rec_time_range').append('12:00-18:00');
                }
                if(time_choose_val==4){
                    $('#rec_time_range').append('18:00-24:00');
                }
            }
        }
        $('#rec_time_range').append($('#time_choose checked:checked').text());
        if(time_choose_val*6 > hh){
            alert('当前选择的时间超出范围，请重新选择');
            $('#result_rank_table').empty();
        }
        else{
            var url = '/user_rank/temporal_rank/?task_type='+time_choose_val+'&sort='+sort_norm+'&number='+number_sort;
            $('#result_rank_table').empty()
            var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
            $('#result_rank_table').append(loading_html)
            call_sync_ajax_request(url, temporal_rank_table);
            console.log(url)
        }
    }
    else{
        if(keyword == ''){  //检查输入词是否为空
            alert('请输入关键词！');
        }else{
            if(keyword == undefined){  //没有输入的时候，更新表格及文字
                // var loading_html = '正在加载...请稍后';
                // console.log(loading_html);
                $('#result_rank_table').empty();
                // $('#result_rank_table').append(loading_html);
                var url = '/user_rank/user_sort/?username='+username+'&time='+day_select+'&sort_norm='+sort_norm+'&sort_scope='+sort_scope+'&number='+number_sort;
                $('#rec_range').empty();
                $('#rec_detail').empty();
                $('#rec_rank_by').empty();
                $('#rec_time_range').empty();
                $('#rec_range').append(show_scope);
                $('#rec_num_range').empty();
                $('#rec_num_range').append(number_sort);
                if(sort_scope != 'in_nolimit' && sort_scope != 'all_nolimit' ){  // 参数是可选的时候，加上详细条件
                    $('#rec_detail').append('-');
                    $('#rec_detail').append(show_arg);
                    url += '&arg='+arg;   //该参数为空时不传
                }
                $('#rec_rank_by').append(show_norm);
                if(day_select == "1"){
                    $('#rec_time_range').append('昨日');
                }
                if(day_select == "7"){
                    $('#rec_time_range').append('7天');
                }
                if(day_select == "30"){                
                    $('#rec_time_range').append('30日');
                }
                if(sort_scope == 'all_nolimit'){
                    url +='&all=True';
                    var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
                    $('#result_rank_table').append(loading_html)
                    $('#recom_in').css('display','none')
                    console.log(url);
                    call_sync_ajax_request(url, draw_all_rank_table);
                }else{
                    //alert('库内')
                    url += '&all=False';
                    var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
                    $('#result_rank_table').append(loading_html)
                    console.log(url);
                    call_sync_ajax_request(url, draw_rank_table);
                }
                //console.log(url);
            }else{ //输入参数的时候，更新任务状态表格
                $('#task_status').css('display', 'block');
                $('#task_search_zh').css('display', 'block');
                $('#open').css('display', 'none');
                $('#close_c').css('display', 'block');
                var keyword_array = [];
                var keyword_array = keyword.split(' ');
                //var keyword_string = keyword_array.join(',');
                var keyword_string = keyword.split(/\s+/g);
                var time_from =$('#time_choose #weibo_from').val().split('/').join('-');
                var time_to =$('#time_choose #weibo_to').val().split('/').join('-');
                var from_stamp = new Date($('#time_choose #weibo_from').val());
                var end_stamp = new Date($('#time_choose #weibo_to').val());
                if(from_stamp > end_stamp){
                    alert('起始时间不得大于终止时间！');
                    return false;
                }
                var url = '/user_rank/user_sort/?time=-1&username='+username+'&st='+time_from +'&et='+time_to+'&sort_norm='+sort_norm+'&sort_scope='+sort_scope+'&arg='+keyword_string+'&task_number='+task_num+'&number='+number_sort;
                console.log(url);
                if(sort_scope == 'all_limit_keyword'){
                    url +='&all=True';
                    //console.log(url);
                    call_sync_ajax_request(url, submit_offline);
                }else{
                    url += '&all=False';
                    //console.log(url);
                    call_sync_ajax_request(url, submit_offline);
                }
            }
        }
    }
}
//搜索任务提交
function user_search_task(){
    var submit_date = $('#user_weibo_modal').val().split('/').join('-');
    var start_date = $('#user_weibo_from_modal').val().split('/').join('-');
    var end_date = $('#user_weibo_to_modal').val().split('/').join('-');
    var submit_key = $('#user_search_key').val();
    var search_url = '/user_rank/task_sort/?user='+username;
    if(submit_key != ''){
        var keywords_string= submit_key.split(' ').join(',');
        search_url += '&keyword='+ keywords_string;
    }
    //var status = $('input[name="search_status"]:checked').val();
    var status = $('#search_status').val();
    //console.log(status);
    search_url += '&status=' +status;
    //var status= $('')
    if($('#user_time_checkbox').is(':checked')){
        search_url += '&start_time='+start_date+'&end_time='+end_date;
    };
    if($('#user_time_checkbox_submit').is(':checked')){
       search_url += '&submit_time='+submit_date;
    }
    console.log(search_url);
    call_sync_ajax_request(search_url, rank_task_status);
}
date_init();
//结果分析默认值
var username = $('#username').text();
var sort_scope = $('#range_choose option:selected').val();
var sort_norm_rank = $('#sort_select_2 option:selected').val();
//console.log(sort_norm_rank);
var arg = $('#range_choose_detail_2 option:selected').text();
var day_select = $("input[name='time_range']:checked").val();
$('#rec_range').append($('#range_choose option:selected').text());
// $('#rec_detail').append('：');
// $('#rec_detail').append($('#range_choose option:selected').text());
$('#rec_rank_by').append($('#sort_select_2 option:selected').text());
var day_select = $("input[name='time_range']:checked").val();
if(day_select == "0"){
    //$('#rec_time_range').append('当日')
    $('#rec_time_range').append($("#time_choose_intime option:selected").text());
    //console.log($("#time_choose_intime option:selected").text());
}
if(day_select == "1"){
    $('#rec_time_range').append('昨日')
}
if(day_select == "7"){
    $('#rec_time_range').append('7天')
}
if(day_select == "30"){
    $('#rec_time_range').append('30日')
}
var scope_dict ={'all_limit_keyword':'全网-按关键词','in_limit_keyword':'库内-按关>键词','in_limit_hashtag':'库内-按微话题'}
var norm_dict ={'weibo_num': '微博数','fans': '粉丝数','bci': '影响力','bci_change':'突发影响力变动','ses':'言论敏感度','ses_change':'突发敏感度变动','imp':'身份敏感>度','imp_change':'突发重要度变动','act':'活跃度','act_change':'突发活跃度变动'}

//任务状态
function task_status_fresh(){
    //console.log('fvf')
    var task_url = '/user_rank/search_task/?username='+username;
    call_sync_ajax_request(task_url, task_status);
}

task_status_fresh();
window.setInterval(task_status_fresh, 60000);

//画结果表格
//var rank_url = '/user_rank/user_sort/?username='+ username +'&time='+ day_select +'&sort_norm='+ sort_norm_rank +'&sort_scope='+ sort_scope+'&all=True';
var rank_url = '/user_rank/temporal_rank/?task_type='+day_select+'&sort='+sort_norm_rank+'&number=100';
console.log(rank_url);
var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
$('#result_rank_table').append(loading_html)
$('#recom_in').css('display','none');
$('.show_key_result').live('click', function(){
    //console.log('asdfsvg');
    // console.log($(this).parent().parent().prev().text());
    // console.log($(this).parent().parent().prev().prev().text());
    $('#recom_in').css('display','none');
    $('#rank_weibo').css('display','block');
    var search_id  = $(this).parent().parent().prev().prev().text();
    var sort_scope = $(this).parent().parent().prev().text();
    //console.log(sort_scope);
    var rank_range = $(this).parent().parent().parent().prev().prev().prev().text();
    var rank_by_key = $(this).parent().parent().parent().prev().prev().prev().prev().text();
    var rank_by = $(this).parent().parent().parent().prev().text();
    var time_range = $(this).parent().parent().parent().prev().prev().text();
    //console.log()
    var sort_scope = $(this).parent().parent().prev().text();
    $('#rec_range').empty();
    $('#rec_range').append(rank_range);
    $('#rec_range').append('-');
    $('#rec_range').append(rank_by_key);
    $('#rec_rank_by').empty();
    $('#rec_rank_by').append(rank_by);
    $('#rec_time_range').empty();
    $('#rec_time_range').append(time_range);
    var url='/user_rank/get_result/?search_id=' + search_id;
    console.log(url);
    //console.log(search_id);
    //call_sync_ajax_request(url, draw_key_rank_table);
    if(sort_scope == 'all_limit_keyword'){
        var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';    
        $('#result_rank_table').empty();
        $('#result_rank_table').append(loading_html);
        call_sync_ajax_request(url, draw_key_rank);
    }else{
        //alert('库内')
        var loading_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
        //console.log(loading_html);
        $('#result_rank_table').empty();
        $('#result_rank_table').append(loading_html);
        call_sync_ajax_request(url, draw_in_key_rank);
    }

});
call_sync_ajax_request(rank_url, temporal_rank_table);

$('.delete_this').live("click", function(){
    var a = confirm('确定要删除吗？');
    if (a == true){
        var url = '/user_rank/delete_task/?';
        var temp = $(this).prev().text();
        url = url + 'search_id=' + temp;
        console.log(url);
        //window.location.href = url;
        call_sync_ajax_request(url,del);
    }
});
$('#user_show_all_task').live('click', function(){
    var task_url = '/user_rank/search_task/?username='+username;
    call_sync_ajax_request(task_url, task_status);
    console.log(task_url)
});

//全网实时排名
$(function(){

$("input[name='time_range']").live('click',function(){
  if($('#range_choose option:selected').val() == 'all_nolimit'){
      if( $("input[name='time_range']:checked").val() == '0'){
          $("#time_choose_intime").css('display', 'block');
          $('#sort_select').empty();
          var sort_select = '';
          sort_select += '<select id="sort_select_2">';
          sort_select += '<option value="retweeted">转发量</option>';
          sort_select += '<option value="comment">评论量</option>';
          sort_select += '</select>';
          $('#sort_select').append(sort_select);
      }else{
          $("#time_choose_intime").css('display', 'none');
          $('#sort_select').empty();
          var sort_select = '';
          sort_select += '<select id="sort_select_2">';
          sort_select += '<option value="fans">粉丝数</option>';
          sort_select += '<option value="weibo_num">微博数</option>';
          sort_select += '<option value="bci">影响力</option>';
          sort_select += '<option value="ses">言论敏感度</option>';
          sort_select += '<option value="bci_change">突发影响力变动</option>';
          sort_select += '<option value="ses_change">突发敏感度变动</option>';
          sort_select += '</select>';
          $('#sort_select').append(sort_select);
      }
  }
});
    $('#range_choose').click(function(){
        $('#rank_weibo').css('display','none');
        var box = document.getElementById('range_choose').value;
        if(box=='in_nolimit' || box=='in_limit_keyword' ||box=='in_limit_hashtag'||box=='in_limit_domain'||box=='in_limit_topic'||box=='in_limit_geo'){
            $('#recom_in').css('display','none');
        }else{
            $('#recom_in').css('display','block');
        if(box == 'all_nolimit'){
            $('#time_choose_intime').empty();
            html = '';
            html = html + '<option name="time_range_in" style="background-color:#eee;"  value="0" >当日最新排名</option>';
            html = html + '<option name="time_range_in"  value="1"  style="margin-left:20px;">00:00 -06:00</option>';
            html = html + '<option name="time_range_in"  value="2"  style="margin-left:20px;">06:00 -12:00</option>';
            html = html + '<option name="time_range_in"  value="3"  style="margin-left:20px;">12:00 -18:00</option>';
            html = html + '<option name="time_range_in"  value="4"  style="margin-left:20px;">18:00 -24:00</option>';
            $('#time_choose_intime').append(html);
            /*$('#sort_select_2').empty();
            html = '';
            html += '<option value="retweeted" checked="checked">总转发数</option>';
            html += '<option value="comment" >总评论数</option>';
            $('#sort_select_2').append(html);*/
        }
    }
    });
})





