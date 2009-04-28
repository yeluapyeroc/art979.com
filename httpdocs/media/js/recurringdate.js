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

Calendar.prototype.generateHTML = function(){
    var firstDay = new Date(this.year, this.month, 1);
    var startingDay = firstDay.getDay();
    var monthLength = cal_days_in_month[this.month];
    if(this.month == 1) {
        if((this.year % 4 == 0 && this.year % 100 != 0) || this.year % 400 == 0){
            monthLength = 29;
        }
    }
    var monthName = cal_months_labels[this.month];
    var html = '<table class="recurringDateCalendar">';
    html += '<tr><th colspan="7">';
    html += monthName + "&nbsp;" + this.year;
    html += '</th></tr>';
    html += '<tr class="recurringDateCalendar_header">';
    for(var i=0; i<=6; i++){
        html += '<td class="recurrindDateCalendar_header_day">';
        html += cal_days_labels[i];
        html += '</td>';
    }
    html += '</tr><tr>';
    var day = 1;
    for(var i=0; i<9; i++) {
        for(var j=0; j<=6; j++) {
            html += '<td class="recurringDateCalendar_day">';
            if(day <= monthLength && (i > 0 || j >= startingDay)) {
                html += day;
                day++;
            }
            html += '</td>';
        }
        if(day > monthLength) {
            break;
        }else{
            html += '</tr><tr>';
        }
    }
    html += '</tr></table>';
    this.html = html;
}

Calendar.prototype.getHTML = function() {
    return this.html;
}

$(function(){
        var cal = new Calendar();
        cal.generateHTML();
        $('.recurringDateInput').append(cal.getHTML());
        $('.recurringDateInput').append('\n<label for="recur_type">Options:</label>\n<input type="radio" name="recur_type" value="none" />One Day\n<input type="radio" name="recur_type" value="multi" />Multiple Days\n<input type="radio" name="recur_type" value="daily" />Repeats Daily\n<input type="radio" name="recur_type" value="weekly" />Repeats Weekly\n<input type="radio" name="recur_type" value="monthly" />Repeats Monthly\n<input type="radio" name="recur_type" value="yearly" />Repeats Yearly');
});
