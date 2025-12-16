from flask import Flask, render_template, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        format_type = request.form["format"]
        quality = request.form["quality"]
        filename = f"{uuid.uuid4()}.%(ext)s"

        # Default command
        ytdlp_cmd = ["yt-dlp", "-o", filename]

        # Format & quality handling
        if format_type == "mp3":
            ytdlp_cmd += ["-x", "--audio-format", "mp3"]
        else:  # mp4 video
            if quality == "best":
                ytdlp_cmd += ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"]
            else:
                ytdlp_cmd += ["-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"]

        ytdlp_cmd.append(url)

        try:
            subprocess.run(ytdlp_cmd, check=True)

            # Find the downloaded file
            downloaded_file = None
            for f in os.listdir():
                if f.startswith(filename.split(".")[0]):
                    downloaded_file = f
                    break

            if downloaded_file:
                return send_file(downloaded_file, as_attachment=True)
            else:
                return "Download failed: File not found."

        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
