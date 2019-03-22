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


@app.route('/cut/<filename>/starting/<start>/ending/<end>')
def cut_new_video(filename, start, end):
    return jsonify({"status": "success", "message": cut_video(filename, start, end)})


@app.route('/volume/<filename>/<volume>')
def lower_volume_new_video(filename, volume):
    return jsonify({"status": "success", "message": reduce_volume(filename, volume)})


@app.route('/retrieve/<filename>')
def retrieve_video(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)


@app.route('/upload')
def display_upload_form():
    """
    Renders a basic html template to allow the upload of video files from the
    browser rather than having to do it through a pure http request
    """

    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    """
    Stores the sent files through a post method, validating them against the
    permited formats and assigning them a randomly generated name

    :return: contains a status and the name of the new file if successful
    :rtyoe: json
    """

    uploaded_file = request.files['file']
    file_extension = uploaded_file_extension(uploaded_file.filename)

    if file_extension in app.config['ALLOWED_EXTENSIONS']:
        new_filename = "%s%s" % (random_string(), file_extension)
        new_filename_path = "%s%s" % (app.config['UPLOAD_FOLDER'], new_filename)

        uploaded_file.save(new_filename_path)

        return jsonify({"status": "success", "message": new_filename})

    else:
        return jsonify({"status": "error", "message": "Format not allowed"})


def random_string(size: str = 20) -> str:
    """
    Generates a cryptographically secure random string with a default length
    of 20 characters

    :param size: Desired size for the string to generate
    :type size: int
    :rtype: str
    :return: A random string of the specified length
    :rtype: str
    """

    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def get_file_extension(filename: str) -> str:
    """
    Obtains the extension of a file which already exists in disk

    :param filename: Name of the file with its extension included
    :type filename: str
    :return: The file extension as it's in disk
    """

    return os.path.splitext(filename)[1]


def cut_video(filename: str, start: int, end: int) -> str:
    """
    Creates a new clip of the original video within the selected timeframe

    :param filename: Name of the file with its extension
    :type filename: str
    :param start: The second of the original video from which the new clip will begin
    :type start: int
    :param end: The second from the original video up to which the clip will be cut
    :type end: int
    :return: The name of the newly created clip
    :rtype: str
    """

    file_extension = get_file_extension(filename)
    original_file = "%s%s" % (app.config['UPLOAD_FOLDER'], filename)

    new_filename = "%s%s" % (random_string(), file_extension)
    new_filename_path = "%s%s" % (app.config['UPLOAD_FOLDER'], new_filename)

    # Load video and select the subclip
    clip = VideoFileClip(original_file).subclip(float(start), float(end))

    # Write the result to a file
    clip.write_videofile(new_filename_path)

    return new_filename


def reduce_volume(filename: str, volume: int) -> str:
    """
    Chances the volume setting of a video, this process can only lower it
    from the already existing point

    :param filename: Name of the file with its extension
    :type filename: str
    :param volume: The new setting where 10 represents the 100%
    :type volume: int
    :return: The name of the newly created clip
    :rtype: str
    """

    volume = float(volume)
    volume = volume / 10

    file_extension = get_file_extension(filename)
    original_file = "%s%s" % (app.config['UPLOAD_FOLDER'], filename)

    new_filename = "%s%s" % (random_string(), file_extension)
    new_filename_path = "%s%s" % (app.config['UPLOAD_FOLDER'], new_filename)

    # Load video
    clip = VideoFileClip(original_file)

    # Reduce the audio volume
    clip = clip.volumex(volume)

    # Write the result to a file
    clip.write_videofile(new_filename_path)

    return new_filename


def uploaded_file_extension(filename: str) -> str:
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
