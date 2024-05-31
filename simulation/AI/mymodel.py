import joblib
import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import math

def getDatasets() -> list:
  os.chdir(os.path.dirname(__file__))
  datasets = []
  for i in range(6) :
    temp = glob.glob(f"dataset/*/dataset_{i}.csv")
    datasets.append(temp)
  return datasets

def getArray(file) -> np.ndarray:
  return pd.read_csv(file, ).values

def getIO(file, num:bool) -> list:
  input = getArray(file)
  if num :
    output = getArray(file.replace("dataset_", "output_"))[:, 2]  # get the wait num bus
  else :
    output = getArray(file.replace("dataset_", "output_"))[:, 1]  # get the wait time
  input = input[:len(output),1:]
  return [input, output]

def standardize(input:np.ndarray) -> np.ndarray:
  return (input - np.mean(input)) / np.std(input, ddof=1)

def standardize_list(input:np.ndarray, col:list) -> np.ndarray:
  for i in col :
    input[:, i] = standardize(input[:, i])
  return input

def smooth(predict:np.ndarray) -> np.ndarray:
  for i in range(5, len(predict)-10) :
    predict[i] = np.mean(predict[i-5:i+10])
  return predict

def ma(predict:np.array) -> np.array:
  alpha = 0.5
  for i in range(10, len(predict)) :
    history = np.mean(predict[i-10:i])
    if (history > predict[i]) :
      predict[i] = (1-alpha)*history + alpha*predict[i]
  return predict
    
def prediction_on_eta(eta:np.array, predict:np.array) -> int:  # return the prediction based on the eta
  eta1 = eta[:, 0]
  eta2 = eta[:, 1]
  eta3 = eta2 * 2 - eta1
  diff1 = np.abs(eta1 - predict)
  diff2 = np.abs(eta2 - predict)
  diff3 = np.abs(eta3 - predict)
  for i in range(len(predict)) :
    if (diff1[i] < diff2[i]) :
      predict[i] = eta1[i]
    elif (diff2[i] < diff3[i]) :
      predict[i] = eta2[i]
  return predict

def num_to_time(num:np.array, eta:np.array) -> np.array:
  predict = np.zeros(len(num))
  for i in range(len(num)) :
    if num[i] < 3 :
      predict[i] = eta[i, int(num[i]-1)]
    else :
      predict[i] = eta[i,1] + (eta[i,1] - eta[i,0]) * (num[i]-2)
  return predict

def pltPredict(test:np.ndarray, predicted:np.ndarray, title:str,) -> None:
  plt.plot(test, label='True', color='blue')
  plt.plot(predicted, label='Predicted', color='red', linewidth=0.5)
  plt.title(title)
  plt.legend()
  plt.show()

def plotError_sub(error_list:np.ndarray, ax, title) -> None:
  errors = error_list[error_list != 0]
  small = abs(math.floor(min(errors) / 100) * 100)
  big = abs(math.ceil(max(errors) / 100) * 100)
  if small > big :
    big = small
  else :
    small = big
  levels = np.arange(-small, big+1, 100)
  digitized = np.digitize(errors, levels)
  frequency = np.bincount(digitized, minlength = len(levels))
  ax.bar(levels, frequency, width=100, align='edge', color='blue')
  ax.axvline(errors.mean(), linestyle='dashed', color='red', linewidth=.75, label='mean error')
  ax.set_title(title)
  return frequency


def pltPredict_sub(test:np.ndarray, predicted:np.ndarray, title:str, ax) -> None:
  ax.plot(predicted, label='Predicted', color='red', linewidth=0.75)
  ax.plot(test, label='Truth', color='blue')
  ax.set_title(title)

def save(name, model, stop) -> None:
  # Save the model to a file
  os.chdir(os.path.dirname(__file__))
  os.makedirs(f"model/{stop}", exist_ok=True)
  joblib.dump(model, f"model/{stop}/{name}.pkl")

def load(name, stop) :
  # Load the model from a file
  os.chdir(os.path.dirname(__file__))
  model = joblib.load(f"model/{stop}/{name}.pkl")
  return model