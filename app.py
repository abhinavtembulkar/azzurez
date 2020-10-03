from export_model import imager, calculate, loop, loader_face, loader_mask
from flask import Flask, render_template, redirect, request, url_for

from binascii import a2b_base64
import base64

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import cv2

app = Flask(__name__)

visit = False
imageid = 0
net = ''
model = '' 
data = 'null'

@app.route('/')
def home():
    print('[INFO] Welcome')
    return render_template('welcome.html')


def predicts():   
    global visit, net, model, imageid

    imag, w, h = imager(f"./static/images/imagee{imageid}.png")
    detect = calculate(imag, net)
    image = loop(imag, detect, model, w, h)
    cv2.imwrite(f"static/results/imagee{imageid}.png",image)

    print('[INFO] Image Id : ',imageid)
    
    global data
    with open(f"./static/results/imagee{imageid}.png", "rb") as img_file:
        data = base64.b64encode(img_file.read()).decode('utf-8')
    data = 'data:image/png;base64,{}'.format(data)

    # socketio.emit('sent image',data)


@app.route('/webcam')
def webcam():
    global visit, net, model
    
    if visit == False:
        net = loader_face()
        model = loader_mask()
        visit = True    
    
    return render_template("webcam.html")

@app.route('/webcam',methods=['POST'])
def inputer():    
    global imageid
    imageid += 1

    input = request.values['imgBase64']
    bin_data = a2b_base64(input)
    fii = open(f'./static/images/imagee{imageid}.png','wb')
    fii.write(bin_data)
    fii.close()

    try:
        predicts()
    except :
        print('[INFO] Error !!')
        # socketio.emit('prederror')

    return redirect(url_for('results'))

@app.route('/result')
def results():
    print('[INFO] Results')
    global data
    return render_template("result.html",content = data)

if __name__ == "__main__":
    app.run(debug=True)