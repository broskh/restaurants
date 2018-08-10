$(document).ready(function() {
    let timePicker = $(".time-picker");
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
    });

    $('#list-loaded-images').delegate(".listelement", "click", function() {
        alert('miao');
        let elemid = $(this).attr('data-id');
        $("#loaded_"+elemid).remove();
    });

    $('#datetimepicker').datetimepicker({
        inline: true,
        sideBySide: true,
        minDate: new Date(),
        icons: {
            time: 'fa fa-time',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down',
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-screenshot',
            clear: 'fa fa-trash',
            close: 'fa fa-remove'
        },
        format: 'YYYY MMMM D H m'
    });

    $("input[type='radio'][name='type']").change(function(){
        if (this.value === 'Ristorante') {
            $("#restaurant-registration").removeClass('collapse')
        }
        else {
            $("#restaurant-registration").addClass('collapse')
        }
    });
});