from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import subprocess
import os
import uuid
from glob import iglob, glob

import nibabel as nib

app = Flask(__name__)


@app.route('/index')
def upload_file():
    return render_template('index.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_route():
    if request.method == 'POST':
        f = request.files['file']
        fname = str(uuid.uuid1()) + secure_filename(f.filename)
        saved_fname = os.path.join("inputs", fname)
        f.save(saved_fname)

        # Process...
        try:
            print('Processing...')
            im = nib.load(saved_fname)
            aff = im.affine
            fdata = im.get_fdata()
            if "nii.gz" not in saved_fname:
                print("Detected uncompressed input, compressing...")
                new_saved_fname = os.path.join("inputs", fname.split('.')[0] + ".nii.gz")
                nib.save(nib.Nifti1Image(fdata, affine=aff), new_saved_fname)
                os.remove(saved_fname)
                saved_fname = new_saved_fname
                print("Compressed version saved and original deleted.")

            # Return
            subprocess.run(["python3", "/home/diedre/git/radvid19/predict.py", "-m", "/home/diedre/git/radvid19/models",
                            "-i", saved_fname, "-o", "outputs", "--compress", "--cpus", '1'])

        except Exception as e:
            return str(e)

        return render_template('download.html')


@app.route('/return_processed/')
def return_processed():
    try:
        print("Preparing results...")
        if os.path.isfile("processed.zip"):
            os.remove("processed.zip")
        subprocess.run(["zip", "-r", "processed.zip", "outputs"])
        for path in iglob(os.path.join("outputs", "**", "*.nii*"), recursive=True):
            os.remove(path)
        for path in glob(os.path.join("inputs", "*.nii*")):
            os.remove(path)
        print("Done.")
        return send_file("processed.zip", as_attachment=True)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
