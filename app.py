from flask import Flask, request, jsonify,url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
import itertools
from globals import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")



@app.route('/post_comment', methods=['POST'])
def post_comment():
    data = request.json
    streamer_id = data.get('session_id')
    comment = data.get('comment')
    print("post Comment/ session id", streamer_id, "comment is: ", comment)
    # if streamer_id in streamers:
    #     COMMENTS[streamer_id].append(comment)
    #     socketio.emit('new_comment', {'comment': comment}, to=streamers[streamer_id])
    #     return jsonify({'status': 'success'}), 200
    # else:
    #     return jsonify({'status': 'streamer not found'}), 404
    # TODO: ALways return now for testing, need to delete the following the uncomment the previous part
    COMMENTS[streamer_id].append(comment)
    socketio.emit('new_comment', {'comment': comment}, to=streamers[streamer_id])
    return jsonify({'status': 'success'}), 200

@app.route('/get_comments')
def get_comments():
    streamer_id = request.args.get('streamerId')
    index = int(request.args.get('index', -1))
    limit = int(request.args.get('limit', 3))

    if streamer_id not in COMMENTS:
        return jsonify({"error": "Streamer ID not found"}), 404
    # Check if the index is within the range of the comments list
    comment_list = COMMENTS[streamer_id]
    if index >= len(comment_list) or index == -1:
        next_url = url_for('get_comments', streamerId=streamer_id, index=len(comment_list), limit=limit, _external=True)
        r_comments = comment_list[-1] if len(comment_list) and index == -1 else []
        return jsonify({"comments": r_comments, "links": {"self": next_url,
                                                  "next":next_url}}), 200  # or 404 if you prefer to indicate "out of range"

    # Slice the comments array to get the requested chunk
    end_index = min(index + limit, len(comment_list))
    print(comment_list, index, end_index)
    chunk = list(itertools.islice(comment_list, index, end_index))

    # Prepare the HATEOAS links for the next set of comments
    next_index = end_index
    next_url = url_for('get_comments', streamerId=streamer_id, index=next_index, limit=limit, _external=True)

    # Construct the response
    response = {
        "comments": chunk,
        "links": {
            "self": url_for('get_comments', streamerId=streamer_id, index=index, limit=limit, _external=True),
            "next": next_url
        }
    }
    
    return jsonify(response)

@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    streamer_id = None
    for sid, id in streamers.items():
        if id == request.sid:
            streamer_id = sid
            break
    
    if streamer_id:
        # Perform cleanup for the disconnecting streamer
        del streamers[streamer_id]
        if streamer_id in COMMENTS:
            del COMMENTS[streamer_id]  
        print(streamers,COMMENTS)
        print(f'Client {streamer_id} disconnected')
    else:
        print('Client disconnected')
@socketio.on('register_streamer')
def handle_register(data):
    streamer_id = data['streamer_id']
    streamers[streamer_id] = request.sid
    emit('registration', {'status': 'registered successfully'})

if __name__ == '__main__':
    socketio.run(app, port=5000, host='0.0.0.0')
