from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import sqlite3
from database import insert_prediction

app = FastAPI()

# ---------------- CORS FIX ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------- LOAD MODEL ---------------
model = joblib.load("rf_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# -------------- INPUT MODEL ---------------
class InputData(BaseModel):
    attendance: int
    internal_marks: int
    assignments: int
    previous_gpa: float

# -------------- PREDICT API ---------------
@app.post("/predict")
def predict(data: InputData):
    features = [[
        data.attendance,
        data.internal_marks,
        data.assignments,
        data.previous_gpa
    ]]

    prediction = model.predict(features)[0]
    prediction_label = encoder.inverse_transform([prediction])[0]

    insert_prediction(
        data.attendance,
        data.internal_marks,
        data.assignments,
        data.previous_gpa,
        prediction_label
    )

    return {"Prediction": prediction_label}

# --------------- HISTORY API --------------
@app.get("/history")
def get_history():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "attendance": row[1],
            "internal_marks": row[2],
            "assignments": row[3],
            "previous_gpa": row[4],
            "prediction": row[5],
            "timestamp": row[6]
        }
        for row in rows
    ]
