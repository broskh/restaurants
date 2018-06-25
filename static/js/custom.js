$(document).ready(function() {
    $(".time-picker").timepicker({  timeFormat: 'H:i',
                                    scrollDefault: 'now' });
    $(".time-picker").click (function () {
        $(".ui-timepicker-wrapper").css("width", $(this).css("width"))
    });
     $("label:has(input.form-check-input)").addClass("form-check-label");
     $("li:has(label.form-check-label)").addClass("form-check");
});