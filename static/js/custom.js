$(document).ready(function () {
    "use strict";

	
	/* Preloader Script
    ======================================================*/
	
	$(".tj-loader").delay(800).slideUp(1600);
	$(".loader-outer").delay(800).slideUp(1600);
	
	
	
	/* Sticky Navigation
    ======================================================*/
	if( $('.tj-nav-row').length ){
		var stickyNavTop = $('.tj-nav-row').offset().top;
		var stickyNav = function(){
			var scrollTop = $(window).scrollTop();
			if (scrollTop > 500) { 
				$('.tj-nav-row').addClass('sticky');	
			} else {
				$('.tj-nav-row').removeClass('sticky'); 
			}
		};
		stickyNav();
		$(window).scroll(function() {
			stickyNav();
		});
    }
	
	
	/* Owl Slider For Partners
    ======================================================*/
    if ($('.partners-list').length) {
        $('.partners-list').owlCarousel({
            loop:true,
            dots: false,
            nav:false,
            navText:'',
            items:5,
            autoplay: false,
            smartSpeed:2000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:2,
                },
                768:{
                    items:3,
                },
                992:{
                    items:4,
                },
                1199:{
                    items:5,
                }
            }
        });
    }
	
	/* Owl Slider For Testimonial 1
    ======================================================*/
	if ($('#testimonial-slider').length) {
        $('#testimonial-slider').owlCarousel({
            loop:true,
            dots: false,
            nav:true,
            navText:'',
            items:2,
			margin:30,
            autoplay: true,
            smartSpeed:1000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
                },
                768:{
                    items:2,
                },
                992:{
                    items:2,
                },
                1199:{
                    items:2,
                }
            }
        });
    }
	
	
	/* Owl Slider For Testimonial 2
    ======================================================*/
	if ($('#testimonial-slider2').length) {
        $('#testimonial-slider2').owlCarousel({
            loop:true,
            dots: false,
            nav:false,
            navText:'',
            items:1,
            autoplay:true,
            smartSpeed:1200,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
                },
                768:{
                    items:1,
                },
                992:{
                    items:1,
                },
                1199:{
                    items:1,
                }
            }
        });
    }
	
	
	/* Owl Slider For Home 2 Cab Slider
    ======================================================*/
	if ($('#cab-slider').length) {
        $('#cab-slider').owlCarousel({
            loop:true,
            dots: false,
            nav:true,
            navText:'',
            items:1,
            autoplay:true,
            smartSpeed:1000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
					nav:false,
					dots:true,
                },
                768:{
                    items:1,
                },
                992:{
                    items:1,
                },
                1199:{
                    items:1,
                }
            }
        });
    }
    
    /* Blog Slider
    ======================================================*/
    if ($('#blog-slider').length) {
        $('#blog-slider').owlCarousel({
            loop:true,
            dots: false,
            nav:true,
            navText:'',
			autoplay:true,
            items:3,
            smartSpeed:1000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
                },
                768:{
                    items:1,
                },
                992:{
                    items:1,
                },
                1199:{
                    items:1,
                }
            }
        });
    }
	
	
	/* Counter Script
    ======================================================*/
	if ($('.fact-counter').length) {
		$('.fact-counter').counterUp({
			delay: 50,
			time: 3000
		});
	}
	
	if ($('.fact-count').length) {
		$('.fact-count').counterUp({
			delay: 70,
			time: 2000
		});
	}
	if ($('.fact-num').length) {
		$('.fact-num').counterUp({
			delay: 70,
			time: 2000
		});
	}
	
	
	/* Car Price Range Filter
    ======================================================*/
	if($( "#price-range" ).length){
		$( "#price-range" ).slider({
		  range: true,
		  min: 0,
		  max: 500,
		  values: [ 75, 300 ],
		  slide: function( event, ui ) {
			$( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
		  }
		});
		$( "#amount" ).val( "$" + $( "#price-range" ).slider( "values", 0 ) +
		" - $" + $( "#price-range" ).slider( "values", 1 ) );
	}
	
	
	/* Owl Slider For Fleet Carousel
    ======================================================*/
	if ($('#cab-carousel').length) {
        $('#cab-carousel').owlCarousel({
            loop:true,
            dots: false,
            nav:true,
            navText:'',
            items:3,
			margin:150,
			center: true,
            autoplay: true,
            smartSpeed:1000,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
                },
                768:{
                    items:2,
                },
                992:{
                    items:2,
                },
                1199:{
                    items:3,
                }
            }
        });
    }
	
	
	/* Cab Filter Isotope Script
    ======================================================*/
	if ($('.cab-filter').length) {
		var $container = $('.cab-filter').imagesLoaded(function() {
			$container.isotope({
				filter: '*',
				animationOptions: {
					duration: 750,
					easing: 'linear',
					queue: false,
				}
			});	
			$('.cab-filter-nav a').on("click", function(){
				$('.cab-filter-nav .current').removeClass('current');
				$(this).addClass('current');
		 
				var selector = $(this).attr('data-filter');
				$container.isotope({
					filter: selector,
					animationOptions: {
						duration: 750,
						easing: 'linear',
						queue: false,
					}
				 });
				 return false;
			}); 
		});
	}
	
	/* Twitter Feed Script
    ======================================================*/
	if ($('.tj-tweets').length) {
		$('.tj-tweets').twittie({
			username: 'sameersattar13',
			dateFormat: '%b, %d, %Y',
			template: '{{tweet}}} <div class="date">{{date}}</div>',
			count: 2,
			loadingText: 'Loading!'
		});
	}
	
	
	/* Gallery Carousel Script
    ======================================================*/
		
	if($(".gallery-thumb").length && $(".gallery").length){
		var right = $(".right-outer");
		var gal_thumb = $(".gallery-thumb");
		var gal = $(".gallery");

		gal_thumb.slick({
			rows: 0,
			slidesToShow: 2,
			draggable: false,
			useTransform: false,
			mobileFirst: true,
			responsive: [
			{
			  breakpoint: 768,
			  settings: {
				slidesToShow: 3
			  }
			},
			{
			  breakpoint: 1023,
			  settings: {
				slidesToShow: 1,
				vertical: true
			  }
			}
		  ]
		});

		gal.slick({
			rows: 0,
			useTransform: false,
			arrows: true,
			fade: true,
			autoplay: true,
			speed:600,
			cssEase: 'ease-in-out',
			asNavFor: gal_thumb,
		
		});
		$(".gallery-thumb .item").on("click", function() {
			var index = $(this).attr("data-slick-index");
			gal.slick("slickGoTo", index);
		});
	}
	function getCarouselHeight() {
		if($(".gallery-thumb").length && $(".gallery").length){
			if (window.matchMedia("(min-width: 1024px)").matches) {
				var galHeight = $(".gallery").height();
				right.css("height", galHeight);
			} else {
				right.css("height", "auto");
			}
		}else{
			return;
		}
	}

	$(window).on("load",function() {
		getCarouselHeight();
	});
		
	
	/* Contact Form Validation/Ajax Call
    ======================================================*/
    if($('#contact-form').length) {
    	$("#contact-form").validate({
    		rules: {
    			name: "required",
    			email: {
    				required: true,
    				email: true
    			},
    			subject: "required",
    			message: "required"
    		},
    		messages: {
    			name: "Please enter your name",
    			email: "Please enter a valid email address",
    			subject: "It is a required field",
    			message: "It is a required field",
    		},
    		submitHandler: function(form) {
    			$.ajax({
    				type : 'POST', 
    				url : 'contact/process.php', 
    				data  : {		
    					"formData" : $(form).serialize()
    				},
    				beforeSend: function() {
    					$("#frm_submit_btn").text("Sending..").addClass('wait');
    					$("#frm_submit_btn").attr('disabled','disabled');
    				},
    				success: function(result){
    					if(result==1){
    						alert("Thank you for contacting. We will get in touch with you soon!");
    						$("#frm_submit_btn").text("Email Sent").addClass('success');
    						$("#frm_submit_btn").removeAttr('disabled');
    						$("#frm_submit_btn").removeClass('wait');
    						$('#contact-form')[0].reset();
    					}else{
    						alert("Something went wrong. Please check your entries and try again");
    						$("#frm_submit_btn").text("Email Failed").addClass('fail');
    						$("#frm_submit_btn").removeAttr('disabled');
    						$("#frm_submit_btn").removeClass('wait');
    					}
    				}
    			});
    			
    			return false;
    		}
    	});
    }
      
      
      
      
    /* Booking Form Script
    ======================================================*/
	
	var nowDate = new Date();
	var today = new Date(nowDate.getFullYear(), nowDate.getMonth(), nowDate.getDate(), 0, 0, 0, 0);
	
	if($('.booking-frm #pickup_date').length){
		$('.booking-frm #pickup_date').datetimepicker({
			format: 'MM/DD/YYYY',
			minDate: today
		});
	}
	
	if($('.booking-frm #pickup_time').length){
		$('.booking-frm #pickup_time').datetimepicker({
			format: 'h:mm a',
		});
	}
	
	if($('.booking-frm #dropoff_date').length){
		$('.booking-frm #dropoff_date').datetimepicker({
			format: 'MM/DD/YYYY',
			minDate: today
		});
	}
	
	if($('.booking-frm #dropoff_time').length){
		$('.booking-frm #dropoff_time').datetimepicker({
			format: 'h:mm a'
		});
	}
	
	//On Load Condition
	var service_type = $(".booking-frm input[name='service_type']:checked").val();
	var booking_ref = Math.floor(Math.random() * 90000) + 10000;
	if( service_type !== null ){
		$('.booking-summary .service_type').text(service_type);
	}
	if( booking_ref !== null ){
		$('.booking-summary .book-ref').text(booking_ref);
	}
	
	//Display Saved Local Storage Ride Booking Data
	var book_ref = sessionStorage.getItem('book_ref');
	var start_loc = sessionStorage.getItem('start_loc');
	var end_loc = sessionStorage.getItem('end_loc');
	var pickup_date = sessionStorage.getItem('pickup_date');
	var pickup_time = sessionStorage.getItem('pickup_time');
	var dropoff_date = sessionStorage.getItem('dropoff_date');
	var dropoff_time = sessionStorage.getItem('dropoff_time');
	var service_type = sessionStorage.getItem('service_type');
	var trip_time = sessionStorage.getItem('trip_time');
	
	if( book_ref !== null ){
		$('.booking-summary .book-ref').text(book_ref);
	}
	if( service_type !== null ){
		$('.booking-summary .service_type').text(service_type);
		if( service_type === 'One Way Journey' ){
			$(".booking-frm #one_way").prop('checked', true);
		}else{
			$(".booking-frm #two_way").prop('checked', true);
		}
	}
	if( start_loc !== null ){
		$('.booking-summary .startup_loc').text(start_loc);
		$('.booking-frm  #point_start_loc').val(start_loc);
	}
	if( end_loc !== null ){
		$('.booking-summary .end_loc').text(end_loc);
		$('.booking-frm #point_end_loc').val(end_loc);
	}
	if( pickup_date !== null ){
		$('.booking-summary .pick_date').text(pickup_date);
		$('.booking-frm #pickup_date').val(pickup_date);
	}
	if( pickup_time !== null ){
		$('.booking-summary .pick_time').text(pickup_time);
		$('.booking-frm #pickup_time').val(pickup_time);
	}
	if( dropoff_date !== null ){
		$('.booking-summary .drop_date').text(dropoff_date);
		$('.booking-frm #dropoff_date').val(dropoff_date);
	}
	if( dropoff_time !== null ){
		$('.booking-summary .drop_time').text(dropoff_time);
		$('.booking-frm #dropoff_time').val(dropoff_time);
	}
	if( trip_time !== null ){
		$('.booking-summary .trip_est').text(trip_time);
	}
	
	//On Change Keypress Blur Keyup Condition
	$('.booking-frm #point_start_loc,.booking-frm input[name="service_type"],.booking-frm #point_end_loc,.booking-frm #pickup_date,.booking-frm #dropoff_date,.booking-frm #pickup_time,.booking-frm #dropoff_time').on('keyup keypress blur change',function(event){
		//Get Values
		var booking_field_val = $(this).val();
		var booking_field_id = $(this).attr('id');
		var service_type = $(".booking-frm input[name='service_type']:checked").val();
		$('.booking-summary .service_type').text(service_type);
		if( booking_field_val.length > 0 ){
			if(booking_field_id=='point_start_loc'){
				$('.booking-summary .startup_loc').text(booking_field_val);
			}else if(booking_field_id=='point_end_loc'){
				$('.booking-summary .end_loc').text(booking_field_val);
			}else if(booking_field_id=='pickup_date'){
				$('.booking-summary .pick_date').text(booking_field_val);
			}else if(booking_field_id=='dropoff_date'){
				$('.booking-summary .drop_date').text(booking_field_val);
			}else if(booking_field_id=='pickup_time'){
				$('.booking-summary .pick_time').text(booking_field_val);
			}else if(booking_field_id=='dropoff_time'){
				$('.booking-summary .drop_time').text(booking_field_val);
			}
		}else{
			if(booking_field_id=='point_start_loc'){
				$('.booking-summary .startup_loc').text('Enter Startup Location');
			}else if(booking_field_id=='point_end_loc'){
				$('.booking-summary .end_loc').text('Enter Destination');
			}else if(booking_field_id=='pickup_date'){
				$('.booking-summary .pick_date').text('Enter Pickup Date');
			}else if(booking_field_id=='pickup_time'){
				$('.booking-summary .pick_time').text('Enter Pickup Time');
			}else if(booking_field_id=='dropoff_date'){
				$('.booking-summary .drop_date').text('Enter Dropoff Date');
			}else if(booking_field_id=='dropoff_time'){
				$('.booking-summary .drop_time').text('Enter Dropoff Time');
			}
		}
	});
	
	if($('#ride-bform').length){
		$('#ride-bform').validate({
			rules: {
				pickup_loc: "required",
				pickup_date: "required",
				pickup_time: "required",
				dropoff_loc: "required",
				dropoff_date: "required",
				book_terms : "required",
				dropoff_time: "required"
			},
			messages: {
				pickup_loc: "This field is required",
				pickup_date: "This field is required",
				pickup_time: "This field is required",
				dropoff_loc: "This field is required",
				dropoff_date: "This field is required",
				book_terms: "This field is required",
				dropoff_time: "This field is required",
			},
			submitHandler: function(form) {
				//Fetch Form Submission Values
				var service_type = $(".booking-frm input[name='service_type']:checked").val();
				var start_loc = $('.booking-frm #point_start_loc').val();
				var end_loc = $('.booking-frm #point_end_loc').val();
				var pickup_date = $('.booking-frm #pickup_date').val();
				var pickup_time = $('.booking-frm #pickup_time').val();
				var dropoff_date = $('.booking-frm #dropoff_date').val();
				var dropoff_time = $('.booking-frm #dropoff_time').val();
				var book_ref = $('.booking-summary .book-ref').text();
				//Save Form Values Inside Local Storage
				sessionStorage.setItem('service_type', service_type);
				sessionStorage.setItem('start_loc', start_loc);
				sessionStorage.setItem('end_loc', end_loc);
				sessionStorage.setItem('book_ref', book_ref);
				sessionStorage.setItem('pickup_date', pickup_date);
				sessionStorage.setItem('pickup_time', pickup_time);
				sessionStorage.setItem('dropoff_date', dropoff_date);
				sessionStorage.setItem('dropoff_time', dropoff_time);
				var tripTime = '';
				var date1 = new Date(pickup_date + " " + pickup_time).getTime();
				var date2 = new Date(dropoff_date + " " + dropoff_time).getTime();
				var msec = date2 - date1;
				var mins = Math.floor(msec / 60000);
				var hrs = Math.floor(mins / 60);
				var days = Math.floor(hrs / 24);
				mins = mins % 60;
				hrs = hrs % 24;
		    	if( days === 0 && hrs === 0 && mins === 0 ){
					alert("Journey starting and ending time cannot be same. Please check and try again!");
					return false;
				}else{
					if( days >= 0 && hrs >= 0 && mins >= 0 ){
						tripTime = days + " days, " + hrs + " hours, " + mins + " minutes";
						sessionStorage.setItem('trip_time', tripTime);
						//Redirect Form to another page for booking confirmation
						window.location.href = "confirm-booking.html";
					}else{
						alert("Wrong Time or Date Selected. Please check and try again!");
						return false;
					}
				}
				
			}
		});
	}
	
	
	if($('#rider-info').length){
		$('#rider-info').validate({
			rules: {
				username: "required",
				phone_num: "required",
				email_id: "required",
			},
			messages: {
				username: "This field is required",
				phone_num: "This field is required",
				email_id: "This field is required",
			},
			submitHandler: function(form) {
				//Fetch Ride Booking Values
				var book_ref = sessionStorage.getItem('book_ref');
				var start_loc = sessionStorage.getItem('start_loc');
				var end_loc = sessionStorage.getItem('end_loc');
				var pickup_date = sessionStorage.getItem('pickup_date');
				var pickup_time = sessionStorage.getItem('pickup_time');
				var dropoff_date = sessionStorage.getItem('dropoff_date');
				var dropoff_time = sessionStorage.getItem('dropoff_time');
				var service_type = sessionStorage.getItem('service_type');
				var trip_time = sessionStorage.getItem('trip_time');
				
				if(start_loc !== null && end_loc !== null && pickup_date !== null && pickup_time !== null && dropoff_date !== null && dropoff_time !== null && service_type !== null ){
					$.ajax({
						type : 'POST', 
						url : 'contact/ride-booking.php', 
						data  : {		
							"formData" : $(form).serialize(),
							"book_ref" : book_ref,
							"start_loc" : start_loc,
							"end_loc" : end_loc,
							"pickup_date" : pickup_date,
							"pickup_time" : pickup_time,
							"dropoff_date" : dropoff_date,
							"dropoff_time" : dropoff_time,
							"service_type" : service_type,
							"trip_time" : trip_time,
						},
						beforeSend: function() {
							$("#ride-bbtn").text("Sending..").addClass('wait');
							$("#ride-bbtn").attr('disabled','disabled');
						},
						success: function(result){
							if(result==1){
								alert("Thank you for booking. We will get in touch with you soon!");
								$("#ride-bbtn").text("Email Sent").addClass('success');
								$("#ride-bbtn").removeAttr('disabled');
								$("#ride-bbtn").removeClass('wait');
								$('#rider-info')[0].reset();
								//Delete Booking Saved Data From Local Storage
								sessionStorage.removeItem("book_ref"); 
								sessionStorage.removeItem("start_loc"); 
								sessionStorage.removeItem("end_loc"); 
								sessionStorage.removeItem("pickup_date"); 
								sessionStorage.removeItem("pickup_time"); 
								sessionStorage.removeItem("dropoff_date"); 
								sessionStorage.removeItem("dropoff_date"); 
								sessionStorage.removeItem("dropoff_time"); 
								sessionStorage.removeItem("service_type"); 
								sessionStorage.removeItem("trip_time"); 
								
								$('.booking-summary .book-ref').text('Not Available');
								$('.booking-summary .service_type').text('Not Available');
								$('.booking-summary .startup_loc').text('Not Available');
								$('.booking-summary .end_loc').text('Not Available');
								$('.booking-summary .pick_date').text('Not Available');
								$('.booking-summary .pick_time').text('Not Available');
								$('.booking-summary .drop_date').text('Not Available');
								$('.booking-summary .drop_time').text('Not Available');
								$('.booking-summary .trip_est').text('Not Available');
							}else{
								alert("Something went wrong. Please check your entries and try again");
								$("#ride-bbtn").text("Email Failed").addClass('fail');
								$("#ride-bbtn").removeAttr('disabled');
								$("#ride-bbtn").removeClass('wait');
							}
						}
					});
				}
				return false;
			}
		});
	}
		
});