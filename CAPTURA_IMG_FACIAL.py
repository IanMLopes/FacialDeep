from flask import Flask, request, jsonify
import os
from tqdm import tqdm
import cv2
import requests
import threading
from time import sleep
import base64
# import json
# import cmake
import numpy as np
import face_recognition
import dlib
from PIL import Image
import numpy as np


class sendImage():
    def __init__(self) -> None:
        self.validation = False
    
    def enviar_imagem(self, capturaImage):
        while True:
            if self.validation:
            # print('aqui')
                try:
                    ret, image = capturaImage.read()
                    imagem_base64 = base64.b64encode(cv2.imencode('.jpg', image)[1])
                    imagem_base64_str = imagem_base64.decode('utf-8')
                    arquivos = {'imagem': imagem_base64_str}
                    resposta = requests.post('http://127.0.0.1:5000/verify/', json=arquivos)

                    if resposta.status_code == 200:
                        data = resposta.json()
                        print(data)
                    else:
                        print("Erro ao enviar imagem. Código de status:", resposta.status_code)
                except Exception as e:
                    print("Erro durante o envio da imagem:", e)
  
    def read_frame(self, cam):
        while True:
            try:
                _, frame = cam.read()

                face_locations = face_recognition.face_locations(frame)

                if( len(face_locations) >= 1):
                    self.validation = True

                    for face_location in face_locations:
                        top, right, bottom, left = face_location

                        start_point = (right, top)
                        end_point = (left, bottom)

                        cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
                        cv2.imshow('Frame', frame)

                else:
                        cv2.imshow('Frame', frame)
                        
                if(cv2.waitKey(1) == ord('q')):
                    break
            except Exception as err:
                pass
        cv2.destroyAllWindows()
    

p = sendImage()

def captureImage():
    capturaImage = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

    capturaImage.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capturaImage.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    capturaImage.set(cv2.CAP_PROP_FOCUS, 50)
    capturaImage.set(cv2.CAP_PROP_EXPOSURE, 5)


    tr_qr = threading.Thread(target=p.enviar_imagem, args=(capturaImage,))
    tr_imgShow = threading.Thread(target=p.read_frame, args=(capturaImage,))
    tr_qr.start()
    tr_imgShow.start()

    while True:
        pass

captureImage()