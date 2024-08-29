import os
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename

# Instalasi Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Mendefinisikan kelas abjad
class_names = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 
    19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}

# Fungsi untuk memeriksa ekstensi file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Fungsi untuk memprediksi satu gambar
def predict_image(model, img_path, class_names, target_size=None):
    if target_size is None:
        target_size = (model.input_shape[1], model.input_shape[2])
    
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  
    
    pred = model.predict(img_array)
    predicted_class_index = np.argmax(pred[0])
    predicted_class_name = class_names[predicted_class_index]
    
    return predicted_class_name

# Memuat model yang telah dilatih
model = tf.keras.models.load_model('asl_signlanguage.h5')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            predicted_class_name = predict_image(model, file_path, class_names)
            return render_template('result.html', filename=filename, predicted_class_name=predicted_class_name)
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == '__main__':
    app.run(debug=True)