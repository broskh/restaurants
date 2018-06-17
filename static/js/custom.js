$(document).ready(function() {
    $(".time-picker").timepicker({  timeFormat: 'H:i',
                                    scrollDefault: 'now' });
    $(".time-picker").click (function () {
        $(".ui-timepicker-wrapper").css("width", $(this).css("width"))
    });
    // $(".ui-timepicker-list").css("background-color", "black")
    // $(".ui-timepicker-wrapper").css("width", $(".time-picker").css("width"))
});