# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file (if you have it)
COPY requirements.txt .

# Install the necessary dependencies
RUN pip install -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose both ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Command to start both FastAPI and Streamlit in the background
CMD uvicorn app:app --host 0.0.0.0 --port 8000 & \
    streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0