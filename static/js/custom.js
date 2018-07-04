$(document).ready(function() {
    timePicker = $(".time-picker");
    timePicker.timepicker({ timeFormat: 'H:i',
                            scrollDefault: 'now' });
    timePicker.click (function () {
        $(".ui-timepicker-wrapper").css("width", $(this).css("width"))
    });

    $("label:has(input.form-check-input)").addClass("form-check-label");
    $("li:has(label.form-check-label)").addClass("form-check");

    $("#id_load_image").change(function(){
        if ($(this)[0].files.length === 0) {
            $(this).siblings("[for='load_image']").html("");
        }
        else if ($(this)[0].files.length === 1) {
            $(this).siblings("[for='load_image']").html($(this)[0].files[0].name);
        }
        else if ($(this)[0].files.length > 1) {
            $(this).siblings("[for='load_image']").html($(this)[0].files.length + " File selezionati");
        }
    })

    $('#list-loaded-images').delegate(".listelement", "click", function() {
        alert('miao');
		var elemid = $(this).attr('data-id');
		$("#loaded_"+elemid).remove();
    });
});