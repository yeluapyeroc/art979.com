$(function(){
	$('#cssdropdown li.headlink').hover(
		function() { $('ul', this).css('display', 'block'); },
		function() { $('ul', this).css('display', 'none'); });

    var value = $('.weeklydate > #weeklydatevalue').val();
    $('.weeklydate > .dayButton').each(function(i) {
        if(value.search($(this).attr('rel')) >= 0) {
        $(this).addClass("pressed");
        $(this).next().val("pressed");
        }
        });
    $('.weeklydate > .dayButton').click(function(i) {
        $(this).toggleClass("pressed");
        if($(this).next().val() == "pressed") {
        $(this).next().val("unpressed");
        }else{
        $(this).next().val("pressed");
        }
        });
});
