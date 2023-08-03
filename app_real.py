from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
 
app = Flask(__name__)
 
UPLOAD_FOLDER = r'C:\Users\User\convert\flask\static\uploads'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
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
        flash('Image successfully uploaded and displayed below')

        image_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        model = YOLO("yolov8n.yaml")  # build a new model from scratch
        model = YOLO(r'C:\Users\User\convert\best.pt')  # load a pretrained model (recommended for training)

        predicted_filename = f"predicted_{filename}"
        predicted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], predicted_filename)

        model.predict(image_path, save=True, imgsz=320, conf=0.2)
        os.rename(image_path, predicted_image_path)  # Rename the predicted image

        return render_template('index.html', filename=filename, predicted_filename=predicted_filename)
    
    flash('Allowed image types are - png, jpg, jpeg, gif')
    return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

# Load a model 
if __name__ == "__main__":
    app.run(debug=True, port=5000)
