from pydub import AudioSegment
#from pydub.silence import split_on_silence
import os
from db.db_utils import add_audio_segment
from db.models import create_tables

def split_audio_file(input_file, output_dir, silence_thresh=-40, min_silence_len=500, keep_silence=500, segment_length=3000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # # Split audio based on silence
    # chunks = split_on_silence(
    #     audio, 
    #     min_silence_len=min_silence_len,
    #     silence_thresh=silence_thresh,
    #     keep_silence=keep_silence
    # )
    
    # # Process and save the chunks
    # for i, chunk in enumerate(chunks):
    start = 0
    while start < len(audio):
        segment = audio[start:start+segment_length]
        if len(segment) > 0:
            segment_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_segment_{start // 1000}.wav")
            segment.export(segment_filename, format="wav")
            add_audio_segment(len(segment))
        start += segment_length
    

def process_folder(input_folder, output_folder, silence_thresh=-40, min_silence_len=500, keep_silence=500, segment_length=3000):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp3"):  
            input_file = os.path.join(input_folder, filename)
            split_audio_file(input_file, output_folder, silence_thresh, min_silence_len, keep_silence, segment_length)

if __name__ == "__main__":
    create_tables()
    input_folder = "./uploads"  # Replace with your input folder path
    output_folder = "./vocal_chunks"  # Replace with your desired output directory
    process_folder(input_folder, output_folder, silence_thresh=-40)  # Adjust parameters as needed
