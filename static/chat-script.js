// static/chat-script.js
var socket = io.connect('http://' + document.domain + ':' + location.port);

var username = decodeURIComponent(new URLSearchParams(window.location.search).get('username'));
var room = decodeURIComponent(new URLSearchParams(window.location.search).get('room'));

socket.emit('join', {'username': username, 'room': room});

socket.on('message', function(data) {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += '<p><strong>' + data.username + ':</strong> ' + data.text + '</p>';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

socket.on('load_messages', function(data) {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = ''; // Clear existing messages
    data.messages.forEach(function(msg) {
        messagesDiv.innerHTML += '<p><strong>' + msg.username + ':</strong> ' + msg.text + '</p>';
    });
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

socket.on('load_data', function(data) {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = ''; // Clear existing messages
    data.messages.forEach(function(msg) {
        messagesDiv.innerHTML += '<p><strong>' + msg.username + ':</strong> ' + msg.text + '</p>';
    });
    
    // Display connection and disconnection events
    data.events.forEach(function(event) {
        if (event.event_type === 'connect') {
            messagesDiv.innerHTML += '<p><em>' + event.username + ' has joined the room.</em></p>';
        } else if (event.event_type === 'disconnect') {
            messagesDiv.innerHTML += '<p><em>' + event.username + ' has left the room.</em></p>';
        }
    });

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

function sendMessage() {
    var messageInput = document.getElementById('message_input');
    var messageText = messageInput.value.trim();
    if (messageText !== '') {
        socket.emit('message', {'text': messageText});
        messageInput.value = '';
    }
}
