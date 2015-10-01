function custom_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
  var custom_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        custom_uids.push(temp_list[i]);
      }
  }
  console.log(custom_uids);
  var len = custom_uids.length;
  if(len<1){
    alert("请至少选择1个用户！");
  }
  else{
      draw_table_custom_confirm(custom_uids, "#custom_confirm");
      get_custom_name();
      $('#custom').modal();
  }
}
function draw_table_custom_confirm(uids, div){
    $(div).empty();
    var html = '';
    html += '<table id="custom_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>相关度</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="custom_confirm_uids">'+ uids[i] +'</td>';
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
function custom_confirm_button(){
  var custom_confirm_uids = [];
  $('[name="custom_confirm_uids"]').each(function(){
      custom_confirm_uids.push($(this).text());
  })
  if (custom_confirm_uids.length < 1){
      alert('至少需要选择1名用户!');
      return;
  }
  var attribute_name = $('[name=attribute_name]').val();
  var attribute_value = $('[name=attribute_value]').val();
  var custom_url = '/tag/add_group_tag/?uid_list='+ custom_confirm_uids.join(',');
  custom_url += '&attribute_name=' + attribute_name + '&attribute_value=' + attribute_value;
  console.log(custom_url);
  base_call_ajax_request(custom_url, callback);
  function callback(data){
       console.log(data);
  }
}
