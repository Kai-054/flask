from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
# from PIL import Image
import cv2


app = Flask(__name__)

UPLOAD_FOLDER = r'D:\convert\flask\static\uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_image(image_path):
    model = YOLO(r'D:\convert\best.pt')  # Load a pretrained model (recommended for training)
    results = model(image_path)[0]
    output = results.plot(conf=0.2)
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.jpg')
    cv2.imwrite(output_path, output)    
    return output_path


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Handle the POST request (upload and process the image)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predicted_image_paths = predict_image(image_path)

            return render_template('index.html', filename=filename, predicted_image_paths=predicted_image_paths)

    # Handle the GET request (render the HTML page with the form)
    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
