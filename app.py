from flask import Flask, Response, stream_with_context
import random
import requests

app = Flask(__name__)

eypz = [
    "https://aemt.me/file/1wyRPkzAYgts.mp4",
    "https://i.imgur.com/8QiXNLt.mp4"
]

@app.route('/')
def home():
    return 'API is running somewhere!'

@app.route('/video', methods=['GET'])
def anime():
    video_url = random.choice(eypz)
    app.logger.info(f"Selected video URL: {video_url}")

    @stream_with_context
    def generate():
        try:
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                content_length = r.headers.get('Content-Length')
                app.logger.info(f"Content-Length: {content_length}")

                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
        except requests.RequestException as e:
            app.logger.error(f"Error fetching video: {e}")
            yield b''

    response = Response(generate(), content_type='video/mp4')
    response.headers["Content-Disposition"] = "inline; filename=video.mp4"
    response.headers["Accept-Ranges"] = "bytes"
    return response

if __name__ == '__main__':
    app.run(port=3000, debug=True)
