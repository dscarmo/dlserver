from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import sys
sys.path.append("/home/diedre/git/radvid19")
import subprocess
import os

from imageio import imwrite, imread

app = Flask(__name__)


@app.route('/index')
def upload_file():
    return render_template('index.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_route():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        saved_fname = os.path.join("inputs", fname)
        f.save(saved_fname)

        # Process...
        try:
            print('Processing...')
            im = imread(saved_fname)

            # Return
            imwrite(os.path.join("outputs", os.path.basename(saved_fname)), im)
            print("Saved processed file.")
        except Exception as e:
            return str(e)

        return render_template('download.html')


@app.route('/return_processed/')
def return_processed():
    try:
        return send_file("processed.png", attachment_filename="processed.png")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
