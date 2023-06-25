import os
import sys
import matplotlib.pyplot as plt
import uvicorn
import numpy as np
from fastapi import HTTPException
from PIL import Image
from io import BytesIO
import tensorflow as tf
from fastapi import FastAPI,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
# Add the Training directory to the Python path
training_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Training'))
sys.path.append(training_path)

# Import the required modules
import preprocessing
import segmentation
import classification


app=FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL=tf.keras.models.load_model(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Models', 'fl_model.h5')))
CLASS_NAMES=['Black__Spot__fruits','Black__Spot__leaves','Citrus__Canker__fruits',
 'Citrus__Canker__leaves','Citrus__Scab__fruits','Healthy__fruits',
 'Healthy__leaves','Huanglongbing__fruits','Huanglongbing__leaves','Melanose__leaves']

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = read_file_as_image(contents)
        
        test_obj1 = preprocessing.IMAGE_PREPROCESSING(image)
        test_gen = test_obj1.PreprocessImage(CLASS_NAMES)
        img00 = (test_gen[0][0] * 255).round().astype(np.uint8)
        
        test_obj2 = segmentation.IMAGE_SEGMENTATION(img00)
        mask = test_obj2.AnalyzeImage()
        image = test_obj2.Segmentation(mask)

        float_image_array = (image.astype(np.float32) / np.max(image)) * 255
        # Round the float values to integers
        float_image_array = np.round(float_image_array).astype(np.uint8)

        arr = [float_image_array]
        array = np.array(arr)
        
        prediction = MODEL.predict(array)
        predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
        confidence = np.max(prediction[0]) * 100

        obj3=classification.CNN()
        solution=obj3.Solution(predicted_class)

        return {
            'class': predicted_class,
            'confidence': float(confidence),
            'solution': solution
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Failed to predict')

    

if __name__=="__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
