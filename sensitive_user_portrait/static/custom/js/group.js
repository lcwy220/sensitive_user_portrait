 function Group_result(){
  this.ajax_method = 'GET';
}
Group_result.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_resultTable: function(data){
   // console.log(data);
    $('#group_task').empty();
	var item = data;
	var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>计算状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
		html += '<tr>';
		for(j=0;j<item[i].length-1;j++){
			if (j==0){
				html += '<td name="task_name">'+item[i][j]+'</td>';
			}else{
				html += '<td>'+item[i][j]+'</td>';
			}
		}
		if(item[i][4]==1){
			html += '<td><a style="cursor:hand;" href="/index/group_analysis/?name=' + item[i][0]+ '">已完成</a></td>';
		}else{
			html += '<td>正在计算</td>';
		}
		html +='<td><a href="javascript:void(0)" id="del">删除</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#group_task').append(html);
   
}
}
var Group_result = new Group_result();
url = '/group/show_task/' 
Group_result.call_sync_ajax_request(url, Group_result.ajax_method, Group_result.Draw_resultTable);

//上传文件
function handleFileSelect(evt){
    var files = evt;
	var task_name = $('#file_task_name').val();
	var state = $('#file_state').val();
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
			var a = oFREvent.target.result;	
			console.log(a);
			$.ajax({   
				type:"POST",  
				url:"/group/upload_file/",
				dataType: "json",
				async:false,
				data:{upload_data:a,task_name:task_name,state:state},
					
				success: function(){
					var show_url = "/group/show_task/";
					Group_result.call_sync_ajax_request(show_url,Group_result.ajax_method,Group_result.Draw_resultTable);
				}
					
			});
			location.reload();
		};            
		reader.readAsText(f,'GB2312');                                                        
    }
}
//删除群组

 function Group_delete(){
	 this.url = "/group/delete_group_task/?";
}
Group_delete.prototype = {   //群组搜索
call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: true,
      success:callback
    });
},
del:function(data){
	location.reload();
}
}

function deleteGroup(that){
	$('a[id^="del"]').click(function(e){
		var url = that.url;
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		console.log(temp);
		url = url + 'task_name=' + temp;
		//window.location.href = url;
		that.call_sync_ajax_request(url,that.ajax_method,that.del);
		console.log(url);
	});
}

var Group_delete = new Group_delete();
deleteGroup(Group_delete);
//搜索群组

