
function pagination_sales_list(){
	$(".pagination li.list:lt(5)").css({'display':'inline', 'margin-right':'0px'});
	$(".pagination li.list").first().css({'display':'inline'});
	$(".pagination li.active").next().css( "display", "inline" );
	$(".pagination li.active").prev().css( "display", "inline" );
	$('.pagination li.list').last().css({'display':'inline', 'margin-left':'40px'});
	$(".pagination li.list").last().addClass('last-place');
	$(window).on('load', function() {
		var current_lenght = $(".pagination li.list").length;
		current_lenght = current_lenght -4;
		console.log(current_lenght);
		var current_id = $("#active_page").val();
		current_id = parseInt(current_id);
		if( current_id >=5 ){
			$(".pagination li.list").first().addClass('first-place');
			$(".pagination li.list:lt(5)").css({'display':'none'});
			$(".pagination li.list").first().css({'display':'inline','margin-right':'40px'});
			$(".pagination li.active").next().css( "display", "inline" );
			$(".pagination li.active").prev().css( "display", "inline" );
			if(current_lenght <= current_id){
				$('.pagination li.list').last().css({'display':'inline', 'margin-left':'0px'});
				$('.pagination li.list').slice(-5).css("display", "inline");
			}
		}
	}); 
}

 
pagination_sales_list();