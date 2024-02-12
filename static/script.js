// static/script.js
var socket = io.connect('http://' + document.domain + ':' + location.port);

document.getElementById('joinForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var username = document.getElementById('username').value.trim();
    var room = document.getElementById('room').value.trim();
    if (username !== '' && room !== '') {
        socket.emit('join', {'username': username, 'room': room});
        window.location.href = '/chat?username=' + encodeURIComponent(username) + '&room=' + encodeURIComponent(room);
    }
});
