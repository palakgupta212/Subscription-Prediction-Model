import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def main():
    print("Loading dataset...")
    df = pd.read_csv('DataSet.csv')
    
    # Drop ID column as it's not predictive
    if 'Loan_ID' in df.columns:
        df = df.drop(columns=['Loan_ID'])
        
    # Map target variable to 1/0
    df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})
    
    X = df.drop(columns=['Loan_Status'])
    y = df['Loan_Status']
    
    # Define categorical and numerical features
    categorical_features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    numeric_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
    
    # Create preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    # Append classifier to preprocessing pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))])
                          
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training the model... (this may take a moment)")
    clf.fit(X_train, y_train)
    
    print("Evaluating the model...")
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Saving the model pipeline to model.pkl...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)
        
    print("Model saved successfully.")

if __name__ == "__main__":
    main()
