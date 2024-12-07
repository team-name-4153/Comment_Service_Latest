import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server")
    sio.emit('register_streamer', {'streamer_id': 'streamer123'})

@sio.event
def new_comment(data):
    print("New comment received:", data['comment'])

@sio.event
def registration(data):
    print(data['status'])

sio.connect('http://localhost:5000')
sio.wait()
