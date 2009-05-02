/*
 * Javascript functions to create the RecurringDateInput Widget
 */

var cal_days_label = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
var cal_months_label = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var cal_days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31];
var cal_current_date = new Date();

function Calendar(month, year) {
    this.month = (isNaN(month) || month == null) ? cal_current_date.getMonth() : month;
    this.year = (isNaN(year) || year == null) ? cal_current_date.getFullYear() : year;
    this.html = '';
}

Calendar.prototype.generateHTML = function(year, month){
    this.year = year;
    this.month = month;
    var firstDay = new Date(this.year, this.month, 1);
    var startingDay = firstDay.getDay();
    var monthLength = cal_days_in_month[this.month];
    if(this.month == 1) {
        if((this.year % 4 == 0 && this.year % 100 != 0) || this.year % 400 == 0){
            monthLength = 29;
        }
    }
    var monthName = cal_months_label[this.month];
    var html = '<table class="recurringDateCalendar">';
    html += '<tr class="recurringDateCalendar-header"><td class="recurringDateCalendar-lnav">&laquo;</td><th colspan="5">';
    html += monthName + "&nbsp;" + this.year;
    html += '</th><td class="recurringDateCalendar-rnav">&raquo;</td></tr>';
    html += '<tr class="recurringDateCalendar-header-days">';
    for(var i=0; i<=6; i++){
        html += '<td>';
        html += cal_days_label[i];
        html += '</td>';
    }
    html += '</tr><tr class="recurringDateCalendar-row">';
    var day = 1;
    for(var i=0; i<9; i++) {
        for(var j=0; j<=6; j++) {
            if(day <= monthLength && (i > 0 || j >= startingDay)) {
                html += '<td class="recurringDateCalendar-day recurringDateCalendar-button">';
                html += day;
                day++;
            }else{
                html += '<td class="recurringDateCalendar-day">';
                html += '&nbsp;';
            }
            html += '</td>';
        }
        if(day > monthLength) {
            break;
        }else{
            html += '</tr><tr class="recurringDateCalendar-row">';
        }
    }
    html += '</tr></table>';
    this.html = html;
    return html;
}

Calendar.prototype.getHTML = function() {
    return this.html;
}

Calendar.prototype.nextMonth = function() {
    if(this.month == 11){
        this.month = 0;
        this.year = Number(this.year) + 1;
    }else{
        this.month = Number(this.month) + 1;
    }
}

Calendar.prototype.prevMonth = function() {
    if(this.month == 0){
        this.month = 11;
        this.year = Number(this.year) - 1;
    }else{
        this.month = Number(this.month) - 1;
    }
}

Calendar.prototype.getMonth = function() {
    return this.month;
}

Calendar.prototype.newDays = function() {
    var firstDay = new Date(this.year, this.month, 1);
    var startingDay = firstDay.getDay();
    var monthLength = cal_days_in_month[this.month];
    if(this.month == 1) {
        if((this.year % 4 == 0 && this.year % 100 != 0) || this.year % 400 == 0){
            monthLength = 29;
        }
    }
    var html = '<tr class="recurringDateCalendar-row">';
    var day = 1;
    for(var i=0; i<9; i++) {
        for(var j=0; j<=6; j++) {
            if(day <= monthLength && (i > 0 || j >= startingDay)) {
                html += '<td class="recurringDateCalendar-day recurringDateCalendar-button">';
                html += day;
                day++;
            }else{
                html += '<td class="recurringDateCalendar-day">';
                html += '&nbsp;';
            }
            html += '</td>';
        }
        if(day > monthLength) {
            break;
        }else{
            html += '</tr><tr class="recurringDateCalendar-row">';
        }
    }
    html += '</tr>';
    return html;
}

