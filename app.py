import subprocess
import os
import uuid
from flask import Flask, jsonify, request, render_template
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = Flask(__name__)

AUDIO_QUALITY = "192k"
YTDLPATH = r"C:\Users\pranj\AppData\Roaming\Python\Python313\Scripts\yt-dlp.exe"
SUPABASE_URL = "https://khmbshckipejanszmaed.supabase.co"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "mp3-storage"  # gets stored here


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Generate unique filename per request
    filename = f"{uuid.uuid4()}.mp3"

    # Step 1: Download MP3 locally
    subprocess.run([
        YTDLPATH,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", AUDIO_QUALITY,
        "-o", filename,
        url
    ], check=True)

    # Step 2: Upload to Supabase
    with open(filename, "rb") as f:
        supabase.storage.from_(BUCKET_NAME).upload(filename, f)


    # Step 3: Generate signed URL (1 hour)
    signed_url_result = supabase.storage.from_(BUCKET_NAME).create_signed_url(filename, 3600, options = {"download": True})

    # Handle dict or string
    if isinstance(signed_url_result, dict):
        mp3_url = signed_url_result.get('signedURL') or signed_url_result.get('signed_url')
    else:
        mp3_url = signed_url_result

    # Step 4: Delete local file
    os.remove(filename)

    # Step 5: Return URL to frontend
    return jsonify({"mp3_url": mp3_url})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
