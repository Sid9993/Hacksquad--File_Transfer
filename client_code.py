#this file acts as the receiver here

#required modules are imported here
import socket
import tqdm
import os

#settings of the connection
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPERATOR>"


def create_connection():
    # creating socket connection
    # create the server socket
    # TCP socket
    s = socket.socket()
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    return s


def conn_listening(s):
    #listening for the connection
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")
    return client_socket

def recieve(client_socket, s):
    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    print(received[0].split(SEPARATOR))
    try:
        filename, filesize = received.split(SEPARATOR)
    except:
        print("File may be corrupted")
        s.close()
    # remove absolute path if there is
    filename = os.path.basename(filename) 
    filename = "templates/" + filename  
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


def close_connection(s, client_socket):
    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()

"""s = create_connection()
client_socket = conn_listening(s)
recieve(client_socket, s)
close_connection(s, client_socket)"""
