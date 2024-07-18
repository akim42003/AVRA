#Model Application
import cv2
import os
import numpy as np 
import librosa
import librosa.display
import matplotlib.pyplot as plt 
import re
from db.db_utils import add_spectrogram_segment

def preprocess_images(spectrogram_dir, split_dir):
    timing_data = []
    
    def split_image(path, idx):
        if file.endswith('.DS_Store'):
            return
        image = cv2.imread(path)
        #print(path)
        height, width, channels = image.shape
        num_segments = width // 128
        remainder_width = width % 128

        for i in range(num_segments):
            start_col = i * 128
            end_col = start_col + 128
            segment = image[:, start_col:end_col]
            #segment = cv2.resize(segment, (128, 154), interpolation = cv2.INTER_AREA)
            #sliced_images.append(segment.flatten())
            segment_path = os.path.join(split_dir, f'{idx}_{i}.png')
            #print(segment_path)
            cv2.imwrite(segment_path, segment)
            add_spectrogram_segment(idx, i, 128)
        if remainder_width > 0:
            start_col = width - remainder_width
            remainder_segment = image[:, start_col:]
            #remainder_segment = cv2.resize(remainder_segment, (128, 154), interpolation = cv2.INTER_AREA)
            #sliced_images.append(remainder_segment.flatten())
            segment_path = os.path.join(split_dir, f'{idx}_r.png')
            cv2.imwrite(segment_path, remainder_segment)
            add_spectrogram_segment(idx, (num_segments+1), remainder_width)
                                    
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

def generate_mel_spectrogram(audio_dir, output_image_dir='full_spectrograms'):
    audio_files = os.listdir(audio_dir)

    def extract_number(filename):
        match = re.search(r'_(\d+)\.wav$', filename)
        return int(match.group(1)) if match else -1
    audio_files = sorted(audio_files, key=extract_number)

    print(audio_files)
    spectrograms=[]
    #print(audio_files)
    #px = 1/plt.rcParams['figure.dpi']
    # Load the audio file
    for idx, file in enumerate(audio_files):
        if file.endswith('.DS_Store'):
            continue
        file = os.path.join(audio_dir, file)
        y, sr = librosa.load(file)

        # Normalize the audio signal
        y = y / np.max(np.abs(y))
        
        # Set parameters to match Audacity's settings
        n_fft = 1024 # Window size for the STFT
        hop_length = 1  # Hop length (50% overlap)
        n_mels = 256  # Number of Mel bands
        fmin = 1  # Minimum frequency
        fmax = sr/2  # Maximum frequency (Nyquist frequency)
        window = 'hann'  # Window type
        amin = 1e-20
        dynamic_range = 80  # Dynamic range in dB
        # Generate mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels, fmin=fmin, fmax=fmax, window=window, power = 2)
        length = librosa.get_duration(y=y, sr=sr)
        gain = 20
        # Convert to log scale (dB)
        S_dB = librosa.power_to_db(S, ref=np.max, amin = amin, top_db = dynamic_range) + gain
        spectrograms.append(S_dB)
        # Plot the mel spectrogram
        plt.figure(figsize=((1024*(length/3))/72, 154/72), dpi = 100)
        plt.axis('off')
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', cmap = 'magma', vmin = (gain-dynamic_range), vmax = 0)
        #plt.show()
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('Mel Spectrogram')
        # plt.tight_layout()

        # Save the plot as an image file
        output_file = os.path.join(output_image_dir, f'mel_spectrogram_{idx}.png')
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
        plt.close()

def main():
    # Define paths and parameters
    audio_dir = './vocal_chunks'
    split_dir = './split_spectrograms'
    spectrogram_dir = './full_spectrograms'

    generate_mel_spectrogram(audio_dir)

    #desired_size = (154, 128)  # Ensure this matches your training image size
    # Preprocess new images
    timing_data = preprocess_images(spectrogram_dir, split_dir)
    #print(timing_data)
    processed_images = os.listdir(split_dir)
    #print(len(processed_images))
  
if __name__ == "__main__":
    main()
