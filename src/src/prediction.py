"""Modèle de prédiction du risque de fraude."""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_prediction_model(input_file):
    """Entraîne un modèle de classification des fraudes."""

    data = pd.read_csv(input_file)

    features = data[["estimated_amount", "fraud_score"]]
    target = data["is_fraud"]

    if target.nunique() < 2:
        raise ValueError("Il faut au moins deux classes pour entraîner le modèle.")

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target
    )

    model = LogisticRegression()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy
