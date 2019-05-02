$(document).ready(function () {
    const USER_URL = '/api/user/';

    $('#login_form').on('submit', function(e){
        e.preventDefault();
        var $that = $(this), formData = new FormData($that.get(0));
        let username = formData.get('username');
        let password = formData.get('password');
        formData = JSON.stringify({'username': username, 'password': password});
        sendRequest(formData, USER_URL, 'post', getResult);
    });

    function getResult(callback){
        if (callback.result && !callback.error) {
            window.location.replace('/');
        } else {
            $('#error').html(callback.error);
        }
    }
});