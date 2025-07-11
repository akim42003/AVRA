# AVRA - Audio Vocal Recognition and Analysis

A machine learning-powered application for audio vocal recognition and analysis using convolutional neural networks (CNN) and support vector machines (SVM). This project enables users to upload audio files, visualize spectrograms, and perform vocal analysis through an intuitive web interface. A full working demo can be accessed via `docker pull akim42003/avra:1.1.0`.

## Features

- **Audio Upload & Processing**: Upload audio files (.mp3, .wav) for analysis
- **Spectrogram Visualization**: Convert audio to mel-spectrograms for visual analysis
- **Machine Learning Models**:
  - CNN-based vocal recognition
  - SVM-based classification
- **Interactive Interface**: Select regions of interest on spectrograms
- **Real-time Analysis**: Process audio segments and display results
- **Analytics Dashboard**: View frequency analysis and stability metrics

## Technology Stack

### Backend
- **Python 3.x** with Flask framework
- **Machine Learning**: PyTorch, scikit-learn
- **Audio Processing**: librosa, scipy
- **Image Processing**: OpenCV, PIL
- **Database**: SQLite
- **APIs**: RESTful endpoints with Flask-CORS

### Frontend
- **React 18.x** with modern JavaScript
- **UI Components**: Custom components with Tailwind CSS
- **Audio Visualization**: WaveSurfer.js integration
- **Charts**: Chart.js for analytics
- **Styling**: Tailwind CSS, Styled Components

## Project Structure

```
AVRA/
├── app/
│   ├── backend/
│   │   ├── app.py                 # Flask application main file
│   │   ├── cnn_model.py           # CNN model implementation
│   │   ├── sliding_svm.py         # SVM model implementation
│   │   ├── audio_split.py         # Audio segmentation
│   │   ├── audio_to_images.py     # Spectrogram generation
│   │   ├── concatenate_images.py  # Image processing
│   │   ├── db/                    # Database models and utilities
│   │   ├── uploads/               # Uploaded audio files
│   │   ├── full_spectrograms/     # Generated spectrograms
│   │   ├── split_spectrograms/    # Processed spectrogram segments
│   │   └── vocal_chunks/          # Audio segments
│   └── frontend/
│       ├── src/
│       │   ├── components/        # React components
│       │   │   ├── Home.jsx       # Landing page
│       │   │   ├── Demo.jsx       # Main analysis interface
│       │   │   ├── Wavesurfing.jsx # Audio player component
│       │   │   ├── ScrollableImage.jsx # Spectrogram viewer
│       │   │   └── ...
│       │   └── App.js             # Main React application
│       ├── public/                # Static assets
│       └── package.json           # Dependencies
└── Emerson_Project.pdf            # Project documentation
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd app/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install flask flask-cors torch torchvision opencv-python librosa scikit-learn pillow numpy scipy requests
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5001`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd app/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000`

## Usage

1. **Upload Audio**: Use the web interface to upload an audio file
2. **View Spectrogram**: The system automatically generates and displays mel-spectrograms
3. **Select Region**: Click and drag on the spectrogram to select regions of interest
4. **Choose Model**: Select CNN or SVM for analysis
5. **View Results**: Analyze the marked spectrogram results and analytics data

## Machine Learning Models

### CNN Model
- **Architecture**: 3-layer CNN
- **Input**: RGB spectrogram images (resized to standard dimensions)
- **Output**: Classification predictions
- **Training**: Uses sliding window approach for segment analysis

### SVM Model
- **Type**: Support Vector Machine for classification
- **Features**: Extracted from spectrogram segments
- **Application**: Alternative classification method

## Data Processing Pipeline

1. **Audio Segmentation**: Split audio into manageable chunks
2. **Spectrogram Generation**: Convert audio to mel-spectrograms
3. **Image Processing**: Create sliding windows for analysis
4. **Model Prediction**: Apply CNN/SVM to classify segments
5. **Result Visualization**: Mark predictions on spectrograms

## Development

### Running Tests
```bash
# Frontend tests
cd app/frontend
npm test

# Backend tests (if available)
cd app/backend
python -m pytest
```

### Building for Production
```bash
# Build frontend
cd app/frontend
npm run build
