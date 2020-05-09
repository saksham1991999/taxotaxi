$(document).ready(function () {
    "use strict";

	/* Color Switcher Toggle Class Script
    ======================================================*/
	
	jQuery('.style-switch-button').click(function(){
		$('.theme_style_switcher').toggleClass("style-switch-active");
	})

	/* Color Switcher Toggle Stylesheet Script
    ======================================================*/

	$('#liteBlue').click(function (e){
		$('#switcher').attr('href','css/theme-color/light-blue-theme.css');
		e.preventDefault();
	});

	$('#orange').click(function (e){
		$('#switcher').attr('href','css/theme-color/orange-theme.css');
		e.preventDefault();
	});

	$('#pink').click(function (e){	  	
		$('#switcher').attr('href','css/theme-color/pink-theme.css');
		e.preventDefault();
	});

	$('#purple').click(function (e){
	    $('#switcher').attr('href','css/theme-color/purple-theme.css');
	    e.preventDefault();
	});
	  
	$('#darkBlue').click(function (e){
		$('#switcher').attr('href','css/theme-color/dark-blue-theme.css');
	    e.preventDefault();
	});
		
	$('#yellow').click(function (e){
	    $('#switcher').attr('href','css/theme-color/yellow-theme.css');
	    e.preventDefault();
	});
	
	$('#green').click(function (e){
	    $('#switcher').attr('href','css/theme-color/green-theme.css');
	    e.preventDefault();
	});

	$('#red').click(function (e){
	    $('#switcher').attr('href','css/theme-color/red-theme.css');
	    e.preventDefault();
	});  

});