$(function(){
        var cal = new Calendar();
        $('.recurringDateInput').append('<div class="recurringDateInput-date"></div>');
        $('.recurringDateInput-date').append('<label for="date">When </label>');
        $('.recurringDateInput-date').append('<div rel="date"><input type="text" rel="start_date" value="start date" readonly="readonly"></div>');
        $('.recurringDateInput-date').append('<div rel="time"><input type="text" rel="start_time" value="start time" readonly="readonly"></div> to ');
        $('.recurringDateInput-date').append('<div rel="date"><input type="text" rel="end_date" value="end date" readonly="readonly"></div>');
        $('.recurringDateInput-date').append('<div rel="time"><input type="text" rel="end_time" value="end time" readonly="readonly"></div>');
        $('.recurringDateInput').append('\n<div class="recurringDateInput-options"></div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-recur-type"><input type="radio" name="recur_type" value="none" checked="checked" />Does Not Repeat</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-recur-type"><input type="radio" name="recur_type" value="daily" />Repeat Daily</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-recur-type"><input type="radio" name="recur_type" value="weekly" />Repeat Weekly</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-recur-type"><input type="radio" name="recur_type" value="monthly" />Repeat Monthly</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-recur-type"><input type="radio" name="recur_type" value="yearly" />Repeat Yearly</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-weekly-option" rel="weekly">Repeat every <select name="weekly_option"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select> weeks</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-weekly-days" rel="weekly"><label for="weekly_days">Repeat On:</label>Sun<input type="checkbox" name="weekly_days" value="sun">Mon<input type="checkbox" name="weekly_days" value="mon">Tue<input type="checkbox" name="weekly_days" value="tue">Wed<input type="checkbox" name="weekly_days" value="wed">Thu<input type="checkbox" name="weekly_days" value="thu">Fri<input type="checkbox" name="weekly_days" value="fri">Sat<input type="checkbox" name="weekly_days" value="sat"></div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-monthly-option" rel="monthly"><label for="monthly_option">Repeat By:</label><input type="radio" name="monthly_option" value="monthday" /> day of the month<input type="radio" name="monthly_option" checked="checked" value="weekday" /> day of the week</div>');
        $('.recurringDateInput-options').append('\n<div class="recurringDateInput-until"><label for="until_date">Ends: </label><div><input type="radio" name="until_date" value="never" />Never<br><input type="radio" name="until_date" value="until" />Until <input class="recurringDateInput-until-date" type="text" name="until_date" rel="until" readonly="readonly"></div></div>');

        $('.recurringDateInput-date > div[rel="date"] > input').add('.recurringDateInput-until-date').focus(function() {
            $('.recurringDateInput-calendar').remove();
            $(this).parent().append('<div class="recurringDateInput-calendar"></div>');
            var selected_date = $(this).val().split('/');
            $('.recurringDateInput-calendar').append(cal.generateHTML(selected_date[2], selected_date[0]-1));
            $('.recurringDateInput-calendar').css("margin-left", $(this).offset().left - $(this).parent().parent().offset().left);
            $(this).hover(function() {
                $('.recurringDateInput-calendar').show();
                },function() {
                });
            $('.recurringDateInput-calendar').hover(function() {
                $(this).show();
                }, function() {
                $(this).remove();
                });
            $('.recurringDateCalendar-lnav').click(function() {
                cal.prevMonth();
                $(this).next().replaceWith('<th colspan="5">' + cal_months_label[cal.getMonth()] + '&nbsp;' + cal.year + '</th>');
                $(this).parent().parent().find('.recurringDateCalendar-row').remove();
                $(this).parent().parent().append(cal.newDays());
                $(this).parent().parent().parent().parent().prev().change();
                });
            $('.recurringDateCalendar-rnav').click(function() {
                cal.nextMonth();
                $(this).prev().replaceWith('<th colspan="5">' + cal_months_label[cal.getMonth()] + '&nbsp;' + cal.year + '</th>');
                $(this).parent().parent().find('.recurringDateCalendar-row').remove();
                $(this).parent().parent().append(cal.newDays());
                $(this).parent().parent().parent().parent().prev().change();
                });
            $('.recurringDateCalendar-button').click(function() {
                    var val = (cal.getMonth()+1) + '/' + $(this).html() + '/' + cal.year;
                    $(this).parent().parent().parent().parent().prev().val(val).change();
                });
            });

        $('.recurringDateInput-date > div[rel="date"] > input').add('.recurringDateInput-until-date').change(function() {
            $('.recurringDateCalendar-button').live("click", function() {
                    var val = (cal.getMonth()+1) + '/' + $(this).html() + '/' + cal.year;
                    $(this).parent().parent().parent().parent().prev().val(val);
                });
            });

        $('.recurringDateInput-recur-type > input').click(function() {
            $('.recurringDateInput-weekly-option').hide();
            $('.recurringDateInput-weekly-days').hide();
            $('.recurringDateInput-monthly-option').hide();
            $('.recurringDateInput-until').hide();
            $('.recurringDateInput-weekly-option[rel="'+$(this).val()+'"]').show();
            $('.recurringDateInput-weekly-days[rel="'+$(this).val()+'"]').show();
            $('.recurringDateInput-monthly-option[rel="'+$(this).val()+'"]').show();
            if($(this).val() != "none"){
            $('.recurringDateInput-until').show();
            }
            });

        $('button[rel="test"]').click(function(event) {
                event.preventDefault();
                var start_date = $('.recurringDateInput-date > div > input[rel="start_date"]').val();
                var start_time = $('.recurringDateInput-date > div > input[rel="start_time"]').val();
                var end_date = $('.recurringDateInput-date > div > input[rel="end_date"]').val();
                var end_time = $('.recurringDateInput-date > div > input[rel="end_time"]').val();
                var recur_type = $('.recurringDateInput-options > div > input:checked').val();
                var weekly_option = $('.recurringDateInput-weekly-option > select > option:selected').val();
                var weekly_days = new Array();
                $('.recurringDateInput-weekly-days > input:checked').each(function() {
                    weekly_days.push($(this).val());
                    });
                if(weekly_days.length == 0){
                var chosen_date = start_date.split('/');
                chosen_date = new Date(chosen_date[2], chosen_date[0]-1, chosen_date[1]);
                weekly_days = cal_days_label[chosen_date.getDay()].toLowerCase();
                }
                else{
                    var weekly_days = weekly_days.join(',');
                }
                var monthly_option = $('.recurringDateInput-monthly-option > input:checked').val();
                var until_date = $('.recurringDateInput-until > div > input:checked').val();
                if(until_date == 'until'){
                var dateval = $('.recurringDateInput-until-date').val();
                until_date = until_date + ',' + dateval;
                }
                var new_value = start_date + ',' + start_time + ',' + end_date + ',' + end_time + ',' + recur_type;
                if(recur_type == 'daily'){
                    new_value = new_value + ',' + until_date;
                }
                if(recur_type == 'weekly'){
                    new_value = new_value + ',' + weekly_option + ',' + weekly_days + ',' + until_date;
                }
                if(recur_type == 'monthly'){
                    new_value = new_value + ',' + monthly_option + ',' + until_date;
                }
                if(recur_type == 'yearly'){
                    new_value = new_value + ',' + until_date;
                }
                $('.recurringDateInput > input[rel="value"]').val(new_value);
                });
        Populate();
});

