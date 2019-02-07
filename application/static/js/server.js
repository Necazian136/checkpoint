function sendRequest(data, functionName, url, method) {
    $.ajax({
        type: method,
        url: url,
        dataType: 'json',
        contentType: false,
        processData: false,
        data: data
    }).done(function (callback) {
        functionName(callback);
    });
}