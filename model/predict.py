import pickle
import pandas as pd
import sklearn
import model

# import the model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

Model_version = '1.0.0'

class_labels = model.classes_.tolist()


def predict_premium(user_data: dict):
    input_df = pd.DataFrame([user_data])
    # make the prediction
    prediction_class = model.predict(input_df)[0]
    # probability of the prediction
    prediction_proba = model.predict_proba(input_df)[0].max()

    # create mapping of class labels to their corresponding probabilities
    proba_mapping = dict(zip(class_labels, model.predict_proba(input_df)[0]))

    return {
        'predicted_class': prediction_class,
        'Confidence': round(prediction_proba, 4),
        'class_probabilities': proba_mapping
    }
