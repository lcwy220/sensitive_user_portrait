function group_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var group_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        group_uids.push(temp_list[i]);
      }
  }
  console.log(group_uids);
  var len = group_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_group_confirm(group_uids, "#group_comfirm");
      $("#group").modal();
  }
}

function draw_table_group_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="group_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr>';
      html += '<td class="center" name="group_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[6] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  if (group_confirm_uids.length < 1){
      alert('至少需要选择1名用户!');
      return;
  }
  console.log(group_confirm_uids);
  var group_ajax_url = '/group/submit_track_task/';
  var group_url = '/index/group_task/';
  var group_name = $('input[name="group_name"]').val();
  var remark = $('input[name="remark"]').val();
  console.log(group_name, remark);
  if (group_name.length == 0){
      alert('群体名称不能为空');
      return;
  }


  var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
  if (!group_name.match(reg)){
    alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if ((remark.length > 0) && (!remark.match(reg))){
    alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  var job = {"task_name":group_name, "uid_list":group_confirm_uids, "state":remark};
  $.ajax({
      type:'POST',
      url: group_ajax_url,
      contentType:"application/json",
      data: JSON.stringify(job),
      dataType: "json",
      success: callback
  });
  function callback(data){
      console.log(data);
      if (data == '1'){
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}

