# RF model predicting the time to wait

from mymodel import *
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datasets = getDatasets()
fig, axes = plt.subplots(2, 3)
writer = pd.ExcelWriter(f"{os.path.dirname(datasets[0][-2])}/RF.xlsx")
for stop in range(1, 6) :

  df = pd.DataFrame(columns=['mae', 'correct% with 15% error', '20%'])
  input = np.array([])
  output = np.array([])
  for dataset in datasets[stop][:-2] :
    temp1, temp2 = getIO(dataset, num=False)
    input = np.append(input, temp1)
    output = np.append(output, temp2)

  input = input.reshape(-1, temp1.shape[1])
  # standardize_list(input, [1,2])
  model = RandomForestRegressor(n_estimators=50)

  model.fit(input, output)

  test = getIO(datasets[stop][-2], num=False)
  # standardize_list(test[0], [1,2])
  predicted = model.predict(test[0])
  # smooth(predicted)
  mae = np.abs(np.subtract(test[1],predicted)).mean()
  mae = round(mae, 4)
  correct_15 = np.where(np.abs(np.subtract(test[1],predicted)) < (np.multiply(test[1], 0.15)), 1, 0).mean()
  correct_20 = np.where(np.abs(np.subtract(test[1],predicted)) < (np.multiply(test[1], 0.2)), 1, 0).mean()
  correct_15 = round(correct_15*100, 4)
  correct_20 = round(correct_20*100, 4)
  print(f"For {stop = } : mae = {mae:.3f}, correct percentage with 15% error = {correct_15:.3f}, with 20% error = {correct_20:.3f}")

  row = pd.DataFrame([[mae, correct_15, correct_20]], columns=df.columns)
  df = pd.concat([df, row])
  pltPredict_sub(test[1], predicted, f"RF : Stop {stop}", axes[stop//3, stop%3])
  df.to_excel(writer, sheet_name=f"Stop{stop}", index=False)

  save("RF", model, stop)
writer.close()
plt.legend()
plt.show()