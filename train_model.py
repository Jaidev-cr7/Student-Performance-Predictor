import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("student.csv")

X = df[['attendance', 'internal_marks', 'assignments', 'previous_gpa']]
y = df['pass_fail']

encoder = LabelEncoder()
y = encoder.fit_transform(y)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, "rf_model.pkl")
joblib.dump(encoder, "label_encoder.pkl")

print("Model trained and saved.")
