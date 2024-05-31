import eta
import time
from datetime import datetime
import os
import pandas as pd

os.chdir(os.path.dirname(__file__))
os.makedirs("asset", exist_ok=True)
timestamp = datetime.now().strftime("%m%d-%H%M")
file = f"asset/{timestamp}.csv"

df = pd.DataFrame(columns=['time', 'stop', 'eta1', 'eta2', 'eta3'])
while True:
  line = eta.get_time()
  for ele in line :
    df = pd.concat([df, pd.DataFrame([ele], columns=['time', 'stop', 'eta1', 'eta2', 'eta3'])])
  df.to_csv(file, index=False)
  print()
  time.sleep(5)