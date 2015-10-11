
//点击跳转页面
function pageGroup(pageNum,pageCount){
	switch(pageNum){
		case 1:
			page_icon(1,5,0);
		break;
		case 2:
			page_icon(1,5,1);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,3);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,4);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,2);
		break;
	}
}

//根据当前选中页生成页面点击按钮
function page_icon(page,count,eq){
	var ul_html = "";
	for(var i=page; i<=count; i++){
		ul_html += "<li>"+i+"</li>";
	}
	$("#pageGro ul").html(ul_html);
	$("#pageGro ul li").eq(eq).addClass("on");
}

//上一页
function pageUp(pageNum,pageCount){
	switch(pageNum){
		case 1:
		break;
		case 2:
			page_icon(1,5,0);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,2);
		break;
		case pageCount:
			page_icon(pageCount-4,pageCount,3);
		break;
		default:
			page_icon(pageNum-2,pageNum+2,1);
		break;
	}
}

//下一页
function pageDown(pageNum,pageCount){
	switch(pageNum){
		case 1:
			page_icon(1,5,1);
		break;
		case 2:
			page_icon(1,5,2);
		break;
		case pageCount-1:
			page_icon(pageCount-4,pageCount,4);
		break;
		case pageCount:
		break;
		default:
			page_icon(pageNum-2,pageNum+2,3);
		break;
	}
}
function Draw_global_weibo(data){
    var page_num = 10;
    if (data.length < page_num) {
          page_num = data.length
          page_group_weibo( 0, page_num, data);
    }
    else {
        page_group_weibo( 0, page_num, data);
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
      console.log(page);         
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        page_group_weibo(start_row,end_row,data);
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
      console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
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
      console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
    });
}

// 自定义微博列表
function page_group_weibo(start_row,end_row,data){
    weibo_num = end_row - start_row;
    $('#group_weibo').empty();
var html = "";
    html += '<div class="group_weibo_font">';
    for (var i = start_row; i < end_row; i += 1){
        s=i.toString();
        uid = data[s]['uid'];
        text = data[s]['text'];
        uname = data[s]['uname'];
        timestamp = data[s]['timestamp'];
        date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="background:whitesmoke;font-size:14px">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>'
    }
        else{
            html += '<div>';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>';
        }
    }
    html += '</div>'; 
    $('#group_weibo').append(html);
}
