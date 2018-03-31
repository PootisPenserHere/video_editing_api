from flask import Flask
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
from flask import send_from_directory
import string
import random
import os.path

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello world!"
    #return send_from_directory(directory ='/code/videos/', filename = "bunny_edited.mp4")

@app.route('/cut/<fileName>/starting/<startTime>/ending/<endTime>')
def newCutVideo(fileName, startTime, endTime):

    return cutVideo(fileName, startTime, endTime)

def randomString(size = 16, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

def getFileExtension(fileName):
    return os.path.splitext(fileName)[1]

def cutVideo(fileName, startTime, endTime):
    fileExtension = getFileExtension(fileName)
    originalFile = "%s%s" % ("videos/", fileName)

    randomName = randomString()
    newFileName = "%s%s" % (randomName, fileExtension)
    newFilePath = "%s%s" % ("videos/", newFileName)

    # Load video and select the subclip
    clip = VideoFileClip(originalFile).subclip(float(startTime),float(endTime))

    # Reduce the audio volume (volume x 0.8)
    clip = clip.volumex(0.8)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip])

    # Write the result to a file (many options available !)
    video.write_videofile(newFilePath)

    return newFileName

@app.route('/retrieve/<fileName>')
def retrieveVideo(fileName):
    return send_from_directory(directory ='/code/videos/', filename = fileName)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
