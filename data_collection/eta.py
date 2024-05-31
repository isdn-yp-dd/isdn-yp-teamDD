import requests
import subprocess
from datetime import datetime
import os

def get(route_id, route_seq, stop_seq) :
  try :
    url = f"https://data.etagmb.gov.hk/eta/route-stop/{route_id}/{route_seq}/{stop_seq}"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data
    else:
      print("Failed")
      return None
  except Exception:
    print("Failed")
  
def get_time() :
  line = []
  for i in range(1, 8):
    eta = get(2004791, 1, i)['data']['eta'] 
    print(str(i) + " : " + str(eta[0]['diff']) + " , " + str(eta[1]['diff']) + " , " + str(eta[2]['diff']))
    ele = [datetime.now().strftime("%H%M%S"), i, str(eta[0]['diff']), str(eta[1]['diff']), str(eta[2]['diff'])]
    line.append(ele)
  return line

if __name__ == "__main__":
  os.chdir(os.path.dirname(__file__))
  subprocess.run("cls", shell=True)
  get_time()