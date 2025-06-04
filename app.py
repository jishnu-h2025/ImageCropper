from flask import Flask, render_template, request, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):  
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Handle file upload
        files = request.files.getlist('folder')
        if not files or all(f.filename == '' for f in files):
            return "No files selected for uploading"
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_files.append({'filename': filename})
        
        return render_template('uploaded.html', folder_files=uploaded_files)
    
    # For GET requests, show the upload form
    return render_template('uploaded.html')

@app.route('/images')
def images():
    # Get list of files in upload directory
    folder_files = []
    upload_path = app.config['UPLOAD_FOLDER']
    
    if os.path.exists(upload_path):
        for filename in os.listdir(upload_path):
            filepath = os.path.join(upload_path, filename)
            if os.path.isfile(filepath) and allowed_file(filename):
                folder_files.append({'filename': filename})
    
    return render_template('images.html', folder_files=folder_files)

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.template_filter('trim')
def trim(s):
    trimmed_string = os.path.basename(s)
    return trimmed_string

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)