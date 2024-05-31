import mymodel
import time
import numpy as np

# def custom_weight(distances) :
#   weight = np.where(distances == 0, 100, 1/distances)
#   return weight

print("\nLoading the model & Prediction")
datasets = mymodel.getDatasets()
input, t = mymodel.getIO(datasets[5][-2], num=False)
for n in [50] :
  times = []
  for i in range(100) :
    model = mymodel.load(f"KNN-{n}", 3)
    be = time.time()
    model.predict(input[:1000])
    af = time.time()
    times.append(af-be)
  print(f"Using k = {n} : {sum(times)/len(times):.4f} seconds / 1000 predictions")

print("\n\n\n")
