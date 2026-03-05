# Loan Prediction AI

A full-stack machine learning application that predicts whether a loan applicant will be approved or rejected based on their demographic and financial profile. 

Built with a Random Forest model, served via FastAPI, with a modern glassmorphism frontend interface.

LINK:- https://subscription-prediction-app.onrender.com/

## Features

- **Machine Learning**: 81% accurate Random Forest Classifier handling categorical and numerical data imputation.
- **FastAPI Backend**: High-performance REST API for serving predictions.
- **Modern UI**: A responsive, aesthetic web interface built with pure HTML, CSS, and JS (no heavy frameworks).
- **Dockerized**: Ready for immediate cloud deployment.

## Project Structure

```text
├── backend/
│   └── main.py          # FastAPI application & model inference
├── frontend/
│   ├── index.html       # Web application UI
│   ├── script.js        # API integration logic
│   └── styles.css       # Glassmorphism aesthetic styling
├── DataSet.csv          # Training data (Loan profiles)
├── train_model.py       # Script to train and save the ML model
├── model.pkl            # Serialized Random Forest model pipeline
├── requirements.txt     # Python dependencies
└── Dockerfile           # Docker configuration for cloud deployment
```

## Running Locally

### Prerequisites
- Python 3.9+
- pip

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (Optional)
If you want to re-train the model on your own device:
```bash
python train_model.py
```
This will generate the `model.pkl` file.

### 3. Run the Server
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
Then open `http://localhost:8000` in your web browser to use the application.

## Deployment

This app is fully prepared for one-click deployment using **Render**, **Railway**, or **Heroku**.

### Deploying on Render (Free)
1. Fork or push this repository to your GitHub account.
2. Sign up at [Render](https://render.com/).
3. Create a **New Web Service**.
4. Connect your GitHub account and select this repository.
5. Render will automatically detect the `Dockerfile` and build your application.
6. Once deployed, you will get a live URL to share your application!

## Dataset Information

The model requires the following features for prediction:
* `Gender` (Male/Female)
* `Married` (Yes/No)
* `Dependents` (0, 1, 2, 3+)
* `Education` (Graduate/Not Graduate)
* `Self_Employed` (Yes/No)
* `ApplicantIncome` (Numeric)
* `CoapplicantIncome` (Numeric)
* `LoanAmount` (Numeric)
* `Loan_Amount_Term` (Numeric)
* `Credit_History` (1.0 for Good, 0.0 for Bad)
* `Property_Area` (Urban/Semiurban/Rural)

Git & GitHub

