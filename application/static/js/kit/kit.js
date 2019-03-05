$(document).ready(function () {
    $('.edit-kit').hide();

    const KIT_URL = '/api/kit/';
    var error = $('#error');
    var last_kit_pressed = null;

    $('.edit_button').on('click', function(e){
        let name = this.getAttribute('data-name');
        let active = this.getAttribute('data-active');

        $('.create-kit').hide();
        $('.edit-kit').show();

        $('#name_of_editing_kit').html(name);

        last_kit_pressed = name;
        if (active == 'True'){
            $('#edit_form_kit_active').attr( "checked", 'on' );
        } else {
            $('#edit_form_kit_active').attr( "checked", null );
        }
    });

    $('.delete_button').on('click', function(e){
        let name = this.getAttribute('data-name');

        sendRequest({}, KIT_URL + name + '/', 'delete', updatePage);
    });

    $('#cancel_edition').on('click', function(e){
        e.preventDefault();
        $('.create-kit').show();
        $('.edit-kit').hide();
    });

    $('#edit_form').on('submit', function(e){
        e.preventDefault();
        var $that = $(this), formData = new FormData($that.get(0));
        let name = formData.get('kit_name');

        let active = '0';
        if (formData.get('kit_active') !== null) {
            active = '1';
        }
        formData = JSON.stringify({'kit_name': name});
        sendRequest(formData, KIT_URL + last_kit_pressed + '/' + active + '/', 'patch', updatePage);
    });

    $('#create_form').on('submit', function(e){
        e.preventDefault();
        var $that = $(this), formData = new FormData($that.get(0));
        let name = formData.get('kit_name');
        let active = '0';
        if (formData.get('kit_active') !== null) {
            active = '1';
        }
        formData = JSON.stringify({'kit_name': name});
        sendRequest(formData, KIT_URL + name + '/' + active + '/', 'post', updatePage);
    });

    function updatePage(callback){
        if (callback.result) {
            location.reload();
        } else if (callback.error) {
            alert(callback.error);
        }
    }
});