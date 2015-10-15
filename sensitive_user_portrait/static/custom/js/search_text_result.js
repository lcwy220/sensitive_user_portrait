Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}

function Search_weibo(){
  this.ajax_method = 'GET';
}

Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_search_text: function(data){
  	console.log(data);
    var min_row = data.length;
    page_num = 20;
    if (min_row < page_num) {
          page_num = min_row
          page_sensitive_weibo( 0, page_num, data);
      }
      else {
          page_sensitive_weibo( 0, page_num, data);
          var total_pages = 0;
          if (min_row % page_num == 0) {
              total_pages = min_row / page_num;
          }
          else {
              total_pages = Math.round(min_row / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        page_icon(1,5,0);
    }else{
        page_icon(1,pageCount,0);
    }
    
    $("#pageGro li").live("click",function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#pageGro li.on").html())          
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > min_row)
          end_row = min_row;
        page_sensitive_weibo(start_row,end_row,data);
    });

    $("#pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index > 0){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html())  
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > min_row){
          end_row = min_row;
      }
        page_sensitive_weibo(start_row,end_row,data);
    });
    

    $("#pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html()) 
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > min_row){
          end_row = min_row;
      }
        page_sensitive_weibo(start_row,end_row,data);
    });
}
}
  function page_sensitive_weibo(start_row,end_row,data){
    var weibo_num = end_row - start_row;
    console.log(weibo_num);
    $('#weibo_content2').empty();
    if (weibo_num == 0){
        $('#weibo_content2').html('暂无微博数据');
        return;
    }else{
    var html = "";
    html += '<div class="group_weibo_font">';
    var colors = ['white', 'whitesmoke'];
    for (var s = start_row; s < end_row; s++) {
        var uname = data[s]['uname'];
        var timestamp = data[s]['timestamp'];
        var geo = data[s]['geo'];
        var text = data[s]['text'];
        var emotion_sort = data[s]['sentiment'];
        var message_type = data[s]['message_type'];
        var is_sensitive = data[s]['sensitive'];
        var uid = data[s]['uid'];
        if ((uname =='unknown') || (uname =='0')){
          uname = "未知";
        }
        if (is_sensitive == 1){
          sensitive = "敏感微博";
        }
        else{
          sensitive = '';
        }
        if (message_type == '1'){
          type = "原创微博";
        }
        else if(message_type == '2'){
          type = "转发微博";
        }
        else{
          type = "评论微博";
        }
        if (emotion_sort == 'positive'){
            emotion = '积极';
        }
        else if(emotion_sort == 'neutral'){
            emotion = '中性';
        }
        else{
            emotion = '消极';
        }
        var sensi_words_weibo = data[s]['sensitive_words'];
        var sensi_words_str = '';
        html += '<div style="padding:10px;background:' + colors[(s+1)%2] + ';font-size:13px">';
        html += '<p style="color:black;"><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;发布:&nbsp;'+ text + '</p>';
        if (sensi_words_weibo.length != 0){
          for (var i=0; i < sensi_words_weibo.length;i++){
              sensi_words_str += sensi_words_weibo[i] +'&nbsp;&nbsp;&nbsp;&nbsp;';
          }
      }
      else{
        sensi_words_str = '无';
      }
        html += '<p style="color:darkred;">敏感词:' + sensi_words_str +'&nbsp;&nbsp;情绪:<span style="color:red">'+ emotion + '</span>&nbsp;&nbsp;类型:<span>'+ type +'</span>&nbsp;&nbsp;<span>'+ sensitive + '</span><span style="float:right">' + timestamp + '&nbsp;&nbsp;' + geo + '&nbsp;&nbsp;'+ '</span></p>';
        html += '</div>'
    }
    html += '</div>'; 
    }
    $('#weibo_content2').append(html);
  }

function draw_conditions(){
    $('#conditions').empty();
    var html = '';
    html += '<span class="mouse" style="margin-left:10px">关键词:'+ words_list;
    $('#conditions').html(html);
}

function draw_empty_conditions(){
    $('#conditions').empty();
}
//请求数据
var Search_weibo = new Search_weibo(); 
$(document).ready(function(){
    draw_conditions();
    // words_list = words_list.split(' ');
    // search_text = '';
    // for (var i = 0; i < words_list.length;i++){
    //   search_text += words_list[i] + ',';
    // }
    // search_text = search_text.substring(0,search_text.length-1)
    // console.log(search_text);
    var sensitive_text = "/search/full_text_search/?words_list=" + words_list;
    Search_weibo.call_sync_ajax_request(sensitive_text, Search_weibo.ajax_method, Search_weibo.Draw_search_text);
})
