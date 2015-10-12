//情绪分析
var emotion_charts = echarts.init(document.getElementById('emotion_chart'));
var pos_emotion=[120, 132, 101, 134, 90, 230,  210];
var neg_emotion=[220, 182, 191, 234, 290, 330, 310];
var neu_emotion=[150, 232, 201, 154, 190, 330, 410];
var emotion_data = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['积极','消极','中性']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'积极',
            type:'line',
            stack: '总量',
            data:[]
        },
        {
            name:'消极',
            type:'line',
            stack: '总量',
            data:[]
        },
        {
            name:'中性',
            type:'line',
            stack: '总量',
            data:[]
        }
    ]
};        
//emotion_data["xAxis"][0]["data"]=[120, 132, 101, 134, 90, 230,  210];       
emotion_data["series"][0]["data"]=pos_emotion;
emotion_data["series"][1]["data"]=neg_emotion;
emotion_data["series"][2]["data"]=neu_emotion;
emotion_charts.setOption(emotion_data);

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
				data:[],
				
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
Influenceoption["series"][0]["data"] = [345,23,55,25,897,34,88,100]
influenceChart.setOption(Influenceoption); 
//一周轨迹分布
$('.course_nr2').find('.shiji').slideDown(600);

for(i=0;i<7;i++){
		document.getElementById('d'+(i+1)).innerHTML = '09-01';

		document.getElementById('city'+(i+1)).innerHTML = '北京';
		/*
        var item = track_data[i];
        var date = item[0];
        var city = item[1];
        document.getElementById('d'+(i+1)).innerHTML = date.substring(4,6) + '-' + date.substring(6,9);
        if(city.length > 0){
            document.getElementById('city'+(i+1)).innerHTML = city.join(',');
        }else{
            $('#city'+(i+1)).addClass('gray');
            document.getElementById('city'+(i+1)).innerHTML = '未发布微博';
        }
		*/
		
	}// JavaScript Document

//敏感词
var sensitive_words = ['a1', 'b1', '1c', '1d'];
var word_length = sensitive_words.length;
var addwords = ''
for(i=0;i<word_length;i++){
    addwords = addwords+'<span>'+sensitive_words[i]+',</span>'
}
document.getElementById('sensi_words').innerHTML = addwords

//hashtag和敏感词云
var sensi_cloud_list = [['但是',23], ['345',78], ['是的',167], ['和你',90]];
var hash_cloud_list = [['但是',23], ['345',78], ['是的',167], ['和你',90]];
//var hash_cloud_list = [{'但是':23}, {'345':78}, {'是的':167}, {'和你':90}, {'请问':233}, {'你':320}, {'热':99},{'新材':210} , {'突然':150}, {'速度';330}, {'朋友':139}];
drawSensitiveCloud('hashtag_cloud', '', hash_cloud_list);
drawSensitiveCloud('sensi_word_cloud', '', sensi_cloud_list);

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
function drawSensitiveCloud(div_name, c_title, cloud_data){
    var sensitiveChart = echarts.init(document.getElementById(div_name)); 
    
    
    
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
//敏感词详情






//敏感词表格
//画表格
var table_data=[{'word':'敏感词1','frency':20,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词2','frency':18,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词3','frency':17,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词4','frency':12,'word_level':'leve2','word_class':'a类词'},{'word':'敏感词5','frency':10,'word_level':'leve1','word_class':'b类词'},{'word':'敏感词6','frency':9,'word_level':'leve2','word_class':'b类词'},{'word':'敏感词7','frency':8,'word_level':'leve1','word_class':'a类词'},]   

$('#show_sensi_word').click(function (){
    var word_level=$("#sensi_word_level").val();
    var word_class=$("#sensi_word_class").val();
    var choose_data=[];
    //var need_data=[]
    if (word_level==0){
        if (word_class==0){
            choose_data = table_data;
        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_class']=='b类词'){
                    choose_data.push(table_data[i])
                }

            }
        }
    }else if(word_level==1){
        if (word_class==0){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1'){
                    choose_data.push(table_data[i])
                }

            }

        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1' & table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve1' & table_data[i]['word_class']=='b类词'){
                    choose_data.push(table_data[i])
                }

            }
        }

        }else if(word_level==2){
        if (word_class==0){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2' & table_data[i]['word_class']=='a类词'){
                    choose_data.push(table_data[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['word_level']=='leve2' & table_data[i]['word_class']=='b类词'){
                    choose_data.push(table_data[i])
                }

            }
        }

    }
