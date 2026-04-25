import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Sample dataset
data = {
    "area": [1000, 1500, 1800, 2400, 3000, 3500, 4000, 1200, 2200, 2800],
    "bedrooms": [2, 3, 3, 4, 4, 4, 5, 2, 3, 4],
    "age": [10, 8, 5, 2, 1, 3, 4, 12, 7, 3],
    "price": [50, 75, 90, 120, 150, 165, 180, 60, 110, 140]
}
df = pd.DataFrame(data)

# Features & target
X = df[["area", "bedrooms", "age"]]
y = df["price"]   # ✅ fixed quote

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Model
model = LinearRegression()
model.fit(X_train, y_train)

# Parameters
print("Intercept:", model.intercept_)
print("Coefficients:", model.coef_)

# Prediction
y_pred = model.predict(X_test)
print("\nActual Prices:", list(y_test))
print("Predicted Prices:", y_pred)

# Evaluation
print("\nR² Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))