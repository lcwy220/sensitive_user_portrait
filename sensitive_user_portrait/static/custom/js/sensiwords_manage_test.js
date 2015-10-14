function Draw_sensi_manage_table(data){
	//console.log(data);
	$('#sensi_manage_table').empty();
    var item = data;
    console.log(item);
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>敏感词</th><th>等级</th><th>类别</th><th>时间</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="attribute_name">'+item[i].words+'</td>';
		/*var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" title="点击编辑">'+item_value+'</a></td>';
        }*/
        html += '<td name="level">'+item[i].level+'</td>';
        html += '<td name="class">'+item[i].sensi_class+'</td>';
		html += '<td name="time">'+item[i].date+'</td>';
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="delTag">修改</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#sensi_manage_table').append(html);
  }


var table_data1 = [{'words':'敏感词1','level':'A','sensi_class':'a类','date':'09-01'},{'words':'敏感词2','level':'A','sensi_class':'b类','date':'09-01'},{'words':'敏感词3','level':'B','sensi_class':'a类','date':'09-01'},{'words':'敏感词4','level':'B','sensi_class':'b类','date':'09-01'}];
Draw_sensi_manage_table(table_data1);	

$('#show_sensi_manage').click(function (){
    var word_level=$("#sensi_manage_level").val();
    var word_class=$("#sensi_manage_class").val();
    alert(word_level);
    var choose_data=[];
    //var need_data=[]
    if (word_level==0){
        if (word_class==0){
            choose_data = table_data1;
            alert(choose_data);
        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['sensi_class']=='a类'){
                    choose_data.push(table_data1[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['sensi_class']=='b类'){
                    choose_data.push(table_data1[i])
                }

            }
        }
    }else if(word_level==1){
        if (word_class==0){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['sensi_class']=='A'){
                    choose_data.push(table_data1[i])
                }

            }

        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['level']=='A' & table_data[i]['sensi_class']=='a类'){
                    choose_data.push(table_data1[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['level']=='A' & table_data[i]['sensi_class']=='b类'){
                    choose_data.push(table_data1[i])
                }

            }
        }

        }else if(word_level==2){
        if (word_class==0){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['level']=='B'){
                    choose_data.push(table_data1[i])
                }

            }
        }else if (word_class==1){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['level']=='B' & table_data[i]['sensi_class']=='a类'){
                    choose_data.push(table_data1[i])
                }

            }
        }else if (word_class==2){
            for (var i = 0; i < table_data.length; i++) {
                if (table_data[i]['level']=='B' & table_data[i]['sensi_class']=='b类'){
                    choose_data.push(table_data1[i])
                }

            }
        }

    }
Draw_sensi_manage_table(choose_data);   

})