from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")


# Dictionary to keep track of streamers and their sockets
streamers = {}
# Middleware for logging
@app.before_request
async def log_request():
    request.start_time = time.time()  # Record the start time
    request_data = await request.get_data()  # Get request data if needed
    app.logger.info(f'Before Request: Method={request.method}, Path={request.path}, Body={request_data.decode()}')

@app.after_request
async def log_response(response):
    duration = time.time() - request.start_time  # Calculate how long the request took
    app.logger.info(f'After Request: Method={request.method}, Path={request.path}, Status={response.status_code}, Duration={duration:.2f} sec')
    return response

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
