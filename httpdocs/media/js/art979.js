$(function(){
	$('#cssdropdown li.headlink').hover(
		function() { $('ul', this).css('display', 'block'); },
		function() { $('ul', this).css('display', 'none'); });
	$('ul.sf-menu').superfish({
 	  	pathClass: 'current',
        delay: 0,
		speed: 'fast',
		});
});
