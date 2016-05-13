function draw_search_results(data){
    //console.log(data);
    $('#search_result').empty();
    var user_url ;
    //console.log(user_url);
    var html = '';
    //html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<table class="table table-bordered table-striped table-condensed datatable">';
    html += '<thead><th style="width:100px;">用户ID</th>';
    html += '<th style="width:135px;">昵称</th>';
    html += '<th style="width:140px;">注册地</th>';
    html += '<th style="">活跃度</th>';
    html += '<th style="">身份敏感度</th>';
    html += '<th style="">影响力</th>';
    html += '<th style="">相关度</th>';
    html += '<th style="">操作</th></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      item = replace_space(item);
      if (item[1] == '未知'){
          item[1] = item[0];
      } 
      for(var j=3;j<7;j++){
        if(item[j]!='未知')
          item[j] = item[j].toFixed(2);
      }
      user_url = '/index/personal/?uid=' + item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '  target="_blank">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ item[2] +'</td>';
      html += '<td class="center" style="">'+ item[3] +'</td>';
      html += '<td class="center" style="">'+ item[4] +'</td>';
      html += '<td class="center" style="">'+ item[5] +'</td>';
      html += '<td class="center" style="">'+ item[6] +'</td>';
      html += '<td class="center" style="width:120px;"><a class="portrait_href" href=' + user_url + ' target="_blank">查看人物属性页</a></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#search_result').append(html);
    $('.datatable').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "aaSorting":[[5, 'desc']],
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "每页&nbsp; _MENU_ 条"
        }
    });
}
