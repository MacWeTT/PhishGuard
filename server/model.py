import pickle
from typing import List


loaded_model = pickle.load(open("./ML_Model/XGBoostClassifier.pickle.dat", "rb"))


def checkForPhishing(data: dict) -> None:
    predictions = loaded_model.predict(data)
    probabilities = loaded_model.predict_proba(data)
    print(predictions, probabilities)
