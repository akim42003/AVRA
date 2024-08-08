from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

UPLOAD_FOLDER = './uploads'
FULL_SPECTROGRAMS_FOLDER = './full_spectrograms'
SPLIT_SPECTROGRAMS_FOLDER = './split_spectrograms'
VOCAL_CHUNKS_FOLDER = './vocal_chunks'
MARKED_SPECTROGRAM_FOLDER = '../frontend/src/spectrogram'
MARKED_SPECTROGRAM_FILE = 'marked_spectrogram.png'
DB_FILE = 'audio_spectrogram.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure all directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FULL_SPECTROGRAMS_FOLDER, exist_ok=True)
os.makedirs(SPLIT_SPECTROGRAMS_FOLDER, exist_ok=True)
os.makedirs(VOCAL_CHUNKS_FOLDER, exist_ok=True)
os.makedirs(MARKED_SPECTROGRAM_FOLDER, exist_ok=True)

@app.route('/save-region', methods=['POST'])
def save_region():
    data = request.json
    start = data.get('start')
    end = data.get('end')
    stop = data.get('stop')
    use_svm = data.get('useSVM')
    use_cnn = data.get('useCNN')
    
    app.logger.debug(f"Received data: {data}")
    app.logger.debug(f"Start: {start}, End: {end}, Stop: {stop}")
    app.logger.debug(f"Use SVM: {use_svm}, Use CNN: {use_cnn}")
    print(os.listdir('./marked_spectrogram'))
    # Call concatenate_images.py with start and end
    subprocess.run(['python', 'concatenate_images.py', str(start), str(end), str(stop)], capture_output=True, text=True)
    
    if use_svm:
        result = subprocess.run(['python', 'sliding_svm.py'], capture_output=True, text=True)
    elif use_cnn:
        result = subprocess.run(['python', 'cnn_model.py'], capture_output=True, text=True)
    else:
        return jsonify({"message": "Reset chosen"})

    # Log the output from the selected script
    app.logger.debug(f"Script output: {result.stdout}")
    if result.returncode != 0:
        app.logger.error(f"Script error: {result.stderr}")
        return jsonify({"message": "Error in script execution"}), 500

    # Return the filename of the marked spectrogram
    return jsonify({"message": "Region saved successfully", "start": start, "end": end, "file": MARKED_SPECTROGRAM_FILE})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    check = False
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        full_audios = os.listdir(UPLOAD_FOLDER)
        if full_audios:
            for item in full_audios:
                if item != file.filename:
                    check = True
                    print('Clearing old audio')
                    audio_path = os.path.join(UPLOAD_FOLDER, item)
                    if os.path.isfile(audio_path):
                        os.remove(audio_path)
        else:
            check = True
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        app.logger.debug(f"File uploaded to: {file_path}")
        # Process the file as needed
        if check == True:
            full_spectrograms = os.listdir(FULL_SPECTROGRAMS_FOLDER)
            if os.path.isfile(DB_FILE):
                os.remove(DB_FILE)
                print('Clearing DB')
            if full_spectrograms:
                print('Clearing and rendering new spectrograms')
                for item in full_spectrograms:
                    item_path = os.path.join(FULL_SPECTROGRAMS_FOLDER, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                split_spectrograms = os.listdir(SPLIT_SPECTROGRAMS_FOLDER)
                for item in split_spectrograms:
                    split_path = os.path.join(SPLIT_SPECTROGRAMS_FOLDER, item)
                    if os.path.isfile(split_path):
                        os.remove(split_path)
                audio_segments = os.listdir(VOCAL_CHUNKS_FOLDER)
                for item in audio_segments:
                    segment_path = os.path.join(VOCAL_CHUNKS_FOLDER, item)
                    if os.path.isfile(segment_path):
                        os.remove(segment_path)
                subprocess.run(['python', 'audio_split.py'])
                subprocess.run(['python', 'audio_to_images.py'])
        return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200

@app.route('/spectrogram/marked_spectrogram.png')
def send_marked_spectrogram():
    return send_from_directory(MARKED_SPECTROGRAM_FOLDER, MARKED_SPECTROGRAM_FILE)

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
