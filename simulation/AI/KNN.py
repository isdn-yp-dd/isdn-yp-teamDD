# KNeighborsClassifier model predicting the time to wait

from mymodel import *
# from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in divide")

def custom_weight(distances) :
  weight = np.where(distances == 0, 100, 1/distances*2)
  return weight

def custom_metric(x, y) :  # assume x is the input to predict
  distance = np.sum(np.abs(x - y))
  if (x[2] <= y[2]) or (x[3] <= y[3]) :  # eta of example is smaller
    offset += 50
  else :
    offset = 0
  return distance + offset
    
datasets = getDatasets()
fig, axes = plt.subplots(3, 2)
axes[0][0].set_title("Stop 0")
writer = pd.ExcelWriter(f"{os.path.dirname(datasets[0][-1])}/KNN.xlsx")
print()
for stop in range(1, 6) :
  print(f"For {stop = }")

  df = pd.DataFrame(columns=['n_neighbors', 'mae', 'within 10% error', '20%'])
  for n_neighbors in [50] :
    input = np.array([])
    output = np.array([])
    for dataset in datasets[stop][:-1] :
      temp1, temp2 = getIO(dataset, num=False)
      input = np.append(input, temp1)
      output = np.append(output, temp2)

    input = input.reshape(-1, temp1.shape[1])
    weight = [5, 1, 1, 1]
    input = input * weight
    model = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance', metric='manhattan')

    model.fit(input, output)

    test = getIO(datasets[stop][-1], num=False)
    test[0] = test[0] * weight
    predicted = model.predict(test[0])
    df2 = pd.DataFrame(predicted, columns=['predicted'])
    df2.to_csv(f"{os.path.dirname(datasets[0][-1])}/predicted_{stop}.csv", index=True)
    # ma(predicted)
    ae = np.subtract(predicted, test[1])
    mae = np.abs(ae).mean()
    mae = round(mae, 4)
    correct_10 = np.where(np.abs(np.subtract(test[1],predicted)) < (np.multiply(test[1], 0.1)), 1, 0).mean()
    correct_20 = np.where(np.abs(np.subtract(test[1],predicted)) < (np.multiply(test[1], 0.2)), 1, 0).mean()
    correct_10 = round(correct_10*100, 4)
    correct_20 = round(correct_20*100, 4)
    print(f"    n-neighbors(k) = {n_neighbors:2} : mae = {mae:.1f}, within 10% error = {correct_10:.1f}%, within 20% error = {correct_20:.1f}%")
    row = pd.DataFrame([[n_neighbors, mae, correct_10, correct_20]], columns=df.columns)
    df = pd.concat([df, row])
    if (n_neighbors == 50) :
      pltPredict_sub(test[1], predicted, f"KNN-custom_metric2({n_neighbors}) : Stop {stop}", axes[stop//2, stop%2])
      # plotError_sub(ae, axes[stop//2, stop%2], f"freq-error : Stop {stop}")
    save(f"KNN-{n_neighbors}", model, stop)
  df.to_excel(writer, sheet_name=f"Stop{stop}", index=False)

print()
writer.close()
plt.subplots_adjust(hspace=0.35)
plt.legend()
plt.show()