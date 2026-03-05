from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI(title="Loan Prediction API")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the static files (frontend)
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))


# Global variable to hold the model
model = None

# Define the input schema
class PredictionInput(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

@app.on_event("startup")
def load_model():
    global model
    try:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/")
def read_root():
    return {"message": "Loan Prediction API is running"}

@app.post("/predict")
def predict_subscription(data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
        
    try:
        # Convert input data to a Pandas DataFrame
        input_data = data.dict()
        df = pd.DataFrame([input_data])
        
        # Predict using the loaded model pipeline
        prediction = model.predict(df)
        probability = model.predict_proba(df)
        
        # Convert prediction back to string label
        result = "Approved" if prediction[0] == 1 else "Rejected"
        confidence = float(probability[0][1]) if result == "Approved" else float(probability[0][0])
        
        return {
            "prediction": result,
            "confidence": round(confidence * 100, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
