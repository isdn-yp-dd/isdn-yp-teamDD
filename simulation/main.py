import_string = \
'''
import numpy as np
import pandas as pd
'''
### LINK START! (https://github.com/evnchn/linkstart.py)
for line in import_string.splitlines():
    if "import" in line:
        #print(line)
        try:
            exec(line)
        except:
            if "#" in line:
                package_name = line.split("#")[-1]
            else:
                splits = line.split("import")
                if "from" in line:
                    package_name = splits[0].replace("from","")
                else:
                    package_name = splits[1]
            package_name = package_name.strip()
            #print("Installing {}...".format(package_name))    
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            try:
                exec(line)
            except:
                print("Failed to install {}".format(package_name))
### DONE
from elements import *  # self-define
import datahandling  # self-define
import mytk  # self-define
import os

def main() :
    ### init ###
    path = os.path.dirname(__file__)
    os.chdir(path)

    # init the bus stop (location, P_queue, P_off)
    Stop(0, 50, 0) # start , most ppl get in, 0 ppl get off
    Stop(90, 7.5, 20) # 1
    Stop(318, 12, 35) # 2
    Stop(366, 10, 10) # 3
    Stop(404, 7, 15) # 4
    Stop(488, 5, 20) # 5
    Stop(553, 0, 100) # end , 0 ppl get in, all ppl get off
    datahandling.init()
    datahandling.dataset_init()

    ### simulation ###
    for time in range(MAX_TIME + 1) : 
    # if (time % 50 == 0) :  # show the progress
    #   print(f"{time = }")
        loop(time)
    #   mytk.update(time)
    datahandling.generate_output()
    datahandling.toExcel()
    print(f"\nSimulation finished!\n{MAX_TIME = }")
    # mytk.mainloop()

if __name__ == "__main__" :
    main()
    
    import subprocess
    subprocess.run(["python", "AI/KNN.py"])