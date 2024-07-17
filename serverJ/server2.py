"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import csv
import os

app = FastAPI()

# Path to the CSV file for storing predictions
CSV_FILE = "C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/serverJ/predictions.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['prediction_id', 'class_name', 'confidence'])

# Define a Pydantic model for prediction data
class Prediction(BaseModel):
    class_name: int
    confidence: float

# Define a Pydantic model for the request body
class PredictionRequest(BaseModel):
    predictions: list[Prediction]

# POST endpoint to receive prediction results
@app.post("/save_predictions/")
async def save_predictions(request: PredictionRequest):
    try:
        # Generate prediction_id
        prediction_id = str(uuid.uuid4())
        
        # Save prediction_id and predictions to CSV file
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            for prediction in request.predictions:
                writer.writerow([prediction_id, prediction.class_name, prediction.confidence])
        
        print(f"Predictions saved with ID: {prediction_id}")
        
        # Return success response
        return {"status": "success", "prediction_id": prediction_id, "predictions": request.predictions}
    
    except Exception as e:
        print(f"Error saving predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# GET endpoint to retrieve the latest predictions
@app.get("/latest_predictions/")
async def get_latest_predictions():
    try:
        # Read predictions from CSV file
        result_predictions = []
        with open(CSV_FILE, mode='r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header row
            for row in reader:
                result_predictions.append({"prediction_id": row[0], "class_name": int(row[1]), "confidence": float(row[2])})
        
        if result_predictions:
            print(f"Retrieved predictions: {result_predictions}")
            return {"status": "success", "predictions": result_predictions}
        else:
            print("No predictions found")
            raise HTTPException(status_code=404, detail="No predictions found")
    
    except Exception as e:
        print(f"Error retrieving predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Run the server with uvicorn if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import csv
import os

app = FastAPI()

# Path to the CSV file for storing predictions
CSV_FILE = "C:/Users/JenyThev/Downloads/POTATO_DISEASE_DETECTION/PDD_Phase2_V3/Potato-Disease-Detection/serverJ/predictions-new.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['prediction_id', 'class_name', 'confidence'])

# Define a Pydantic model for prediction data
class Prediction(BaseModel):
    class_name: str
    confidence: float

# Define a Pydantic model for the request body
class PredictionRequest(BaseModel):
    predictions: list[Prediction]

# POST endpoint to receive prediction results
@app.post("/save_predictions/")
async def save_predictions(request: PredictionRequest):
    try:
        # Generate prediction_id
        prediction_id = str(uuid.uuid4())
        
        # Save prediction_id and predictions to CSV file
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            for prediction in request.predictions:
                writer.writerow([prediction_id, prediction.class_name, prediction.confidence])
        
        print(f"Predictions saved with ID: {prediction_id}")
        
        # Return success response
        return {"status": "success", "prediction_id": prediction_id, "predictions": request.predictions}
    
    except Exception as e:
        print(f"Error saving predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# GET endpoint to retrieve the latest predictions
@app.get("/latest_predictions/")
async def get_latest_predictions():
    try:
        # Read predictions from CSV file
        result_predictions = []
        with open(CSV_FILE, mode='r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header row
            for row in reader:
                result_predictions.append({"prediction_id": row[0], "class_name": row[1], "confidence": float(row[2])})
        
        if result_predictions:
            print(f"Retrieved predictions: {result_predictions}")
            return {"status": "success", "predictions": result_predictions}
        else:
            print("No predictions found")
            raise HTTPException(status_code=404, detail="No predictions found")
    
    except Exception as e:
        print(f"Error retrieving predictions: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Run the server with uvicorn if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)