drawRank('sensiword_table','敏感词', choose_data, 'word');   

    })
//画表格：语言属性
function drawRank(div_name,c_name, rank_data, item_name){
    if (!rank_data){
        rank_data = new Array();
    }
    $('#'+ div_name).empty();
        html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center;width:50px;">排名</th><th style="text-align:center;width:150px;">'+c_name+'</th>';
        //html += '<th style="text-align:center">' + cname + '</th></tr>';
        var min_row = Math.min(10, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           var item = rank_data[i];
           var sensitive_word;
           if ((item[item_name] == 'unknown') || (item[item_name] == '0')){
               sensitive_word = '未知';
           }
           else{
               sensitive_word = item[item_name];
           }
         html += '<tr><th style="text-align:center;width:50px;">' + m + '</th>';
         html += '<th style="text-align:center;width:150px;">' + sensitive_word + '</a></th>';
         //html += '<th style="text-align:center">' + item[2].toFixed(2) + '</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);
        }  
drawRank('sensiword_table','敏感词',table_data, 'word');
var dict_sensi_cloud = getCloudData(sensi_cloud_list);
var dict_hash_cloud = getCloudData(hash_cloud_list);
drawRank('sensi_detail_body','敏感词', dict_sensi_cloud, 'name');
drawRank('hash_detail_body','敏感词', dict_hash_cloud, 'name');


// 敏感微博列表
var weibo_data = [['2015-09-01','北京 北京','1例如我们在做一个很长的网页时,需要在页面内做一个导航,点击导航里的链接不是新开一个窗口或者跳转到其他网址,而是跳转到当前页的某一个位置',['敏感词7','敏感词5'],0,'情绪',['aaa1','bbb','ccc','ddd']],['2015-09-02','北京 北京','2例如我们在做一个很长的网页时,需要在页面内做一个导航,点击导航里的链接不是新开一个窗口或者跳转到其他网址,而是跳转到当前页的某一个位置',['敏感词7','敏感词5'],1,'情绪',['aaa2','bbb','ccc','ddd']],
['2015-09-01','北京 北京','3例如我们在做一个很长的网页时,需要在页面内做一个导航,点击导航里的链接不是新开一个窗口或者跳转到其他网址,而是跳转到当前页的某一个位置',['敏感词7','敏感词5'],0,'情绪',['aaa3','bbb','ccc','ddd']],['2015-09-02','北京 北京','4例如我们在做一个很长的网页时,需要在页面内做一个导航,点击导航里的链接不是新开一个窗口或者跳转到其他网址,而是跳转到当前页的某一个位置',['敏感词7','敏感词5'],1,'情绪',['aaa4','bbb','ccc','ddd']]];

function page_group_weibo(start_row,end_row,data){
    var weibo_num = end_row - start_row;
    $('#weibo_content2').empty();
    if (weibo_num == 0){
        $('#weibo_content2').html('暂无微博数据');
        return;
    }
    var html = "";
    html += '<div class="group_weibo_font">';
    var colors = ['white', 'whitesmoke'];
    for (var s = start_row; s < end_row; s++){
        var timestamp = data[s][0];
        var geo = data[s][1];
        var text = data[s][2];
        var emotion = data[s][5];
        var sensi_words_weibo = data[s][3]
        var retweeted_line_detail = data[s][6]

        for (var i=0; i < sensi_words_weibo.length;i++){
            sensi_words_str += sensi_words_weibo[i] +'&nbsp;&nbsp;&nbsp;&nbsp;'
        }
        //var comment = data[s][6];
        // uid = data[s]['uid'];
        // uname = data[s]['uname'];
        // var date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (data[s][4] == 0){
            var re_line = '<span style="margin-left:30px;"><a data-toggle="modal"  data-target="#retweeted_line'+s+'">转发链</a></span>';
        }
        else{
            var re_line = '';
        }
        if (data[s][3].length != 0){
            var sensi_words_str=''
            var re_line_str='<p>'
            for (var i=0; i < retweeted_line_detail.length-1;i++){
                re_line_str += retweeted_line_detail[i] +'&nbsp;&nbsp;>>>>>&nbsp;&nbsp;';
            }
            re_line_str += retweeted_line_detail[retweeted_line_detail.length-1]+'</p>';
            drawmodal(s,re_line_str);
        }

        html += '<div style="padding:10px;background:' + colors[(s+1)%2] + ';font-size:13px">';
        // html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
        html += '<p style="color:black;">'  + text + '</p>';
        html += '<p style="color:darkred;">敏感词：' + sensi_words_str +'&nbsp;&nbsp;情绪:<span style="color:red">'+ emotion + re_line+ '</span><span style="float:right">' + timestamp + '&nbsp;&nbsp;' + geo + '&nbsp;&nbsp;'+ '</span></p>';
        html += '</div>'
    }
    html += '</div>'; 
    $('#weibo_content2').append(html);
}


