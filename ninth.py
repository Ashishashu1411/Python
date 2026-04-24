# logistic_regression_sklearn_reduced.py
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load data
X, y = load_breast_cancer(return_X_y=True)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Pipeline: scaling + logistic regression
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("logreg", LogisticRegression(max_iter=1000, solver="lbfgs"))
])

# Baseline
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

print("Baseline Accuracy =", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Grid Search
param_grid = {
    "logreg__C": [0.01, 0.1, 1, 10, 100],
    "logreg__penalty": ["l2"],
    "logreg__solver": ["lbfgs", "newton-cg"],
}

grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

print("Best CV Accuracy =", grid.best_score_)
print("Best Params =", grid.best_params_)

# Tuned model
best_model = grid.best_estimator_ 
y_pred_tuned = best_model.predict(X_test)

print("\nTuned Accuracy =", accuracy_score(y_test, y_pred_tuned))
print("\nConfusion Matrix (Tuned): \n", confusion_matrix(y_test, y_pred_tuned))
print("\nClassification Report (Tuned): \n", classification_report(y_pred_tuned, y_pred_tuned))