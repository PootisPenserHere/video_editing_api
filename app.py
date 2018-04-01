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
from werkzeug import secure_filename

app = Flask(__name__)

# Api config
app.config['UPLOAD_FOLDER'] = "videos/"
app.config['ALLOWED_EXTENSIONS '] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'mp4'])

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

def allowedExtensions(filename):
    return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_FOLDER']

@app.route('/retrieve/<fileName>')
def retrieveVideo(fileName):
    return send_from_directory(directory ='/code/videos/', filename = fileName)

@app.route('/upload')
def formUploadFile():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadFile():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