Draw_global_weibo(weibo_data)

//转发链模态框
function drawmodal(id,data){

    var html = '<div class="modal fade" id="retweeted_line'+ id +'" tabindex="-1" role="dialog" aria-labelledby="sensi_detail_content"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"></button><h4 class="modal-title" id="sensi_detail_content">微博转发关系</h4></div><div class="modal-body" id="re_relation' + id + '">'+ data + '</div><div class="modal-footer"><button type="button" class="btn btn-default" data-dismiss="modal">Close</button></div></div></div></div>';
    $('#weibo_re_modal').append(html);

}

//画交互信息表格
function drawRank_social(div_name, rank_data, more_div){
    if (!rank_data){
        rank_data = new Array();
    }
     $('#'+ div_name).empty();
        var html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
        html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th>';
        html += '<th style="text-align:center">次数</th>';
        html += '<th style="text-align:center">是否入库</th></tr>';
        var min_row = Math.min(5, rank_data.length);
        for (var i = 0; i < min_row; i++) {
           var s = i.toString();
           var m = i + 1;
           var item = rank_data[i];
           var nickname;
           if ((item[1][0] == 'unknown') || (item[1][0] == '0')){
               nickname = '未知';
           }
           else{
               nickname = item[1][0];
           }
           var in_status;
           if (item[1][2] == 0){
               in_status = '否';
           }
           else{
               in_status = '是';
           }
         html += '<tr><th style="text-align:center">' + m + '</th>';
         html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
         html += '<th style="text-align:center">' + item[1][1] + '</th>';
         html += '<th style="text-align:center">' + in_status + '</th></tr>';
        };
        html += '</table>'; 
        $('#' + div_name).append(html);  

    //更多
    $('#' + more_div).empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th>';
    html += '<th style="text-align:center">昵称</th>';
    html += '<th style="text-align:center">次数</th>';
    html += '<th style="text-align:center">是否入库</th></tr>';
    for (var i = 0; i < rank_data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       var item = rank_data[i];
       var nickname;
       if ((item[1][0] == 'unknown') || (item[1][0] == '0')){
           nickname = '未知';
       }
       else{
           nickname = item[1][0];
       }
       var in_status;
       if (item[1][2] == 0){
           in_status = '否';
       }
       else{
           in_status = '是';
       }
       html += '<tr><th style="text-align:center">' + m + '</th>';
       html += '<th style="text-align:center"><a title=' + item[0] +' target="_blank" href="/index/personal/?uid=' + item[0] + '">' + nickname + '</a></th>';
       html += '<th style="text-align:center">' + item[1][1] + '</th>';
       html += '<th style="text-align:center">' + in_status + '</th></tr>';
    };
    html += '</table>'; 
    $('#' + more_div).append(html);                  
}
function draw(data){
    console.log(data);
    personalData = data;
    drawBasic(personalData);
    drawInfluenceTrend(personalData.influence_trend);
    drawTimeTrend(personalData.time_trend);
    drawTrack(personalData.activity_geo_distribute);

    var rank_list = new Array();
    rank_list['repost'] = 'retweet';
    rank_list['retweeted'] = 'follow';
    rank_list['top_at'] = 'at';
    var more_div_list = new Array();
    more_div_list['repost'] = 'more_repost';
    more_div_list['retweeted'] = 'more_retweeted';
    more_div_list['top_at'] = 'more_at';
    for (var div_name in rank_list){
        var key = rank_list[div_name];
        var more_div = more_div_list[div_name];
        drawRank_social(div_name, data[key][0], more_div);
    }

}