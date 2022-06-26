
#this file acts as the sender here


#dependency modules
import socket
import tqdm
import os

#settings
seperator = "<SEPERATOR>"
buffersize = 4096
# the ip address or hostname of the receiver
host = "hostid"
# the port, let's use 5001
port = 5004
# the name of file we want to send, make sure it exists
#filename = "/home/user/Desktop/basics.sh"
# get the file size
#filesize = os.path.getsize(filename)

def create_connection():
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    try:
        s.connect((host, port))
        print("[+] Connected.")
        return s
    except:
        print("Connection filed.....!")
        return None
    


def send_file(s, filename, filesize):
    #file sending part
    # send the filename and filesize
    s.send(f"{filename}{seperator}{filesize}".encode())
    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(buffersize)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))


def close_connection(s):
    # close the socket
    s.close()

"""s = create_connection()
send_file(s)
close_connection(s)"""