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
function drawSensitiveCloud(){
    var sensitiveChart = echarts.init(document.getElementById('sensitiveCloud')); 
	var optionSensitive = {
        title: {
            text: '敏感词',
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
            data: [
                {
                    name: "Sam S Club",
                    value: 10000,
                    itemStyle: {
                        normal: {
                            color: 'black'
                        }
                    }
                },
                {
                    name: "Macys",
                    value: 6181,
                    itemStyle: createRandomItemStyle()
                },
                {
                    name: "Amy Schumer",
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
    sensitiveChart.setOption(optionSensitive);
}	  
	  
//hashtag
function drawHashtagCloud(){
	var hashtagChart = echarts.init(document.getElementById('hashtagCloud')); 
	var optionHashtag = {
        title: {
            text: 'hashtag',
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
            data: [
                {
                    name: "Sam S Club",
                    value: 10000,
                    itemStyle: {
                        normal: {
                            color: 'black'
                        }
                    }
                },
                {
                    name: "Macys",
                    value: 6181,
                    itemStyle: createRandomItemStyle()
                },
                {
                    name: "Amy Schumer",
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
    hashtagChart.setOption(optionHashtag);
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

//重点领域人物
function drawDomain(){
    $('#domain_portrait').empty();
  var num = 0 
  //for (key in data['domain_top_user']){ 
  for(j=0;j<6;j++){
   num ++;
   if (num < 7){
       html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:20px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
      // html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
	  html += '<span class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">草根</a></small></span>';
       html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
       html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
       for(i=0;i<6;i++){
	   /*
	   for (i = 0; i<data['domain_top_user'][key].length; i++){
          var s = i.toString();
           if (data['domain_top_user'][key][s]['1'] == 'unknown'){
              domain_top_username = '未知';
           }else{
              domain_top_username = data['domain_top_user'][key][s]['1'];
                  };
           if (data['domain_top_user'][key][s]['2'] == 'unknown'){
              domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
           }else{
              domain_top_user_portrait = data['domain_top_user'][key][s]['2'];
                  };
		
          html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['domain_top_user'][key][s]['0'] +'" title="' + domain_top_username +'">';
          html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';         
       */
	   html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope">';
	    html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="http://tp2.sinaimg.cn/1878376757/50/0/1" alt="xxx"></div></a></li>';
	   }
       html += '</ul></div></div>';
       $('#domain_portrait').append(html);
	   }
   }
}	
//话题重点人物
function drawTopic(){
    $('#topic_portrait').empty();
  var num = 0 
  //for (key in data['domain_top_user']){ 
  for(j=0;j<6;j++){
   num ++;
   if (num < 7){
       html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:20px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
      // html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
	  html += '<span class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">生活</a></small></span>';
       html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
       html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
       for(i=0;i<6;i++){
	   /*
	   for (i = 0; i<data['domain_top_user'][key].length; i++){
          var s = i.toString();
           if (data20domain_top_user'][key][s]['1'] == 'unknown'){
              domain_top_username = '未知';
           }else{
              domain_top_username = data['domain_top_user'][key][s]['1'];
                  };
           if (data['domain_top_user'][key][s]['2'] == 'unknown'){
              domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
           }else{
              domain_top_user_portrait = data['domain_top_user'][key][s]['2'];
                  };
		
          html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['domain_top_user'][key][s]['0'] +'" title="' + domain_top_username +'">';
          html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';         
       */
	   html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope">';
	    html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="http://tp2.sinaimg.cn/1878376757/50/0/1" alt="xxx"></div></a></li>';
	   }
       html += '</ul></div></div>';
       $('#topic_portrait').append(html);
	   }
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
           /*
           if (data['top_retweeted_user'][s]['1'] == 'unknown'){
              top_retweeted = '未知';
           }else{
              top_retweeted = data['top_retweeted_user'][s]['1'];
           };
           html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_retweeted_user'][s]['0'] + '">' + top_retweeted + '</a></th><th style="text-align:center">' + data['top_retweeted_user'][s]['3'] +  '</th></tr>';
            */
         html += '<tr><th style="text-align:center">' + m + '</th>';
         html += '<th style="text-align:center">' + rank_data[i] + '</th>';
         html += '<th style="text-align:center">1000</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);  

//发布敏感微博人
     $('#top_user_sensitive').empty();
        html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">发布敏感微博人</th></tr>';
        var min_row = Math.min(5, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           /*
           if (data['top_retweeted_user'][s]['1'] == 'unknown'){
              top_retweeted = '未知';
           }else{
              top_retweeted = data['top_retweeted_user'][s]['1'];
           };
           html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_retweeted_user'][s]['0'] + '">' + top_retweeted + '</a></th><th style="text-align:center">' + data['top_retweeted_user'][s]['3'] +  '</th></tr>';
            */
         html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">国际在线</th><th style="text-align:center">1000</th></tr>';
        };
        html += '</table>'; 
        $('#top_user_sensitive').append(html);  
	
	
	//更多
	$('#' + more_div).empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th>';
    html += '<th style="text-align:center">昵称</th><th style="text-align:center">' + cname + '</th></tr>';
	for (var i = 0; i < rank_data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th>';
       html += '<th style="text-align:center">' + rank_data[i] +  '</th>';
       html += '<th style="text-align:center">1000</th></tr>';
    };
    html += '</table>'; 
    $('#' + more_div).append(html);                  
}
function draw(data){
    console.log(data);
    global_overview_data = data;
    var rank_list = new Array();
    rank_list['top_influence'] = 'influence';
    rank_list['importance'] = 'importance';
    rank_list['top_activeness'] = 'activeness';
    rank_list['top_sensitive'] = 'sensitive';
    rank_list['retweeted_user'] = 'top_retweeted';
    rank_list['top_comment_user'] = 'top_comment';
    //rank_list['top_user_sensitive'] = '';
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
var global_overview_data;
var overview_url = '/overview/show/?date=2013-09-07';
call_ajax_request(overview_url, draw);
drawSensitiveCloud();
drawHashtagCloud();
drawPsyState();
drawDomain();
drawTopic();
