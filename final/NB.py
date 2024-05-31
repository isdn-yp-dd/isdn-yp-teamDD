import numpy as np
from sklearn.naive_bayes import CategoricalNB
import joblib
import os

def main() :
  log = [9, 5, 11, 6, 8, 12, 7, 5, 6, 6, 6, 10, 8, 10, 10]  # num = number of ppl can get in the bus ;record the number by ourself for data collection
  train = []
  for num in log:
    for i in range(num):  # num can get in the bus
      train.append([i, 0])  # 0 = can get in the next bus, 1 = cannot
    for i in range(num, 19):  # max is 18, >=19 100% cannot get in next bus
      train.append([i, 1])

  train = np.array(train)
  model = CategoricalNB(alpha=0.25).fit(train[:, 0].reshape(-1, 1), train[:, 1])  # with smoothing
  # model = CategoricalNB(alpha=0.001).fit(train[:, 0].reshape(-1, 1), train[:, 1])  # without smoothing
  joblib.dump(model, "NB_model.pkl")

  print()
  for i in range(19):
    output = model.predict(np.array([[i]]))
    prob = model.predict_proba(np.array([[i]]))  # can control expectation
    print(f"for the {i:2} th person at the queue, the probability of getting in the first minibus is {prob[0][0]*100:.1f}%\n")

if __name__ == "__main__":
  os.chdir(os.path.dirname(__file__))
  main()