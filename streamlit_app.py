import streamlit as st
import requests
from PIL import Image

# Function to send the image to FastAPI and get prediction
def get_prediction(image_file):
    url = "http://localhost:8000/predict/"
    files = {"file": image_file}
    response = requests.post(url, files=files)
    return response.json()

# Streamlit UI
st.title("Brain Tumor Classification")

# File uploader to upload images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# Placeholder for displaying the result
result_placeholder = st.empty()

# If an image is uploaded, show it
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Create a 'Predict' button
    if st.button('Predict'):
        # Send the image to FastAPI for prediction
        result = get_prediction(uploaded_file.getvalue())
        
        result_placeholder.write(result)