function Populate() {
    var value = $('.recurringDateInput > input[rel="value"]').val();
    if(value == '') {
        today = new Date();
        value = (today.getMonth() + 1) + '/' + today.getDate() + '/' + today.getFullYear() + ',1:00pm,' + (today.getMonth() + 1) + '/' + today.getDate() + '/' + today.getFullYear() + ',2:00pm,none,1,weekday,until,' + (today.getMonth() +1) + '/' + today.getDate() + '/' + today.getFullYear();
    }
    var start_date = value.match(/^\d\d?\/\d\d?\/\d{4}/);
    value = value.replace(/^\d\d?\/\d\d?\/\d{4},/, '');
    var start_time = value.match(/^\d\d?:\d\d(?:am|pm)/);
    start_time = start_time[0];
    value = value.replace(/^\d\d?:\d\d(?:am|pm),/, '');
    var end_date = value.match(/^\d\d?\/\d\d?\/\d{4}/);
    value = value.replace(/^\d\d?\/\d\d?\/\d{4},/, '');
    var end_time = value.match(/^\d\d?:\d\d(?:am|pm)/);
    end_time = end_time[0];
    value = value.replace(/^\d\d?:\d\d(?:am|pm),/, '');
    var recur_type = value.match(/^none|daily|weekly|monthly|yearly/);
    recur_type = recur_type[0];
    value = value.replace(/^(none|dialy|weekly|monthly|yearly),?/, '');
    var weekly_option = value.match(/^\d\d?/);
    if(weekly_option) {
        weekly_option = weekly_option[0];
        value = value.replace(/^\d\d?,?/, '');
    }
    var weekly_days = value.match(/^(?:sun,|mon,|tue,|wed,|thu,|fri,|sat,){1,7}/);
    if(weekly_days) {
        weekly_days = weekly_days[0];
        weekly_days = weekly_days.substring(0, weekly_days.length-1);
        weekly_days = weekly_days.split(',');
        value = value.replace(/^((sun|mon|tue|wed|thu|fri|sat),)+/, '');
    }
    var monthly_option = value.match(/^(?:weekday|monthday)+/);
    if(monthly_option) {
        monthly_option = monthly_option[0];
        value = value.replace(/^weekday,|monthday,/, '');
    }
    var until_date = value.match(/until,\d\d?\/\d\d?\/\d{4}|never/);
    if(until_date){
        until_date = until_date[0].split(',');
    }

    $('.recurringDateInput-date > div > input[rel="start_date"]').val(start_date);
    $('.recurringDateInput-date > div > input[rel="start_time"]').val(start_time);
    $('.recurringDateInput-date > div > input[rel="end_date"]').val(end_date);
    $('.recurringDateInput-date > div > input[rel="end_time"]').val(end_time);
    $('.recurringDateInput-recur-type > input[value="'+recur_type+'"]').attr("checked", "checked").click();
    if(weekly_option) {
        $('.recurringDateInput-weekly-option > select > option[value="'+weekly_option+'"]').attr("selected", "selected");
    }
    if(weekly_days) {
        for(var i=0; i<weekly_days.length; i++) {
            $('.recurringDateInput-weekly-days > input[value="'+weekly_days[i]+'"]').attr("checked", "checked");
        }
    }
    if(monthly_option) {
        $('.recurringDateInput-monthly-option > input[value="'+monthly_option+'"]').attr("checked", "checked");
    }
    if(until_date) {
        $('.recurringDateInput-until > div > input[value="'+until_date.shift()+'"]').attr("checked", "checked").next().val(until_date.shift());
    }
}
