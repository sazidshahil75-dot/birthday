from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-song', methods=['POST'])
def upload_song():
    if 'song' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['song']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = 'birthday_song.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'url': f'/static/uploads/{filename}', 'name': file.filename})
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/static/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
