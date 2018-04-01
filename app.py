from flask import Flask
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
from flask import send_from_directory
from flask import request
from flask import jsonify
from flask import render_template
import string
import random
import os.path

app = Flask(__name__)

# Api config
app.config['UPLOAD_FOLDER'] = "videos/"
app.config['ALLOWED_EXTENSIONS'] = set(['.flv', '.gif', '.gifv', '.avi', '.mpg', '.mp4', '.3gp'])

@app.route('/')
def hello():
    return "hello world!"
    #return send_from_directory(directory ='/code/videos/', filename = "bunny_edited.mp4")

@app.route('/cut/<fileName>/starting/<startTime>/ending/<endTime>')
def newCutVideo(fileName, startTime, endTime):
    return cutVideo(fileName, startTime, endTime)

@app.route('/volume/<fileName>/<newLevel>')
def newVideoLowerVolume(fileName, newLevel):
    return reduceVolume(fileName, newLevel)

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

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip])

    # Write the result to a file (many options available !)
    video.write_videofile(newFilePath)

    return newFileName

def reduceVolume(fileName, newVolume):
    newVolume = float(newVolume)
    newVolume = newVolume / 10

    fileExtension = getFileExtension(fileName)
    originalFile = "%s%s" % ("videos/", fileName)

    randomName = randomString()
    newFileName = "%s%s" % (randomName, fileExtension)
    newFilePath = "%s%s" % ("videos/", newFileName)

    # Load video
    clip = VideoFileClip(originalFile)

    # Reduce the audio volume
    clip = clip.volumex(newVolume)

    # Write the result to a file (many options available !)
    clip.write_videofile(newFilePath)

    return newFileName

def uploadedFileExtension(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return "%s%s" % (".", extension)

@app.route('/retrieve/<fileName>')
def retrieveVideo(fileName):
    return send_from_directory(directory ='/code/videos/', filename = fileName)

@app.route('/upload')
def formUploadFile():
   return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def uploadFile():
  receivedFile = request.files['file']
  receivedFileFormat = uploadedFileExtension(receivedFile.filename)

  if receivedFileFormat in app.config['ALLOWED_EXTENSIONS']:
      randomName = randomString()
      newFileName = "%s%s" % (randomName, receivedFileFormat)
      newFilePath = "%s%s" % (app.config['UPLOAD_FOLDER'], newFileName)

      receivedFile.save(newFilePath)

      return jsonify({"status": "success", "message": newFileName})

  else:
      return jsonify({"status": "error", "message": "Format not allowed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
