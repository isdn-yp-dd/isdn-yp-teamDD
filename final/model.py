import joblib
from sklearn.naive_bayes import CategoricalNB
import os

# load the model
model:CategoricalNB = joblib.load(f"{os.path.dirname(os.path.abspath(__file__))}/NB_model.pkl")

# return the expected number of minibus to wait
def predict(arr) -> int:

  # probability of getting in the first minibus
  prob = model.predict_proba(arr)[0][0]

  # expect getting in the first minibus if probability > 0.6
  if prob > 0.6 :
    return 1
  # expect getting in the second minibus if probability > 0.05
  elif prob > 0.05:
    return 2
  # nearly impossible to predict the waiting time accurately
  else:
    return 3