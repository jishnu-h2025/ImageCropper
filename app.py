from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__,template_folder='templates', static_folder='static',static_url_path='/static')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    if request.method == 'POST':
        folder_files = request.files.getlist('folder')
        if not folder_files or all(f.filename == '' for f in folder_files):
            return "No folder part in the request"

        for file in folder_files:
            if file and allowed_file(file.filename):
                print(f"Processing file: {file.filename}")
                upload_folder = os.path.join(app.static_folder, 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                
        return render_template('uploaded.html', folder_files=folder_files)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)


#HI I am jishnu