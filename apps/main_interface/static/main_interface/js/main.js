function main() {
    var namespace = '/test'; // change to an empty string to use the global namespace
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function (msg) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    });
    // event handler for new connections
    socket.on('connect', function () {
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('form#emit').submit(function (event) {
        console.log('sending message');
        socket.emit('my event', {data: $('#emit_data').val()});
        return false;
    });
    $('form#broadcast').submit(function (event) {
        socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
        return false;
    });
    $('form#join').submit(function (event) {
        socket.emit('join', {room: $('#join_room').val()});
        return false;
    });
    $('form#leave').submit(function (event) {
        socket.emit('leave', {room: $('#leave_room').val()});
        return false;
    });
    $('form#send_room').submit(function (event) {
        socket.emit('my room event', {room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });
    $('form#close').submit(function (event) {
        socket.emit('close room', {room: $('#close_room').val()});
        return false;
    });
    $('form#disconnect').submit(function (event) {
        socket.emit('disconnect request');
        return false;
    });
}

// start things off
$(document).ready(main);
