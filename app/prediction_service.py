import pandas as pd

from .model_loader import model


def predict_sustainability(data):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return float(prediction[0])