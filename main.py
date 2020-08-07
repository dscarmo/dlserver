from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename

from imageio import imwrite, imread

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_route():
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        f.save(fname)

        render_template('loading.html')

        # Process...
        print('Processing...')
        try:
            im = imread(fname)
            im = (im - im.min()) / (im.max() - im.min())
        except Exception as e:
            return str(e)

        # Return
        imwrite("processed.png", im)
        print("Saved processed file.")

        render_template('download.html')


@app.route('/return_processed/')
def return_processed():
    try:
        return send_file("processed.png", attachment_filename="processed.png")
        render_template("upload.html")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
