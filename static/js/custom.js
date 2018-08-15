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
        let elemid = $(this).attr('data-id');
        $("#loaded_"+elemid).remove();
    });

    $('.datetimepicker').datetimepicker({
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
        if (this.value === '3') {
            $("#restaurant-registration").removeClass('collapse')
        }
        else {
            $("#restaurant-registration").addClass('collapse')
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
        // id = $(this).data('id');
        // csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        // url = $(this).data('url');
        // $.ajax({
        //     url: url,
        //     data: { 'id' : id },
        //     method: 'POST',
        //     beforeSend: function(xhr) {
        //         xhr.setRequestHeader("X-CSRFToken", csrf_token);
        //     },
        //     success: function(){
        //         $("#loaded_"+id).remove();
        //     }
        // });
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
        input_name.val('');
        input_price.val('');
        let new_voice_id = 'new-voice-'+new Date().getTime();
        let new_category_element = '<li class="list-group-item new" data-id="'+new_voice_id+'">\n'+
                                    '<span>'+voice_name+' - '+voice_price+'€</span>\n'+
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
    });

    $(".delete-category").click(function() {
        deleteCategory($(this));
    });

    $(".delete-voice").click(function() {
        deleteVoice($(this));
    });

    let restaurant_detail_datetimepicker = $("#restaurant_detail_datetimepicker");
    restaurant_detail_datetimepicker.on("dp.change",function (e) {
        $("#id_start_time").val(e.date.format("YYYY-MM-DD-h-m-s"));
    });
    if(restaurant_detail_datetimepicker.length){
        $("#id_start_time").val(restaurant_detail_datetimepicker.data("DateTimePicker").viewDate().format("YYYY-MM-DD-h-m-s"));
    }
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