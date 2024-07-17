"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import shutil
import os
from send_to_server import predict_and_send  # Import the prediction function

app = FastAPI()

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

# Define a Pydantic model for prediction data
class Prediction(BaseModel):
    class_name: str
    confidence: float

# Define a Pydantic model for the entire request data
class PredictionData(BaseModel):
    image: str
    detections: List[Prediction]

@app.post("/receive_data/")
async def receive_data(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Perform the prediction
        prediction_results = predict_and_send(temp_file_path)
        
        # Delete the temporary file
        os.remove(temp_file_path)
        
        # Return the predictions
        return {"status": "success", "predictions": prediction_results}
    
    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Run the server with uvicorn if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import shutil
import os
from send_to_server import predict_and_send  # Import the prediction function

app = FastAPI()

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

# Define a Pydantic model for prediction data
class Prediction(BaseModel):
    class_name: str
    confidence: float

# Define a Pydantic model for the entire request data
class PredictionData(BaseModel):
    image: str
    detections: List[Prediction]

# POST endpoint to receive and process an uploaded image
@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Perform the prediction
        prediction_results = predict_and_send(temp_file_path)
        
        # Delete the temporary file
        os.remove(temp_file_path)
        
        # Return the predictions
        return {"status": "success", "predictions": prediction_results}
    
    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# GET endpoint to retrieve predictions (dummy example)
#@app.get("/predictions/{prediction_id}")
@app.get("/predictions/")
async def get_prediction(prediction_id: str):
    # Here you could implement logic to retrieve predictions by ID from a database or storage
    # For now, we return a dummy response
    #dummy_predictions = [
     #   {"class_name": "Potato Blight", "confidence": 0.85},
      #  {"class_name": "Healthy Potato", "confidence": 0.92}
    #]
    #return {"status": "success", "predictions": dummy_predictions}
    return {"status": "success", "predictions": []}

# Run the server with uvicorn if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


