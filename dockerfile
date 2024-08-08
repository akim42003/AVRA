# Use an official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /app

# Copy the backend files into the container
COPY backend/ ./backend/
COPY requirements.txt .

# Install backend dependencies
RUN pip install -r requirements.txt

# Install Node.js, npm, and ffmpeg
RUN apt-get update && apt-get install -y nodejs npm ffmpeg

# Copy the frontend files and build the React app
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Set the working directory back to the backend
WORKDIR /app/backend

# Expose the port the app runs on
EXPOSE 5001

# Set the command to run the backend
CMD ["python", "app.py"]
