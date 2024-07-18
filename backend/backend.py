#Model Application
import cv2
import os
import joblib
import numpy as np 
# import demucs.api
from pydub import AudioSegment
from pydub.silence import split_on_silence
import librosa
import librosa.display
import matplotlib.pyplot as plt 
import re

def load_model(model_path):
    """Load the SVM model from the file."""
    return joblib.load(model_path)

def preprocess_images(spectrogram_dir, split_dir):
    timing_data = []
    
    def split_image(path, idx):
        if file.endswith('.DS_Store'):
            return
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        #print(path)
        height, width = image.shape
        num_segments = width // 128
        remainder_width = width % 128

        for i in range(num_segments):
            start_col = i * 128
            end_col = start_col + 128
            segment = image[:, start_col:end_col]
            segment = cv2.resize(segment, (128, 154), interpolation = cv2.INTER_AREA)
            #sliced_images.append(segment.flatten())
            segment_path = os.path.join(split_dir, f'{idx}_{i}.png')
            #print(segment_path)
            cv2.imwrite(segment_path, segment)
        if remainder_width > 0:
            start_col = width - remainder_width
            remainder_segment = image[:, start_col:]
            remainder_segment = cv2.resize(remainder_segment, (128, 154), interpolation = cv2.INTER_AREA)
            #sliced_images.append(remainder_segment.flatten())
            segment_path = os.path.join(split_dir, f'{idx}_r.png')
            cv2.imwrite(segment_path, remainder_segment)
        timing_data.append((num_segments, remainder_width))
    
    def natural_sort_key(s):
        """Sort helper function to extract numbers from strings."""
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    file_names = os.listdir(spectrogram_dir)
    file_names = sorted(file_names, key = natural_sort_key)
    #print(file_names)
    #print(file_names)
    for idx, file in enumerate(file_names): #ignore DS file
        path = os.path.join(spectrogram_dir, file)
        #print(str(path))
        split_image(path, idx)
    return timing_data

def make_predictions(model, samples):
    """Make predictions on the preprocessed samples using the loaded model."""
    return model.predict(samples)

def generate_mel_spectrogram(audio_files, output_image_dir='/Users/alex/Desktop/backend_spectrograms'):
    spectrograms=[]
    #print(audio_files)
    #px = 1/plt.rcParams['figure.dpi']
    # Load the audio file
    for idx, file in enumerate(audio_files):

        y, sr = librosa.load(file)
        # Set parameters to match Audacity's settings
        n_fft = 1024 # Window size for the STFT
        hop_length = 1  # Hop length (50% overlap)
        n_mels = 256  # Number of Mel bands
        fmin = 1  # Minimum frequency
        fmax = sr/2  # Maximum frequency (Nyquist frequency)
        window = 'hann'  # Window type
        # Generate mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=fmin, fmax=fmax, window=window)
        length = librosa.get_duration(y=y, sr=sr)
        gain = 20
        # Convert to log scale (dB)
        S_dB = librosa.power_to_db(S, ref=np.max) + gain
        spectrograms.append(S_dB)
        # Plot the mel spectrogram
        plt.figure(figsize=((1024*(length/3))/72, 154/72), dpi = 100)
        plt.axis('off')
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', cmap = 'magma', vmin = -60, vmax = 0)
        #plt.show()
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('Mel Spectrogram')
        # plt.tight_layout()

        # Save the plot as an image file
        output_file = os.path.join(output_image_dir, f'mel_spectrogram_{idx}.png')
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
        plt.close()

    #return spectrograms
def separate_vocals(test_dir, silence_thresh=-40, min_silence_len=500, keep_silence=500, segment_length=3000):
    file_name = os.listdir(test_dir)
    input_path = os.path.join(test_dir, file_name[1])
    #print(file_name)
    # separator = demucs.api.Separator(segment = 10, split = True)
    output_dir = '/Users/alex/Desktop/backend_out'
    # origin, separated_audio = separator.seperate_audio_file(file_name)
    # audio = AudioSegment.from_file(separated_audio)
    # Split audio based on silence
    audio = AudioSegment.from_file(input_path)
    chunks = split_on_silence(
        audio, 
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    audio_files = []
    for i, chunk in enumerate(chunks):
        start = 0
        while start < len(chunk):
            segment = chunk[start:start+segment_length]
            if len(segment) > 0:
                segment_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename('audio'))[0]}_segment_{i}_{start // 1000}.wav")
                audio_files.append(segment_filename)
                segment.export(segment_filename, format="wav")
            start += segment_length
    generate_mel_spectrogram(audio_files)
    

def main():
    # Define paths and parameters
    model_path = 'svm_model.pkl'
    test_dir = '/Users/alex/Desktop/testing'
    split_dir = '/Users/alex/Desktop/backend_split'
    spectrogram_dir = '/Users/alex/Desktop/backend_spectrograms'

    #desired_size = (154, 128)  # Ensure this matches your training image size

    # Load the trained SVM model
    model = load_model(model_path)
    #Demucs stem splitter API 
    separate_vocals(test_dir)
    # Preprocess new images
    timing_data = preprocess_images(spectrogram_dir, split_dir)
    #print(timing_data)
    processed_images = os.listdir(split_dir)
    #print(len(processed_images))
    # Make predictions if there are valid samples
    samples = []
    file_paths = []
    for file in processed_images:
        if file.endswith('.DS_Store'):
            continue
        full_path = os.path.join(split_dir, file)
        image = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        flat_image = image.flatten()
        samples.append(flat_image)
        file_paths.append(full_path)

    predictions = make_predictions(model, samples)
        # Print the predictions
    for path, prediction in zip(file_paths, predictions):
        print(f"Image: {path}, Predicted Class: {prediction}")

if __name__ == "__main__":
    main()
