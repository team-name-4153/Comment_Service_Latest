import requests

def post_comment(streamer_id, comment):
    url = 'http://localhost:5000/post_comment'  # Update this URL based on your server configuration
    data = {
        'streamer_id': streamer_id,
        'comment': comment
    }
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Comment posted successfully:", response.json())
    else:
        print("Failed to post comment:", response.json())

# Example usage
post_comment('streamer123', 'Hello, this is a test comment from the audience!')
