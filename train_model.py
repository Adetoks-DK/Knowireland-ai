import pandas as pd

# Load dataset
df = pd.read_csv("datasets/sustainability_dataset.csv")
print(df["sustainability_score"].describe())

print(df.head())

print(df.info())

print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

df.drop_duplicates(inplace=True)
import matplotlib.pyplot as plt

plt.hist(df["sustainability_score"], bins=20)
plt.title("Distribution of Sustainability Scores")
plt.xlabel("Score")
plt.ylabel("Number of Companies")
plt.show()
print(df.corr(numeric_only=True))
X = df[
    [
        "employees",
        "annual_revenue",
        "energy_consumption",
        "water_consumption",
        "waste_generated",
        "recycling_rate",
        "renewable_energy",
        "transport_emissions",
        "carbon_emissions"
    ]
]

y = df["sustainability_score"]
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("MAE:", mae)
print("MSE:", mse)
print("R²:", r2)
import joblib
from sklearn.ensemble import RandomForestRegressor

# Train the model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "trained_models/sustainability_model.pkl")

print("Model saved successfully!")

