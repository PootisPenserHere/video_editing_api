from flask import Flask
from moviepy.editor import *
from flask import send_from_directory
from flask import request
from flask import jsonify
from flask import render_template
import string
import random
import os.path

app = Flask(__name__)

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
    return send_from_directory(directory='/code/videos/', filename=fileName)


@app.route('/upload')
def formUploadFile():
    """
    Renders a basic html template to allow the upload of video files from the
    browser rather than having to do it through a requesting application
    """

    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def uploadFile():
    """
    Stores the sent files through a post method, validating them against the
    permited formats and assigning them a randomly generated name

    :return: contains a status and the name of the new file if successful
    :rtyoe: json
    """

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


def randomString(size: str =20):
    """
    Generates a cryptographically secure random string with a default length
    of 20 characters

    :param size: Desired size for the string to generate
    :type size: int
    :rtype: str
    :return:
    """

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def getFileExtension(fileName: str) -> str:
    """
    Obtains the extension of a file which already exists in disk

    :param fileName: Name of the file with its extension included
    :type fileName: str
    :return:
    """

    return os.path.splitext(fileName)[1]


def cutVideo(fileName: str, startTime: int, endTime: int):
    """
    Creates a new clip of the original video within the selected timeframe

    :param fileName: Name of the file with its extension
    :type fileName: str
    :param startTime: The second of the original video from which the new clip will begin
    :type startTime: int
    :param endTime: The second from the original video up to which the clip will be cut
    :type endTime: int
    :return:
    """

    fileExtension = getFileExtension(fileName)
    originalFile = "%s%s" % (app.config['UPLOAD_FOLDER'], fileName)

    randomName = randomString()
    newFileName = "%s%s" % (randomName, fileExtension)
    newFilePath = "%s%s" % (app.config['UPLOAD_FOLDER'], newFileName)

    # Load video and select the subclip
    clip = VideoFileClip(originalFile).subclip(float(startTime), float(endTime))

    # Write the result to a file
    clip.write_videofile(newFilePath)

    return jsonify({"status": "success", "message": newFileName})


def reduceVolume(fileName: str, newVolume: int):
    """
    Chances the volume setting of a video, this process can only lower it
    from the already existing point

    :param fileName: Name of the file with its extension
    :type fileName: str
    :param newVolume: The new setting where 10 represents the 100%
    :type newVolume: int
    :return:
    """

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


def uploadedFileExtension(filename: str) -> str:
    """
    Returns the extension from a file name

    :param filename: Name of the file with its extension
    :type filename: str
    :return: The extension of the file
    :rtype: str
    """

    extension = filename.rsplit('.', 1)[1].lower()
    return "%s%s" % (".", extension)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
