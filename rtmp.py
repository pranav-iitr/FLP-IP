from flask import Flask, Response, request
import subprocess

app = Flask(__name__)

@app.route("/live/<stream_key>", methods=["POST"])
def live(stream_key):
    ffmpeg_cmd = [
        'ffmpeg', 
        '-i', 'pipe:0', 
        '-c', 'copy', 
        '-f', 'flv', 
        f'rtmp://localhost:1935/live/{stream_key}'
    ]

    p = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    p.communicate(request.data)
    return Response(status=200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
