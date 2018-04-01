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

@app.route('/cut/<fileName>/starting/<startTime>/ending/<endTime>')
def newCutVideo(fileName, startTime, endTime):
    return cutVideo(fileName, startTime, endTime)

@app.route('/volume/<fileName>/<newLevel>')
def newVideoLowerVolume(fileName, newLevel):
    return reduceVolume(fileName, newLevel)

@app.route('/retrieve/<fileName>')
def retrieveVideo(fileName):
    return send_from_directory(directory ='/code/videos/', filename = fileName)

''' Renders a basic html template to allow the upload of video files from the
browser rather than having to do it through a requesting application
'''
@app.route('/upload')
def formUploadFile():
   return render_template('upload.html')

''' Stores the sent files through a post method, validating them against the
permited formats and assigning them a randomly generated name

@return json - contains a status and the name of the new file if successful
'''
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

''' Generates a cryptographically secure random string with a default lenght of
20 characters
'''
def randomString(size = 20, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

''' Obtains the extension of a file which already exists in disk

@param filename string - the name of the file
@return string
'''
def getFileExtension(fileName):
    return os.path.splitext(fileName)[1]

''' Creates a new clip of the original video within the selected timeframe

@param filename string - the name of the file
@param startTime int - the second from which the new clip will begin
@param endTime int - the second on which the new clip will end
@return json - contains a status and the name of the new file if successful
'''
def cutVideo(fileName, startTime, endTime):
    fileExtension = getFileExtension(fileName)
    originalFile = "%s%s" % (app.config['UPLOAD_FOLDER'], fileName)

    randomName = randomString()
    newFileName = "%s%s" % (randomName, fileExtension)
    newFilePath = "%s%s" % (app.config['UPLOAD_FOLDER'], newFileName)

    # Load video and select the subclip
    clip = VideoFileClip(originalFile).subclip(float(startTime),float(endTime))

    # Write the result to a file
    clip.write_videofile(newFilePath)

    return jsonify({"status": "success", "message": newFileName})

''' Chances the volume setting of a video, this process can only lower it from
the already existing point

@param filename string - the name of the file
@param newVolume int - the new setting where 10 represents the 100%
@return json - contains a status and the name of the new file if successful
'''
def reduceVolume(fileName, newVolume):
    newVolume = float(newVolume)
    newVolume = newVolume / 10

    fileExtension = getFileExtension(fileName)
    originalFile = "%s%s" % (app.config['UPLOAD_FOLDER'], fileName)

    randomName = randomString()
    newFileName = "%s%s" % (randomName, fileExtension)
    newFilePath = "%s%s" % (app.config['UPLOAD_FOLDER'], newFileName)

    # Load video
    clip = VideoFileClip(originalFile)

    # Reduce the audio volume
    clip = clip.volumex(newVolume)

    # Write the result to a file
    clip.write_videofile(newFilePath)

    return jsonify({"status": "success", "message": newFileName})

''' Returns the extension from an uploaded file

@param filename string - the name of the file
@return string
'''
def uploadedFileExtension(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return "%s%s" % (".", extension)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
