import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Training data
X_train = [
    "Experienced Python developer with Machine Learning and SQL skills",
    "Skilled in JavaScript, React, Node.js, and GitHub projects",
    "Strong communication and leadership with project management experience",
    "No relevant skills or experience",
    "Looking for any job, no skills listed",
    "Basic computer knowledge, no programming experience"
]

y_train = [1, 1, 1, 0, 0, 0]  # 1 = Good resume, 0 = Bad resume

# Create pipeline
model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", LogisticRegression())
])

# Train model
model.fit(X_train, y_train)

# Save model to a file
joblib.dump(model, "resume_model.pkl")
print("Model trained and saved as resume_model.pkl")
