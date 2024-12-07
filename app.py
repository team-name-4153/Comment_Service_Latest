from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dictionary to keep track of streamers and their sockets
streamers = {}

@app.route('/post_comment', methods=['POST'])
def post_comment():
    data = request.json
    streamer_id = data.get('streamer_id')
    comment = data.get('comment')

    if streamer_id in streamers:
        socketio.emit('new_comment', {'comment': comment}, to=streamers[streamer_id])
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'streamer not found'}), 404

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('register_streamer')
def handle_register(data):
    streamer_id = data['streamer_id']
    streamers[streamer_id] = request.sid
    emit('registration', {'status': 'registered successfully'})

if __name__ == '__main__':
    socketio.run(app)
