$(document).ready(function() {
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": $.cookie("csrftoken") }
        });
    });

    $(".date-picker").datepicker({
        format: 'dd/mm/yyyy',
        startDate: new Date() });

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
        let elemid = $(this).attr('data-id');
        $("#loaded_"+elemid).remove();
    });

    let datetimepicker = $('.datetimepicker');
    let default_date = datetimepicker.data('start');
    if (!default_date) {
        default_date = false;
    }
    else {
        default_date = new Date(default_date);
        if (default_date < new Date()) {
            default_date = false;
        }
    }
    datetimepicker.datetimepicker({
        inline: true,
        sideBySide: true,
        minDate: new Date(),
        defaultDate: default_date,
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
    let client_bookings_datetimepicker = $(".client_bookings_datetimepicker");
    client_bookings_datetimepicker.each(function () {
        default_date = $(this).data('start');
        if (!default_date) {
            default_date = false;
        }
        else {
            default_date = new Date(default_date);
        if (default_date < new Date()) {
            default_date = false;
        }
        }
        $(this).datetimepicker({
            inline: true,
            sideBySide: true,
            defaultDate: default_date,
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
    });

    $("input[type='radio'][name='user_type']").change(function(){
        if (this.value === '2') {
            $("#restaurant-registration").removeClass('collapse');
        }
        else {
            $("#restaurant-registration").addClass('collapse');
        }
    });

    $(".delete-image-button").click(function() {
        let li = $(this).closest('li');
        let hidden_categories = $('#id_remove_images');
        let array = hidden_categories.val();
        if (array === "") {
            array = [li.data('id')];
        }
        else {
            array = array instanceof Array ? array : [array];
            array.push(li.data('id'));
        }
        hidden_categories.val(array);
        li.remove();
    });

    $("#add-menu-category").click(function() {
        let input = $(this).siblings("input");
        let category_name = input.val();
        input.val('');
        let new_category_id = 'new-category-'+new Date().getTime();
        let new_category_element = '<a class="list-group-item list-group-item-action active new" data-id="'+new_category_id+'" id="'+new_category_id+'" data-toggle="list" href="#voices-'+new_category_id+'" role="tab" aria-controls="'+new_category_id+'">\n'+
                                    category_name+'\n'+
                                    '<button type="button" class="delete-category btn btn-default ml-auto">\n'+
                                        '<span class="fa fa-trash"></span>\n'+
                                    '</button>\n'+
                                '</a>';
        let menu_categories = $('#menu-categories');
        menu_categories.find('.list-group-item').removeClass('active');
        menu_categories.append(new_category_element);

        let new_voices_element = '<div class="tab-pane fade show active" id="voices-'+new_category_id+'" role="tabpanel" aria-labelledby="'+new_category_id+'">\n'+
                                    '<ul class="list-group">\n'+
                                    '</ul>\n'+
                                '</div>';
        let menu_voices = $('#menu-voices');
        menu_voices.find('.tab-pane').removeClass('active');
        menu_voices.append(new_voices_element);
        $('#add-menu-voice').closest('div').removeClass('collapse');

        let hidden_categories = $('#id_add_categories');
        let array = hidden_categories.val();
        let element = {
            'id': new_category_id,
            'name': category_name,
        };
        if (array === "") {
            array = [element];
        }
        else {
            array = JSON.parse(array);
            array.push(element);
        }
        hidden_categories.val(JSON.stringify(array));

        $(".delete-category").click(function() {
            deleteCategory($(this));
        });
    });

    $("#add-menu-voice").click(function() {
        let input_name = $('#new-voice-name');
        let input_price = $('#new-voice-price');
        let voice_name = input_name.val();
        let voice_price = input_price.val();
        if (!isFloat(voice_price) && !isInt(voice_price)) {
            $('#new-voice').after('<div class="margin-top-15 alert alert-danger alert-dismissible">\n' +
                    '  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\n' +
                    '  Il prezzo inserito non è valido' +
                    '</div>');
        }
        else {
            input_name.val('');
            input_price.val('');
            let new_voice_id = 'new-voice-'+new Date().getTime();
            let new_category_element = '<li class="list-group-item new" data-id="'+new_voice_id+'">\n'+
                                        '<span>'+voice_name+' - '+Number.parseFloat(voice_price).toFixed(2)+'€</span>\n'+
                                            '<button type="button" class="delete-voice btn ml-auto btn-default">\n'+
                                                '<span class="fa fa-trash"></span>\n'+
                                            '</button>\n'+
                                    '</li>';
            let div = $('#menu-voices').find('div.active');
            let voices_ul = div.find('ul').first();
            voices_ul.append(new_category_element);

            let hidden_voices = $('#id_add_voices');
            let array = hidden_voices.val();
            let element = {
                'id': new_voice_id,
                'category_id': $('#'+div.attr('aria-labelledby')).data('id'),
                'name': voice_name,
                'price': voice_price
            };
            if (array === "") {
                array = [element];
            }
            else {
                array = JSON.parse(array);
                array.push(element);
            }
            hidden_voices.val(JSON.stringify(array));

            $(".delete-voice").click(function() {
                deleteVoice($(this));
            });
        }
    });

    $(".delete-category").click(function() {
        deleteCategory($(this));
    });

    $(".delete-voice").click(function() {
        deleteVoice($(this));
    });

    let restaurant_detail_datetimepicker = $("#restaurant_detail_datetimepicker");
    restaurant_detail_datetimepicker.on("dp.change",function (e) {
        $("#id_start_time").val(e.date.format("YYYY-MM-DD-H-m-s"));
        $("#booking-availability").html('');
        $("#book-button").prop('disabled', true);
    });
    if(restaurant_detail_datetimepicker.length){
        $("#id_start_time").val(restaurant_detail_datetimepicker.data("DateTimePicker").viewDate().format("YYYY-MM-DD-H-m-s"));
    }

    client_bookings_datetimepicker.on("dp.change",function (e) {
        let result_element = $(this).closest('.result-element');
        result_element.find("input[name='start_time']").val(e.date.format("YYYY-MM-DD-H-m-s"));
        result_element.find(".booking-availability-for-edit").html('');
        result_element.find(".save-edit-booking").prop('disabled', true);
    });

    $(".delete-client-booking").click(function() {
        let button = $(this);
        let id = $(this).closest('.result-element').data('id');
        let url = button.data('url');
        $.ajax({
            url: url,
            data: { 'id' : id },
            method: 'POST',
            success: function(){
                button.closest('.result-element').remove();
            }
        });
    });

    let save_edit_booking = $('.save-edit-booking');
    if (save_edit_booking.length > 0) {
        save_edit_booking.closest('.result-element').find("input[name='n_places']").on('input', function() {
            $(this).closest('.result-element').find('.save-edit-booking').prop('disabled', true);
        });
    }

    $(".check-availability-for-edit").click(function() {
        let button = $(this);
        let result_element = $(this).closest('.result-element');
        let url = button.data('url');
        let n_places = result_element.closest('.result-element').find("input[name='n_places']").val();
        let start_time = result_element.find("input[name='start_time']").val();
        let booking_id = result_element.data('id');
        let id = button.data('restaurant_id');
        let client_id = button.data('client_id');
        if (!isInt(n_places)) {
            $("#booking-availability").html('Dati inseriti non validi');
        }
        else {
            $.ajax({
                url: url,
                data: { 'restaurant_id' : id,
                        'n_places' : n_places,
                        'start_time' : start_time,
                        'booking_id' : booking_id ,
                        'client_id' : client_id },
                method: 'POST',
                success: function(response){
                    let save_button = result_element.find(".save-edit-booking");
                    if (response['state'] === 1) {
                        result_element.find(".booking-availability-for-edit").html('Disponibile');
                        save_button.html('Salva');
                        save_button.prop('disabled', false);
                        result_element.find("input[name='state']").val(response['state']);
                    }
                    else if (response['state'] === 0) {
                        result_element.find(".booking-availability-for-edit").html('Non Disponibile');
                        save_button.html('Vai in coda');
                        save_button.prop('disabled', false);
                        result_element.find("input[name='state']").val(response['state']);
                    }
                    else {
                        result_element.find(".booking-availability-for-edit").html('Prenotazione già esistente');
                    }
                }
            });
        }
    });

    save_edit_booking.click(function() {
        let button = $(this);
        let result_element = button.closest('.result-element');
        let id = result_element.data('id');
        let start_time = result_element.find("input[name='start_time']").val();
        let state = result_element.find("input[name='state']").val();
        let n_places = result_element.find("input[name='n_places']").val();
        let url = button.data('url');
        $.ajax({
            url: url,
            data: { 'id' : id,
                 'n_places' : n_places,
                 'start_time' : start_time,
                 'state' : state },
            method: 'POST',
            success: function(){
                button.closest('.result-element').append('<div class="alert alert-success alert-dismissible">\n' +
                    '  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\n' +
                    '  Modifica avvenuta con successo' +
                    '</div>');
            }
        });
    });

    $(".client-edit-booking").click(function() {
        let i = $(this).find('i');
        if (i.hasClass('fa-chevron-down')) {
            i.removeClass('fa-chevron-down');
            i.addClass('fa-chevron-up');
        }
        else {
            i.removeClass('fa-chevron-up');
            i.addClass('fa-chevron-down');
        }
    });

    if ($('#book-button').length > 0) {
        $( "#id_n_places" ).on('input', function() {
            $("#book-button").prop('disabled', true);
        });
    }

    $("#check-availability").click(function() {
        let button = $(this);
        let url = button.data('url');
        let n_places_element = $("#id_n_places");
        let n_places = n_places_element.val();
        let start_time = $("#id_start_time").val();
        let restaurant_id = button.data('restaurant_id');
        let client_id = button.data('client_id');
        if (!isInt(n_places)) {
            $("#booking-availability").html('Dati inseriti non validi');
        }
        else {
            $.ajax({
                url: url,
                data: { 'restaurant_id' : restaurant_id,
                        'n_places' : n_places,
                        'client_id' : client_id,
                        'start_time' : start_time },
                method: 'POST',
                success: function(response){
                    let book_button = $("#book-button");
                    if (response['state'] === 1) {
                        $("#booking-availability").html('Disponibile');
                        book_button.val('Prenota');
                        book_button.prop('disabled', false);
                        $("#id_state").val(response['state']);
                    }
                    else if (response['state'] === 0) {
                        $("#booking-availability").html('Non disponibile');
                        book_button.val('Vai in coda');
                        book_button.prop('disabled', false);
                        $("#id_state").val(response['state']);
                    }
                    else {
                        $("#booking-availability").html('Prenotazione già esistente');
                    }
                }
            });
        }
    });

    $("#restaurant_bookings_datetimepicker").on("dp.change",function (e) {
        let url = $(this).data('url');
        let time = e.date.format("YYYY-MM-DD-H-m-s");
        let id =$(this).data('id');
        $.ajax({
            url: url,
            data: { 'restaurant_id' : id,
                 'time' : time },
            method: 'POST',
            success: function(response){
                $('#places-reserved').html(response['occupied_places']);
            }
        });
    });

   $("input[type='checkbox']").closest('label').css('margin-bottom', '0');
});

function deleteCategory(button) {
    let a = button.closest('a');
    let voices = $("#voices-"+a.attr('id'));
    let category_id = a.data('id');

    if (!a.hasClass('new')) {
        let hidden_categories = $('#id_remove_categories');
        let array = hidden_categories.val();
        if (array === "") {
            array = [category_id];
        }
        else {
            array = array instanceof Array ? array : [array];
            array.push(category_id);
        }
        hidden_categories.val(array);

        voices.find('li').each(function () {
            let voice_id = $(this).data('id');
            if (!$(this).hasClass('new')) {
                let hidden_voices = $('#id_remove_voices');
                array = hidden_voices.val();
                if (array === "") {
                    array = [voice_id];
                }
                else {
                    array = array instanceof Array ? array : [array];
                    array.push(voice_id);
                }
                hidden_voices.val(array);
            }
        });
    }
    else {
        let hidden_add_categories = $('#id_add_categories');
        let array = JSON.parse(hidden_add_categories.val());
        for(let i=0; i < array.length; i++) {
           if (array[i]['id'] === category_id) {
                array.splice(i, 1);
                i--;
            }
        }
        hidden_add_categories.val(JSON.stringify(array));

        let hidden_add_voices = $('#id_add_voices');
        array = hidden_add_voices.val();
        if (array === "") {
            array = '[]'
        }
        array = JSON.parse(array);
        for(let i=0; i < array.length; i++) {
           if (array[i]['category_id'] === category_id) {
                array.splice(i, 1);
                i--;
            }
        }
        hidden_add_voices.val(JSON.stringify(array));
    }
    a.remove();
    voices.remove();

    if ($('#menu-categories').find('a.list-group-item').length === 0) {
        $('#new-voice').addClass('collapse');
    }
}

function deleteVoice(button) {
    let voice = button.closest('li');
    let voice_id = voice.data('id');
    if (!voice.hasClass('new')) {
        let hidden_voices = $('#id_remove_voices');
        let array = hidden_voices.val();
        if (array === "") {
            array = [voice_id];
        }
        else {
            array = array instanceof Array ? array : [array];
            array.push(voice_id);
        }
        hidden_voices.val(array);
    }
    else {
        let hidden_add_voices = $('#id_add_voices');
        let array = JSON.parse(hidden_add_voices.val());
        for(let i=0; i < array.length; i++) {
           if (array[i]['id'] === voice_id) {
                array.splice(i, 1);
                i--;
            }
        }
        hidden_add_voices.val(JSON.stringify(array));
    }
    voice.remove();
}

function isInt(value) {
    return !isNaN(value) && !isNaN(parseInt(value, 10));
}

function isFloat(inputtxt) {
    let decimal = /^[-+]?[0-9]+\.[0-9]+$/;
    return inputtxt.match(decimal)
}