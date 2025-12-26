from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

AUDIO_QUALITY = "192k"
YTDLPATH = r"C:\Users\pranj\AppData\Roaming\Python\Python313\Scripts\yt-dlp.exe"
OUTPUT_TEMPLATE = r"D:\downloads\%(title)s.%(ext)s"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        subprocess.run(
            [
                YTDLPATH,
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", AUDIO_QUALITY,
                "-o", OUTPUT_TEMPLATE,
                url
            ],
            check=True
        )
        return jsonify({"status": "Download complete"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed", "details": str(e)}), 500 #jsonify le json banauncha which is better to send back
    # rather than dictionary


if __name__ == "__main__":
    app.run(debug=True)