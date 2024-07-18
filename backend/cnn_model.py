import os
import cv2
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from collections import Counter
import numpy as np
import torch.nn.functional as F

# CNN model definition
class StandardCNN(nn.Module):
    def __init__(self, num_classes):
        super(StandardCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1_input_features = 128 * 16 * 19  # Adjust according to input size
        self.fc1 = nn.Linear(self.fc1_input_features, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(x.size(0), -1)  # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_cnn_model(model_path, device, num_classes):
    """Load the CNN model from the file."""
    model = StandardCNN(num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model

def sliding_window_classification_cnn(spectrogram, window_height, window_width, step_size, cnn_model, device):
    height, width = spectrogram.shape[:2]
    predictions = []
    transform = transforms.Compose([
        transforms.Resize((window_height, window_width)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize for RGB
    ])

    for x in range(0, width - window_width + 1, step_size):
        window = spectrogram[0:window_height, x:x + window_width]
        window_rgb = cv2.cvtColor(window, cv2.COLOR_GRAY2RGB)  # Convert to RGB
        image = Image.fromarray(window_rgb)
        image = transform(image).unsqueeze(0).to(device)
        with torch.no_grad():
            output = cnn_model(image)
            _, predicted = torch.max(output.data, 1)
            predictions.append(((x + (window_width//2)), predicted.item()))

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
            segment_predictions.clear()  # Reset segment predictions
            diff_predictions.clear()

    return transitions

def main():
    cnn_model_path = 'simple_cnn.pth'
    num_classes = 4  # Set the number of classes for the CNN model

    image_path = './marked_spectrogram/concatenated_image.png'
    output_dir = '../frontend/src/spectrogram'

    window_height = 154
    window_width = 128
    step_size = 10

    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = load_cnn_model(cnn_model_path, device, num_classes)

    spectrogram = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    spectrogram = cv2.resize(spectrogram, (spectrogram.shape[1], window_height))  # Ensure the height matches window_height  

    predictions = sliding_window_classification_cnn(spectrogram, window_height, window_width, step_size, model, device)

    print(predictions)
    spectrogram_color = cv2.imread(image_path, cv2.COLOR_RGB2BGR) # Convert to color for overlaying text
    
    total_width = spectrogram.shape[1]
    sec_per_pixel = 3 / total_width
    print(sec_per_pixel)
    threshold_time_ms = 100  # Threshold duration in milliseconds
    threshold_time_seconds = threshold_time_ms / 1000  # Convert to seconds
    pixels_per_threshold = int(threshold_time_seconds / sec_per_pixel)
    print(f"Pixels per 150ms threshold: {pixels_per_threshold}")

    transitions = detect_transitions(predictions, pixels_per_threshold, step_size)

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
        middle_pos = ((end_pos - start_pos) // 2) + start_pos
        majority_class = transitions[i][2]
        cv2.putText(spectrogram_color, f'Majority: {majority_class}', (end_pos - pixels_per_threshold, window_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        start_pos = end_pos

    cv2.putText(spectrogram_color, 'End of Analysis', (total_width - 128 - pixels_per_threshold, window_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    image_path = os.path.join(output_dir, 'marked_spectrogram.png')
    cv2.imwrite(image_path, spectrogram_color)

if __name__ == "__main__":
    main()
