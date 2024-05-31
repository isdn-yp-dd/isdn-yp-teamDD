import elements # self-define
import pandas as pd
import numpy as np
from datetime import datetime
import os

timestamp = datetime.now().strftime("%m%d-%H%M%S")
path = f"AI/dataset/{timestamp}"

file_bus = f"{path}/bus.csv"
file_stop = f"{path}/stop.json"

# get #
def getBus() -> pd.DataFrame:  # getBus(True) to get the record
  return pd.read_csv(file_bus)

def getStop() -> pd.DataFrame:  # getStop(True) to get the record
  return pd.read_json(file_stop)

# init #
def handleStop_init() -> None:  # init the stop
  df = pd.DataFrame(np.zeros((1, len(elements.Stop.list_obj[:-1])), dtype=np.int8),
                    columns=["Stop" + str(i) for i in range(len(elements.Stop.list_obj[:-1]))])
  saveStop(df)

def handleBus_init() -> None:  # init the bus
  df = pd.DataFrame(columns=['id', 'seats', 'state'])
  saveBus(df)

def init() -> None:  # init all stuff
  os.chdir(os.path.dirname(__file__))
  os.makedirs(path, exist_ok=True)
  handleStop_init()
  handleBus_init()

# handle #
def handleBus(id:int, seats:int, state:int, time:int) -> None:
  df = getBus()
  if id in df['id'].values :
    if (state == 7) :
      df = df.drop(df[df['id'] == id].index)
    else :
      df.loc[df['id'] == id, 'seats'] = seats
      df.loc[df['id'] == id, 'state'] = state
  else :
    row = pd.DataFrame([[id, seats, 0]], columns=['id', 'seats', 'state'])
    df = pd.concat([df, row])
  saveBus(df)
  print(f"{time} - (Bus , {id}, {seats}, {state})")  # print the seats (when get on/off)

def handleStop(index:int, change:int, time:int) -> None:  # change the amount of ppl at the stop queue
  if (change == 0) :
    return
  df = getStop()
  df.loc[0]["Stop" + str(index)] += change
  saveStop(df)
  print(f"{time} - (Stop , {index}, {change})")  # print the change of ppl (when hv changes)

# save #
def saveBus(df:pd.DataFrame) -> None:
  df.to_csv(file_bus, index=False)

def saveStop(df:pd.DataFrame, b = False) -> None:
  df.to_json(file_stop, orient='records')

## dataset ##
file_dataset = f"{path}/dataset"

def dataset_init() -> None:  # init the dataset
  stop = getStop()
  for i in range(len(stop.columns)) :
    df = pd.DataFrame(columns=['time', 'amount of ppl at the stop', 'amount of empty seats on the next minibus', "eta of the next minibus", "eta of the 2nd next minibus"])
    saveDataset(df, i)

def getDataset(i) -> pd.DataFrame:  # get the dataset
  df = pd.read_csv(f"{file_dataset}_{i}.csv")
  return df

def saveDataset(df:pd.DataFrame, i) -> None:  # save the dataset
  df.to_csv(f"{file_dataset}_{i}.csv", index=False)

def generate_dataset(t) :  # generate the dataset
  bus = getBus()
  stop = getStop()
  for i in range(len(stop.columns)) :
    df = getDataset(i)
    temp = [t, stop.values[0][i]]
    # state = 0-7, 0 is waiting start, state i is going station i
    # id of the next bus is the largest int <= i
    n1 = None  # n1 is the next bus
    n2 = None  # n2 is the 2nd next bus
    for row in bus.values :
      if (row[2] <= i) :
        if (n1) :
          n2 = row.tolist()
          break
        else :
          n1 = row.tolist()
    # print(f"{n1 = }, {n2 = }")
    if (not n1) :  # n1 & n2 missing
      temp.append(19)
      temp.append(elements.Stop.list_location[i] + elements.BUS_CYCLE - (t-1) % elements.BUS_CYCLE - 1)
      temp.append(elements.Stop.list_location[i] + elements.BUS_CYCLE * 2 - (t-1) % elements.BUS_CYCLE - 1)
    elif (not n2) :  # n2 missing, n1 exists
      temp.append(n1[1])
      temp.append(elements.Stop.list_location[i] - elements.Bus.list_obj[n1[0]].position)
      temp.append(elements.Stop.list_location[i] + elements.BUS_CYCLE - (t-1) % elements.BUS_CYCLE - 1)
    else :  # n1 & n2 exist
      temp.append(n1[1])
      temp.append(elements.Stop.list_location[i] - elements.Bus.list_obj[n1[0]].position)
      temp.append(elements.Stop.list_location[i] - elements.Bus.list_obj[n2[0]].position)
    row = pd.DataFrame([temp], columns=['time', 'amount of ppl at the stop', 'amount of empty seats on the next minibus', "eta of the next minibus", "eta of the 2nd next minibus"])
    df = pd.concat([df, row])
    saveDataset(df, i)

def toExcel() -> None:  # save the dataset to excel
  writer = pd.ExcelWriter(f"{file_dataset}.xlsx")
  for i in range(len(elements.Stop.list_obj[:-1])) :
    df = getDataset(i)
    df.to_excel(writer, sheet_name=f"Stop{i}", index=False)
  writer.close()
  writer = pd.ExcelWriter(f"{path}/output.xlsx")
  for i in range(1, len(elements.Stop.list_obj[:-1])) :
    df = pd.read_csv(f"{path}/output_{i}.csv")
    df.to_excel(writer, sheet_name=f"Stop{i}", index=False)
  writer.close()

def generate_output() -> None :
  for i in range(1, len(elements.Stop.list_obj[:-1])) :
    stop = elements.Stop.list_obj[i]
    temp = np.array(list(zip(stop.waiting_time, stop.waiting_num_bus)))
    df = pd.DataFrame(temp, columns=['waiting time', 'waiting num bus'])
    df.to_csv(f"{path}/output_{i}.csv", index=True)