//词云
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
function call_ajax_request(url, callback){
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: false,
        success: callback
    });
}

function drawSensitiveCloud(div_name, c_title, cloud_data){
    var sensitiveChart = echarts.init(document.getElementById(div_name)); 
    function getCloudData(cloud_data){
        var chart_data = new Array();
        for (var i = 0;i < cloud_data.length;i++){
            var item = cloud_data[i];
            var item_dict =  {
                name: item[0],
                value: item[1] * 100,
                itemStyle: createRandomItemStyle()
            };
            chart_data.push(item_dict);
        }
        return chart_data;
    }
    
    var optionSensitive = {
        title: {
            text: c_title,
        },
        tooltip: {
            show: true
        },
        series: [{
            type: 'wordCloud',
            size: ['80%', '80%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            data: []
        }]
    };
    var chart_data = getCloudData(cloud_data);
    optionSensitive["series"][0]["data"] = chart_data;
    sensitiveChart.setOption(optionSensitive);
}	  
	  
//心理状态
function drawPsyState(){
    var psychologyChart = echarts.init(document.getElementById('psychologyState')); 
    var optionPsychology = {
        title: {
            text: '心理状态',
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        calculable : false,
        //     grid:{
        //     y:40
        // },
        series : [
            {
                name:'',
                type:'pie',
                selectedMode: 'single',
                radius : [0, 40],
                center: ['50%', '60%'],
                
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
                name:'心理状态',
                type:'pie',
                radius : [60, 80],
                center: ['50%', '60%'],
                
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
    psychologyChart.setOption(optionPsychology);  
}

//话题重点人物
function drawTopic(div_name, more_div_name, rank_data){
    $('#'+div_name).empty();
    var num = 0; 
    for (var key in rank_data){ 
        num ++;
        if (num > 6){
            break;
        }
        var html = '';
        html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:20px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
        html += '<span class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></span>';
        html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
        html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
        var topic_list = rank_data[key];
        var min_num = Math.min(4, topic_list.length);
        for(var i = 0;i < min_num; i++){
            var person_data = topic_list[i];
            var domain_top_username;
            if ((person_data[1] == 'unknown') || (person_data[1] == '0')){
                domain_top_username = '未知';
            }
            else{
                domain_top_username = person_data[1];
            }
            var domain_top_user_portrait;
            if (person_data[2] == 'unknown'){
                domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
            }
            else{
                domain_top_user_portrait = person_data[2];
            }
            html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + person_data[0] +'" title="' + domain_top_username +'">';
            html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';
	   }
       html += '</ul></div></div>';
       $('#'+div_name).append(html);
   }
   $('#'+more_div_name).empty();
   for (key in rank_data){ 
       var html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
       html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
       html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
       html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
        var topic_list = rank_data[key];
        var min_num = Math.min(4, topic_list.length);
       for(var i = 0;i < min_num; i++){
            var person_data = topic_list[i];
            var domain_top_username;
            if ((person_data[1] == 'unknown') || (person_data[1] == '0')){
                domain_top_username = '未知';
            }
            else{
                domain_top_username = person_data[1];
            }
            var domain_top_user_portrait;
            if (person_data[2] == 'unknown'){
                domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
            }
            else{
                domain_top_user_portrait = person_data[2];
            }
            html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + person_data[0] +'" title="' + domain_top_username +'">';
            html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';
        }
        html += '</ul></div></div>';
       $('#'+more_div_name).append(html);
   }
}
	
//画表格
function drawRank(div_name, cname, rank_data, more_div){
     $('#'+ div_name).empty();
        html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th>';
        html += '<th style="text-align:center">' + cname + '</th></tr>';
        var min_row = Math.min(5, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           var item = rank_data[i];
           var nickname;
           if ((item[1] == 'unknown') || (item[1] == '0')){
               nickname = '未知';
           }
           else{
               nickname = item[1];
           }
         html += '<tr><th style="text-align:center">' + m + '</th>';
         html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
         html += '<th style="text-align:center">' + item[2].toFixed(2) + '</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);  

	//更多
	$('#' + more_div).empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th>';
    html += '<th style="text-align:center">昵称</th><th style="text-align:center">' + cname + '</th></tr>';
	for (var i = 0; i < rank_data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       var item = rank_data[i];
       var nickname;
       if ((item[1] == 'unknown') || (item[1] == '0')){
           nickname = '未知';
       }
       else{
           nickname = item[1];
       }
       html += '<tr><th style="text-align:center">' + m + '</th>';
       html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
       html += '<th style="text-align:center">' + item[2].toFixed(2) + '</th></tr>';
    };
    html += '</table>'; 
    $('#' + more_div).append(html);                  
}
function draw(data){
    console.log(data);
    var global_overview_data = data;
    $('#totalNumber').html(global_overview_data.total_number);
    $('#sensitiveN').html(global_overview_data.sensitive_number);
    $('#hinfluence').html(global_overview_data.influence_number);
    $('#storeNumber').html(global_overview_data.recommend_in);
    $('#groupN').html(global_overview_data.monitor_number[0]);
    $('#gtotal').html(global_overview_data.monitor_number[1]);
    $('#wordsN').html(global_overview_data.new_sensitive_words);

    var div_name = 'sensitiveCloud';
    var c_title = '敏感词';
    var cloud_data = global_overview_data.sensitive_words;
    drawSensitiveCloud(div_name, c_title, cloud_data);
    var div_name = 'hashtagCloud';
    var c_title = 'hashtag';
    var cloud_data = global_overview_data.sensitive_hashtag;
    drawSensitiveCloud(div_name, c_title, cloud_data);
    
    // unfinished
    drawPsyState();

    var div_name = 'topic_portrait';
    var more_div_name = 'topic_more_portrait';
    var rank_data = global_overview_data.topic_rank;
    drawTopic(div_name, more_div_name, rank_data);
    var div_name = 'domain_portrait';
    var more_div_name = 'domain_more_portrait';
    var rank_data = global_overview_data.domain_rank;
    drawTopic(div_name, more_div_name, rank_data);


    var rank_list = new Array();
    rank_list['top_influence'] = 'influence';
    rank_list['importance'] = 'importance';
    rank_list['top_activeness'] = 'activeness';
    rank_list['top_sensitive'] = 'sensitive';
    rank_list['retweeted_user'] = 'retweeted_total';
    rank_list['top_comment_user'] = 'comment_total';
    rank_list['top_user_sensitive'] = 'top_weibo_number';
    var cname_list = new Array();
    cname_list['top_influence'] = '影响力';
    cname_list['importance'] = '重要性';
    cname_list['top_activeness'] = '活跃度';
    cname_list['top_sensitive'] = '敏感度';
    cname_list['retweeted_user'] = '转发量';
    cname_list['top_comment_user'] = '评论量';
    cname_list['top_user_sensitive'] = '敏感微博数';
    var more_div_list = new Array();
    more_div_list['top_influence'] = 'more_influence';
    more_div_list['importance'] = 'more_important';
    more_div_list['top_activeness'] = 'more_activeness';
    more_div_list['top_sensitive'] = 'more_sensitive';
    more_div_list['retweeted_user'] = 'more_retweeted';
    more_div_list['top_comment_user'] = 'more_comment';
    more_div_list['top_user_sensitive'] = 'more_sensitive_rank';
    for (var div_name in rank_list){
        var key = rank_list[div_name];
        var cname = cname_list[div_name];
        var more_div = more_div_list[div_name];
        drawRank(div_name, cname, data[key], more_div);
    }
}
var overview_url = '/overview/show/?date=2013-09-07';
call_ajax_request(overview_url, draw);
