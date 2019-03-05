function sendRequest(data, url, method, functionName) {
    $.ajax({
        type: method,
        url: url,
        dataType: 'json',
        contentType: 'application/json',
        data: data
    }).done(function (callback) {
        functionName(callback);
    });
}