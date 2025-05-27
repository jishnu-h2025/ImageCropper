from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    # List uploaded files for display
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [f for f in files if allowed_file(f)]
    return render_template('index.html', images=images)

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'images' not in request.files:
        return redirect(url_for('index'))

    files = request.files.getlist('images')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
