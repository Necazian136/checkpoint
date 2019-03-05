$(document).ready(function () {

    $('.edit-plate').hide();

    const PLATE_URL = '/api/plate/' + $('body').attr('data-kit-name') + '/';
    console.log(PLATE_URL);
    var error = $('#error');
    var last_plate_pressed = null;

    $('.edit_button').on('click', function(e){
        let name = this.getAttribute('data-name');

        $('.create-plate').hide();
        $('.edit-plate').show();

        $('#name_of_editing_plate').html(name);

        last_plate_pressed = name;
    });

    $('.delete_button').on('click', function(e){
        let name = this.getAttribute('data-name');
        sendRequest('{}', PLATE_URL + name + '/', 'delete', updatePage);
    });

    $('#cancel_edition').on('click', function(e){
        e.preventDefault();
        $('.create-plate').show();
        $('.edit-plate').hide();
    });

    $('#edit_form').on('submit', function(e){
        e.preventDefault();
        var $that = $(this), formData = new FormData($that.get(0));
        let name = formData.get('plate_name');

        formData = JSON.stringify({'plate_name': name});
        sendRequest(formData, PLATE_URL + last_plate_pressed + '/', 'patch', updatePage);
    });

    $('#create_form').on('submit', function(e){
        e.preventDefault();
        var $that = $(this), formData = new FormData($that.get(0));
        let name = formData.get('plate_name');

        formData = JSON.stringify({'plate_name': name});
        sendRequest(formData, PLATE_URL + name + '/', 'post', updatePage);
    });

    function updatePage(callback){
        if (callback.result) {
            location.reload();
        } else if (callback.error) {
            alert(callback.error);
        }
    }
});