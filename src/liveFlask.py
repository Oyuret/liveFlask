import subprocess
from flask import Flask
from flask import request
app = Flask(__name__)

livestreamer = 0

@app.route("/stream/play/<service>/<streamer>", methods = ['GET'])
def hello(service, streamer):
    global livestreamer

    if(isinstance(livestreamer,subprocess.Popen)):
        terminate_stream(livestreamer)

    livestreamer = subprocess.Popen(["livestreamer", service + "/" + streamer, "best", "-np", "omxplayer -o hdmi --win \"40 25 1880 1055\""])
    return "Opening stream"


@app.route("/stream/play", methods = ['POST'])
def start_stream():
    global livestreamer

    if(isinstance(livestreamer,subprocess.Popen)):
        terminate_stream(livestreamer)

    if not request.json or not 'url' in request.json:
        return "Fel i url"

    livestreamer = subprocess.Popen(["livestreamer", request.json['url'], "best", "-np", "omxplayer -o hdmi --win \"40 25 1880 1055\""])
    return "Opening stream"

@app.route("/stream/stop", methods = ['GET'])
def stop_stream():
    global livestreamer

    if(isinstance(livestreamer,subprocess.Popen)):
        terminate_stream(livestreamer)
    
    return "Stopping stream"


@app.route('/shutdown', methods=['GET'])
def shutdown():
    global livestreamer
    if(isinstance(livestreamer,subprocess.Popen)):
        terminate_stream(livestreamer)
    shutdown_server()
    return 'Server shutting down...'


def terminate_stream(livestreamer):
    if(livestreamer.poll() is None):
        subprocess.call(["killall", "omxplayer.bin"])
        livestreamer.wait()
        return
    else:
        return

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, debug=True)
