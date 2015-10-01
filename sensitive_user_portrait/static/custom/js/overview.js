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
	  
	  
//hashtag
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
	  
//心理状态
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
	
//重点领域人物
$('#domain_portrait').empty();
  var num = 0 
  //for (key in data['domain_top_user']){ 
  for(j=0;j<6;j++){
   num ++;
   if (num < 7){
       html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
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
	
//话题重点人物
$('#topic_portrait').empty();
  var num = 0 
  //for (key in data['domain_top_user']){ 
  for(j=0;j<6;j++){
   num ++;
   if (num < 7){
       html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
      // html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
	  html += '<span class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">生活</a></small></span>';
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
       $('#topic_portrait').append(html);
	   }
   }	
	
	
//画表格
//影响力排名
 $('#top_influence').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">影响力</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#top_influence').append(html);  
	
//重要度排名
$('#importance').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">重要度</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#importance').append(html);  
//活跃度排名
$('#top_activeness').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#top_activeness').append(html);

//敏感度排名	
$('#top_sensitive').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">敏感度</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#top_sensitive').append(html);
//转发量排名
 $('#retweeted_user').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">转发量</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#retweeted_user').append(html);  
//评论量排名
 $('#top_comment_user').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">评论量</th></tr>';
    for (var i = 0; i < 5; i++) {
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
    $('#top_comment_user').append(html);  
//发布敏感微博人
 $('#top_user_sensitive').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">发布敏感微博人</th></tr>';
    for (var i = 0; i < 5; i++) {
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
	$('#more_sensitive_rank').empty();
    html = '';
    html += '<table id="modal_online_pattern" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">上网方式</th><th style="text-align:center">微博数</th></tr>';
    /*
	for (var i = 0; i < data['online_pattern_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['online_pattern_top'][s]['0'] +  '</th><th style="text-align:center">' + data['online_pattern_top'][s]['1'] +  '</th></tr>';
    };
	*/
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iPhone 6 Plus</th><th style="text-align:center">88625</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">iPhone 6</th><th style="text-align:center">78230</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">iPhone客户端</th><th style="text-align:center">51368</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">360安全浏览器</th><th style="text-align:center">50629</th></tr>';
    html += '<tr><th style="text-align:center">' + 6 + '</th><th style="text-align:center">皮皮时光机</th><th style="text-align:center">48625</th></tr>';
    html += '<tr><th style="text-align:center">' + 7 + '</th><th style="text-align:center">vivo_X5Max</th><th style="text-align:center">48230</th></tr>';
    html += '<tr><th style="text-align:center">' + 8 + '</th><th style="text-align:center">iPhone 5s</th><th style="text-align:center">11368</th></tr>';
    html += '<tr><th style="text-align:center">' + 9 + '</th><th style="text-align:center">Android客户端</th><th style="text-align:center">9629</th></tr>';
    html += '<tr><th style="text-align:center">' + 10 + '</th><th style="text-align:center">红米Note</th><th style="text-align:center">8625</th></tr>';
    html += '<tr><th style="text-align:center">' + 11 + '</th><th style="text-align:center">搜狗高速浏览器</th><th style="text-align:center">8230</th></tr>';
    html += '<tr><th style="text-align:center">' + 12 + '</th><th style="text-align:center">小米手机2S</th><th style="text-align:center">7368</th></tr>';
    html += '<tr><th style="text-align:center">' + 13 + '</th><th style="text-align:center">三星 GALAXY S6</th><th style="text-align:center">6629</th></tr>';
    html += '<tr><th style="text-align:center">' + 14 + '</th><th style="text-align:center">iPad客户端</th><th style="text-align:center">6625</th></tr>';
    html += '<tr><th style="text-align:center">' + 15 + '</th><th style="text-align:center">iPad mini</th><th style="text-align:center">5230</th></tr>';
    html += '<tr><th style="text-align:center">' + 16 + '</th><th style="text-align:center">三星GALAXY S5</th><th style="text-align:center">4368</th></tr>';
    html += '<tr><th style="text-align:center">' + 17 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">3629</th></tr>';
    html += '<tr><th style="text-align:center">' + 18 + '</th><th style="text-align:center">微博手机版</th><th style="text-align:center">3230</th></tr>';
    html += '<tr><th style="text-align:center">' + 19 + '</th><th style="text-align:center">魅族 MX4</th><th style="text-align:center">2368</th></tr>';
    html += '<tr><th style="text-align:center">' + 20 + '</th><th style="text-align:center">三星GALAXY S4</th><th style="text-align:center">1629</th></tr>';
    html += '</table>'; 
    $('#more_sensitive_rank').append(html);                  