from fastapi import FastAPI
from fastapi import UploadFile,File
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
from io import BytesIO
import uvicorn
from typing import Tuple

app = FastAPI()

# Load the model
model = load_model('best_model.h5')

class_labels = ['glioma', 'healthy', 'meningioma', 'pituitary']

# Load the model
model = load_model('best_model.h5')

def read_file_as_image(data) -> Tuple[np.ndarray, Tuple[int, int]]: # A function to read the image file as a numpy array
    img = Image.open(BytesIO(data)).convert('RGB') # Open the image and convert it to RGB color space
    img_resized = img.resize((128,128), resample=Image.BICUBIC) # Resize the image to 180 x 180
    image = np.array(img_resized) # Convert the image to a numpy array
    image = image / 255.0
    return image, img_resized.size # Return the image and its size

@app.get('/')
def root():
    return {'message': 'Welcome to the Brain Tumor Detection API'}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image, img_size = read_file_as_image(await file.read()) # Read the image file
    img_batch = np.expand_dims(image, 0) # Add an extra dimension to the image so that it matches the input shape of the model

    predictions = model.predict(img_batch) # Make a prediction
    predicted_class = class_labels[np.argmax(predictions[0])] # Get the predicted class
    confidence = np.max(predictions[0]) # Get the confidence of the prediction

    return { # Return the prediction
    'class': predicted_class,   
    'confidence': float(confidence) 
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)