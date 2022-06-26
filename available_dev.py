# importing subprocess
import subprocess
import os

# getting meta data of the wifi network
def wifi_names():
    osname = os.uname()
    if(osname[0] == "Linux"):
        data = subprocess.check_output(['nmcli', 'connection', 'show'])
        # decoding meta data from byte to string
        data = data.decode('utf-8', errors ="backslashreplace")
        data = data.split('\n')
        names = []
        for i in data:
            k=i.split()
            if(len(k)==0):
                pass
            else:
                names.append(k[0])
                print(i.split())
    return names
    
