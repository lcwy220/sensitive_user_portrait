jQuery(function($) {'use strict',

	
	// Flexslider slider
	$('.slidetexts').flexslider({
		animation: "slide",
		selector: ".slide-text .texts",
		controlNav: false,
		directionNav: false ,
		slideshowSpeed: 4000,  
		direction: "vertical",
		start: function(slider){
			$('body').removeClass('loading'); 
		}
	});

	$(window).bind('load', function () {
		parallaxInit();						  
	});
	function parallaxInit() {
        // custom for navbar
        if (($(".navbar-fixed-top").length > 0)) {
            if (($(this).scrollTop() > 0) && ($(window).width() > 767)) {
                $("body").addClass("fixed-header-on");
            } else {
                $("body").removeClass("fixed-header-on");
            }
        }
			$("#services").parallax("50%", 0.3);
			$("#promotion").parallax("50%", 0.3);
			$("#promotion-two").parallax("50%", 0.3);
			$("#testimonial").parallax("50%", 0.3);
		
	}	
	parallaxInit();	

	// Feature Tab Content
	$('.features-nav li').on('click',function(){'use strict',
		$('.features-nav li').removeClass('active');
		$(this).addClass('active');
	});
	$('#community-carousel ul.carousel-indicators li').on('click',function(){'use strict',
		$('.features-nav li').removeClass('active');
		var lists = $('.features-nav li');
		$(lists[$(this).index()]).addClass('active');
	});


	// Coummunity Carousel
	$('#community-carousel').carousel({
		interval: false
	});

	// portfolio filter
	$(window).load(function(){'use strict',
		$portfolio_selectors = $('.portfolio-filter >li>a');
		if($portfolio_selectors!='undefined'){
			$portfolio = $('.portfolio-items');
			$portfolio.isotope({
				itemSelector : '.col-sm-3',
				layoutMode : 'fitRows'
			});
			
			$portfolio_selectors.on('click', function(){
				$portfolio_selectors.removeClass('active');
				$(this).addClass('active');
				var selector = $(this).attr('data-filter');
				$portfolio.isotope({ filter: selector });
				return false;
			});
		}
	});


	// Contact form validation
	var form = $('.contact-form');
	form.submit(function () {'use strict',
		$this = $(this);
		$.post($(this).attr('action'), function(data) {
			$this.prev().text(data.message).fadeIn().delay(3000).fadeOut();
		},'json');
		return false;
	});


	// Navigation Scroll
	$(window).scroll(function(event) {
		Scroll();
	});

	$('.navbar-collapse ul li a').click(function() {  
        $('html, body').animate({scrollTop: $(this.hash).offset().top - 79}, 1000);
		return false;
	});

});

//Preloder script
jQuery(window).load(function(){'use strict';
	$(".preloader").remove();
	$("a[data-rel]").prettyPhoto();

	// Slider Height
	var slideHeight = $(window).height();
	$('#home-carousel .carousel-inner .item, #home-carousel .video-container').css('height',slideHeight);

	$(window).resize(function(){'use strict',
		$('#home-carousel .carousel-inner .item, #home-carousel .video-container').css('height',slideHeight);
	});

});


// User define function
function Scroll() {
	var contentTop      =   [];
	var contentBottom   =   [];
	var winTop      =   $(window).scrollTop();
	var rangeTop    =   200;
	var rangeBottom =   500;
	$('.navbar-collapse').find('.scroll > a').each(function(){
		contentTop.push( $( $(this).attr('href') ).offset().top);
		contentBottom.push( $( $(this).attr('href') ).offset().top + $( $(this).attr('href') ).height() );
	})
	$.each( contentTop, function(i){
		if ( winTop > contentTop[i] - rangeTop ){
			$('.navbar-collapse li.scroll')
			.removeClass('active')
			.eq(i).addClass('active');			
		}
	})
    $(window).scroll(function(){
        if (($(".navbar-fixed-top").length > 0)) {
            if (($(this).scrollTop() > 0) && ($(window).width() > 767)) {
                $("body").addClass("fixed-header-on");
            } else {
                $("body").removeClass("fixed-header-on");
            }
        }
    });

};

// Portfolio Single View

$('#portfolio').on('click','.folio-read-more',function(event){
	event.preventDefault();

	var link = $(this).data('single_url');
	var full_url = '#portfolio-single-wrap',
		parts = full_url.split("#"),
		trgt = parts[1],
		target_top = $("#"+trgt).offset().top;

	$('html, body').animate({scrollTop:target_top}, 1200);
	$('#portfolio-single').slideUp(1000, function(){
		$(this).load(link,function(){
			$(this).slideDown(1000);
		});
	});
});

// Close Portfolio Single View
$('#portfolio-single-wrap').on('click','.close-folio-item',function(){
	var full_url = '#portfolio',
		parts = full_url.split("#"),
		trgt = parts[1],
		target_offset = $("#"+trgt).offset(),
		target_top = target_offset.top;

	$('html, body').animate({scrollTop:target_top}, 1400);

	$("#portfolio-single").slideUp(1000);
});


// Google Map Customization
/*
(function(){

	var map;

	map = new GMaps({
		el: '#gmap',
		lat: 43.04446,
		lng: -76.130791,
		scrollwheel:false,
		zoom: 10,
		zoomControl : false,
		panControl : false,
		streetViewControl : false,
		mapTypeControl: false,
		overviewMapControl: false,
		clickable: false
	});

	var image = 'images/map-icon.png';
	map.addMarker({
		lat: 43.04446,
		lng: -76.130791,
		icon: image,
		animation: google.maps.Animation.DROP,
		verticalAlign: 'bottom',
		horizontalAlign: 'center',
		backgroundColor: '#3e8bff',
	});


	var styles = [ 

	{
		"featureType": "road",
		"stylers": [
		{ "color": "#000000" }
		]
	},{
		"featureType": "water",
		"stylers": [
		{ "color": "#333333" }
		]
	}
	,{
		"featureType": "landscape",
		"stylers": [
		{ "color": "#141414" }
		]
	},{
		"elementType": "labels.text.fill",
		"stylers": [
		{ "color": "#808080" }
		]
	},{
		"featureType": "poi",
		"stylers": [
		{ "color": "#161616" }
		]
	},{
		"elementType": "labels.text",
		"stylers": [
		{ "saturation": 1 },
		{ "weight": 0.1 },
		{ "color": "#7f8080" }
		]
	}

	];


	map.addStyle({
		styledMapName:"Styled Map",
		styles: styles,
		mapTypeId: "map_style"  
	});

	map.setStyle("map_style");
}());
*/
