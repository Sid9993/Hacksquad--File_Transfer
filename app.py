from flask import Flask, render_template,request
from available_dev import wifi_names
from werkzeug.utils import secure_filename
import server_code
import os
import client_code

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/reciever")
def rec():
    return render_template('receiver.html')

@app.route("/server")
def ser():
    devices=wifi_names()
    return render_template('server.html', devices=devices[1:], name="anandhu")


@app.route("/serverShare", methods=['POST'])
def sShare():
    file=request.files["File Input"]
    filename = secure_filename(file.filename)
    print (filename)
    file.save(filename)
    s = server_code.create_connection()
    if(s==None and os.path.isfile(filename)):
        return "File recieved through common endpoint.... may be through mobile device"
    else:
        filesize = os.path.getsize(filename)
        server_code.send_file(s, filename, filesize)
        server_code.close_connection(s)
        os.remove(filename)
        return "file sent!"

    
@app.route("/recSide", methods=['POST'])
def recSide():
    s = client_code.create_connection()
    client_socket = client_code.conn_listening(s)
    client_code.recieve(client_socket, s)
    client_code.close_connection(s, client_socket)
    return "File recieved"


#to go to the virtualenv: source venv/Scripts/activate
#to deactivate: deactivate
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")