from flask import Flask
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def hello():
    # Load bunny.mp4 and select the subclip 00:00:50 - 00:00:60
    clip = VideoFileClip("bunny.mp4").subclip(50,60)

    # Reduce the audio volume (volume x 0.8)
    clip = clip.volumex(0.8)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip])

    # Write the result to a file (many options available !)
    video.write_videofile("bunny_edited.mp4")

    return send_from_directory(directory ='/code/', filename = "bunny_edited.mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
