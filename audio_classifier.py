import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv
import os
import sys
from scipy.io import wavfile
import warnings
import scipy
import shutil
from pydub import AudioSegment
import tempfile

def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding to score vector."""
    class_names = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row['display_name'])
    return class_names

def ensure_mono(waveform):
    """Convert stereo audio to mono by averaging channels."""
    if len(waveform.shape) > 1:
        print("Converting stereo to mono")
        return np.mean(waveform, axis=1)
    return waveform

def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Resample waveform if required."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) /
                                 original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform

def convert_to_wav(audio_path):
    """Convert audio file to WAV format if needed."""
    try:
        if audio_path.lower().endswith('.mp3'):
            audio = AudioSegment.from_mp3(audio_path)
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio.export(temp_wav.name, format='wav')
            return temp_wav.name
        return audio_path
    except Exception as e:
        print(f"Error converting audio file: {str(e)}")
        return None

def classify_audio_file(model, class_names, audio_path):
    """Classify a single audio file using YAMNet."""
    try:
        print(f"\nProcessing: {audio_path}")

        wav_path = convert_to_wav(audio_path)
        if wav_path is None:
            return None
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=wavfile.WavFileWarning)
            sample_rate, wav_data = wavfile.read(audio_path, 'rb')
        sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
        waveform = wav_data / tf.int16.max
        waveform = ensure_mono(waveform)
        
        # Run the model
        scores, embeddings, spectrogram = model(waveform)
        scores_np = scores.numpy()
        
        # Get top 3 predicted classes
        mean_scores = scores_np.mean(axis=0)
        top_3_indices = mean_scores.argsort()[-3:][::-1]
        top_3_classes = [(class_names[i], float(mean_scores[i])) for i in top_3_indices]
        
        return top_3_classes
    except Exception as e:
        print(f"Error processing {audio_path}: {str(e)}")
        return None

def process_directory(input_path):
    """Process all WAV files in the given directory and organize them."""
    try:
        # Load model
        print("Loading YAMNet model...")
        model = hub.load('https://tfhub.dev/google/yamnet/1')
        class_map_path = model.class_map_path().numpy()
        class_names = class_names_from_csv(class_map_path)
        
        # Create Audio directory if it doesn't exist
        base_dir = os.path.join(os.getcwd(), "Assets")
        audio_dir = os.path.join(base_dir, "Classified YAMnet Audio")
        os.makedirs(audio_dir, exist_ok=True)
        
        # Process files
        results = []
        for file in os.listdir(input_path):
            if file.lower().endswith(('.wav', '.mp3')):
                file_path = os.path.join(input_path, file)
                
                if "Classified YAMnet Audio" in file_path.split(os.sep):
                    continue
                    
                print(f"Processing: {file}")
                
                classifications = classify_audio_file(model, class_names, file_path)
                if classifications:
                    main_class = classifications[0][0]  # Get the top classification
                    
                    class_dir = os.path.join(audio_dir, main_class)
                    os.makedirs(class_dir, exist_ok=True)
                    
                    dest_path = os.path.join(class_dir, file)
                    if not os.path.exists(dest_path):
                        shutil.copy2(file_path, dest_path)
                    
                    results.append({
                        'file': file,
                        'classifications': classifications
                    })
                    
                    print(f"Classified {file} as {main_class}")
        
        print("\nClassification Summary:")
        for result in results:
            print(f"\nFile: {result['file']}")
            print("Classifications:")
            for class_name, confidence in result['classifications']:
                print(f"- {class_name}: {confidence:.3f}")
        
        return results
    
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_directory = sys.argv[1]
        if os.path.exists(input_directory):
            process_directory(input_directory)
        else:
            print(f"Directory not found: {input_directory}")
    else:
        print("Please provide an input directory path")
