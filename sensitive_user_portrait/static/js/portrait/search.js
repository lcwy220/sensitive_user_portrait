function call_ajax_request(url, callback){
    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        async: false,
        success: callback
    });
}
function simple_search(){
    console.log('fdghghfd');
	var simple_url = '/search/portrait_search/?stype=1';
	//simple_url += get_simple_par();
	console.log(url);
	call_ajax_request(simple_url, draw_search_results);
}
function advanced_search(){}

