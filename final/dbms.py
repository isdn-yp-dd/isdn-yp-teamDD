import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import os
from model import predict
import requests
import time
import statistics
from ftplib import FTP

os.chdir(os.path.dirname(__file__))

try:
    conn = mysql.connector.connect(
        host="", 
        database="", 
        user="",  
        password="", 
        port=3306  # 3306 Default port for MySQL
    )
    cur = conn.cursor()
except Exception as e:
    print(f"Error connecting to the database: {e}")

ftp_details = {
            'host': '',
            'user': '',
            'password': '',
            'remote_path': ''
        }
ftp = FTP(ftp_details['host'])
ftp.login(ftp_details['user'], ftp_details['password'])

def insert_data(timestamp, eta1, eta2, eta3, count, alg_out, t, table='prediction'):
    """Insert data into the test table."""
    if conn is not None and cur is not None:
        try:
            cur.execute(f"INSERT INTO `{table}`(`time`, `eta1`, `eta2`, `eta3`, `ppl_count`, `alg_out`, `prediction_time`) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (timestamp, eta1, eta2, eta3, count, alg_out, t))
            conn.commit()
            # print(f"Data inserted")
        except Exception as e:
            print(f"Error inserting data: {e}")

def query_data():
    """Query data from the test table. If bus_id is provided, filter by bus_id. Save the results to a CSV file."""
    if conn is not None and cur is not None:
        try:
            cur.execute(f"SELECT * FROM `test`")
            rows = cur.fetchall()[-5:]
            ar = []
            for row in rows:
                ar.append(row[3])
            num = statistics.mode(ar) 
            return num
        except Exception as e:
            print(f"Error querying data: {e}")
            return []

def clear_table(table_name):
    """Clear all data in the test table."""
    if conn is not None and cur is not None:
        try:
            cur.execute(f"DELETE FROM {table_name};")
            conn.commit()
            print(f"All data cleared from table: {table_name}.")
        except Exception as e:
            print(f"Error clearing table: {e}")

def getETA() :
  try :
    url = "https://data.etagmb.gov.hk/eta/route-stop/2004791/1/7"
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data
    else:
      print("Failed")
      return None
  except Exception:
    print("Failed")


def real_time() :
    try :
        eta = getETA()['data']['eta']
        eta1 = -1
        eta2 = -1
        eta3 = -1
        try :
            eta1 = max(0, eta[0]['diff'])
            eta2 = max(0, eta[1]['diff'])
            eta3 = max(0, eta[2]['diff'])
        except :
            pass
        ppl_count = query_data()
        alg_out = predict([[ppl_count]])
        try :
            prediction_time = eta[alg_out-1]['diff']
        except :
            prediction_time = 0
        # insert_data(datetime.now(), eta1, eta2, eta3, ppl_count, alg_out, prediction_time)
        json_data = {
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'eta1': eta1,
            'eta2': eta2,
            'eta3': eta3,
            'ppl_count': ppl_count,
            'alg_out': alg_out,
            'prediction_time': prediction_time
        }
        df = pd.DataFrame(json_data, index=[0])
        print(df)
        df.to_json("real_time.json", orient='records')
        with open("real_time.json", 'rb') as file:
            ftp.storbinary(f'STOR {ftp_details["remote_path"]}', file)
        return df
    except Exception as e:
        print(e)
        return []

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    while True:
        df = real_time()
        time.sleep(5)