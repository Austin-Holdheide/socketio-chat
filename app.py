from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import json
from time import time
import os  # Add this import for handling file paths

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cv4u8fvj8wr5tijm8345tjiwuj-5t80tu'
socketio = SocketIO(app)

# Define the folder path
JSON_FOLDER = 'chatjson'

# Create the folder if it doesn't exist
os.makedirs(JSON_FOLDER, exist_ok=True)

def write_data_to_json(room, data):
    filename = os.path.join(JSON_FOLDER, f'{room}_data.json')
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def read_data_from_json(room):
    filename = os.path.join(JSON_FOLDER, f'{room}_data.json')
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return {'messages': []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        session['username'] = username
        session['room'] = room
        data = read_data_from_json(room)
        return render_template('chat.html', room=room, data=data)
    else:
        return redirect(url_for('index'))

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    session['username'] = username
    session['room'] = room
    join_room(room)

    # Load previous messages for the chat room
    data = read_data_from_json(room)
    messages = data.get('messages', [])
    emit('load_messages', {'messages': messages})

        # Log connect message as a regular message
    connect_message = f'{username} has joined the room.'
    data['messages'].append({'username': 'Server', 'text': connect_message, 'timestamp': int(time())})
    write_data_to_json(room, data)

    emit('message', {'username': 'Server', 'text': connect_message}, room=room)
    print('Client connected')

    

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username', 'Anonymous')
    room = session.get('room', 'default')
    leave_message = f'{username} has left the room.'

    # Log disconnect message as a regular message
    data = read_data_from_json(room)
    data['messages'].append({'username': 'Server', 'text': leave_message, 'timestamp': int(time())})
    write_data_to_json(room, data)

    emit('message', {'username': 'Server', 'text': leave_message}, room=room)
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    room = session.get('room', 'default')
    text = data['text']

    data = read_data_from_json(room)
    data['messages'].append({'username': username, 'text': text, 'timestamp': int(time())})
    write_data_to_json(room, data)

    emit('message', {'username': username, 'text': text}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
