import joblib
import pandas as pd
import Utils as utils

# loading the pre-trained models
loaded_model = joblib.load("models/model.sav")
loaded_cvec = joblib.load("models/countvectorizer.sav")


def get_file_classifier(content):
    df = pd.DataFrame(content, columns=['file_content'])
    bow = loaded_cvec.transform(df['text'])
    predicted_val = loaded_model.predict(bow)
    return utils.get_file_classifer_from_label(predicted_val[0])
