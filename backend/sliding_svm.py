import os
import cv2
import joblib
import requests
from collections import Counter
import numpy as np

def load_model(model_path):
    """Load the SVM model from the file."""
    return joblib.load(model_path)

def sliding_window_classification(spectrogram, window_height, window_width, step_size, svm_model):
    height, width = spectrogram.shape
    predictions = []

    for x in range(0, width - window_width + 1, step_size):
        window = spectrogram[0:window_height, x:x + window_width]
        window = window.flatten().reshape(1, -1)  # Flatten the window for the SVM model
        prediction = svm_model.predict(window)
        predictions.append(((x + (window_width // 2)), prediction[0]))

    return predictions

def detect_transitions(predictions, pixels_per_threshold, step_size):
    transitions = []
    previous_class = None
    segment_predictions = []
    diff_predictions = []

    for position, pred_class in predictions:
        position = position - pixels_per_threshold + step_size
        segment_predictions.append(pred_class)
        if previous_class is None:
            previous_class = pred_class
            segment_predictions.clear()
            continue
        
        current_majority_class = Counter(segment_predictions).most_common(1)[0][0]
        if current_majority_class != pred_class:
            diff_predictions.append(pred_class)

        if pred_class != current_majority_class and (len(diff_predictions) * step_size) >= pixels_per_threshold:
            transitions.append((position, previous_class, current_majority_class))
            current_majority_class = pred_class
            segment_predictions.clear()
            diff_predictions.clear()

    return transitions

def calculate_register_frequency(predictions):
    counts = Counter([pred[1] for pred in predictions])
    total = sum(counts.values())
    frequencies = {int(label): count / total for label, count in counts.items()}
    return frequencies

def calculate_label_stability(predictions, step_size):
    stability_scores = {}
    current_label = int(predictions[0][1])  # Convert the initial label to an int
    current_streak = step_size

    for i in range(1, len(predictions)):
        label = int(predictions[i][1])  # Convert each label to an int
        
        if label == current_label:
            current_streak += step_size
        else:
            if current_label not in stability_scores:
                stability_scores[current_label] = 0
            stability_scores[current_label] += current_streak

            # Reset for new label
            current_label = label
            current_streak = step_size

    # Final update for the last streak
    if current_label not in stability_scores:
        stability_scores[current_label] = 0
    stability_scores[current_label] += current_streak

    return stability_scores


def send_analytics_to_backend(frequencies, stability):
    backend_url = 'http://localhost:5001/save-analytics'
    data = {
        'frequencies': frequencies,
        'stability': stability
    }
    response = requests.post(backend_url, json=data)
    if response.status_code == 200:
        print("Analytics successfully sent to the backend.")
    else:
        print("Failed to send analytics to the backend.")

def main():
    model_path = 'svm_model.pkl'
    image_path = './marked_spectrogram/concatenated_image.png'
    output_dir = '../frontend/src/spectrogram'

    window_height = 154
    window_width = 128
    step_size = 10

    model = load_model(model_path)
    spectrogram = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    spectrogram = cv2.resize(spectrogram, (spectrogram.shape[1], window_height))  # Ensure the height matches window_height  

    predictions = sliding_window_classification(spectrogram, window_height, window_width, step_size, model)

    print(predictions)
    spectrogram_color = cv2.imread(image_path, cv2.COLOR_RGB2BGR) # Convert to color for overlaying text
    
    total_width = spectrogram.shape[1]
    sec_per_pixel = 3/total_width
    print(sec_per_pixel)
    threshold_time_ms = 100  # Threshold duration in milliseconds
    threshold_time_seconds = threshold_time_ms / 1000  # Convert to seconds
    pixels_per_threshold = int(threshold_time_seconds / sec_per_pixel)
    print(f"Pixels per 150ms threshold: {pixels_per_threshold}")

    transitions = detect_transitions(predictions, pixels_per_threshold, step_size)

    # Calculate and print register frequencies
    frequencies = calculate_register_frequency(predictions)
    print("Frequencies of Vocal Registers:", frequencies)

    # Calculate and print label stability
    stability = calculate_label_stability(predictions, step_size)
    print("Label Stability Scores:", stability)

    # Send analytics to the backend
    send_analytics_to_backend(frequencies, stability)

    # Visualize predictions
    for x, pred_class in predictions:
        # Annotate each prediction with its class
        cv2.putText(spectrogram_color, str(pred_class), (x, window_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1, cv2.LINE_AA)

    # Visualize transitions with time annotations
    for x, prev_class, new_class in transitions:
        cv2.line(spectrogram_color, (x , 0), (x, window_height), (0, 255, 0), 2)

    # Visualize majority class per transition segment
    for i in range(len(transitions)):
        if i == 0:
            start_pos = 0

        end_pos = transitions[i][0]
        middle_pos = ((end_pos-start_pos) // 2) + start_pos
        majority_class = transitions[i][2]
        if majority_class == 0:
            majority_class = 'Chest'
        elif majority_class == 1:
            majority_class = 'Mix'
        elif majority_class == 2:
            majority_class = 'Head Mix'
        elif majority_class == 3:
            majority_class = 'Head'
        cv2.putText(spectrogram_color, f'Majority: {majority_class}', (middle_pos - pixels_per_threshold, window_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        start_pos = end_pos

    cv2.putText(spectrogram_color, 'End of Analysis', (total_width - 128 - pixels_per_threshold, window_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    image_path = os.path.join(output_dir, 'marked_spectrogram.png')
    cv2.imwrite(image_path, spectrogram_color)

if __name__ == "__main__":
    main()
