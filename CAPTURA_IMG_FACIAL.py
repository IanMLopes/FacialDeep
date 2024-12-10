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
import io


class sendImage():
    def __init__(self) -> None:
        self.validation = False
    
    def enviar_imagem(self, capturaImage):
        # while self.validation:
        while True:
            if self.validation:
                try:
                    ret, image = capturaImage.read()
                    x,y,h,w = ((333, 106, 658, 430))
                    cutimage = image[y:y+w, x:x+h]
                    
                    self.validation = False
                    print(' self.validation --->', self.validation)

                    cv2.imshow('Frame', cutimage)
                
                    _, img_encoded = cv2.imencode('.jpg', cutimage)
                    img_bytes = io.BytesIO(img_encoded.tobytes())
                    files = {
                        'file': ('imagem.jpg', img_bytes, 'image/jpeg'),
                        'jig': 1

                    }
                    cv2.waitKey(300)
                    # resposta = requests.post('http://127.0.0.1:5000/embedding/', files=files)
                    resposta = requests.post('http://127.0.0.1:5000/verify/', files=files)
                    # resposta = requests.post('http://10.58.72.190:5051/api/Biometric/verify-jig-face', files=files)
                    print(' resposta ', resposta)

                    if resposta.status_code == 200:
                        data = resposta.json()
                        if data:                     
                            print('data:', data)   
                            # print('Embedding:', data['data']['embedding'])
                            # print('Nome: ', data['data']['name'], ' - ' 'Registro: ', data['data']['register'])
                            # print('Nome: ', data['data']['name'], ' - ' 'Registro: ', data['data']['register'], ' - ' 'Registro: ', data['data']['distance'])
                            self.validation = True
                        else:
                            print('Não encontrado')
                    else:
                        print("Erro ao enviar imagem. Código de status:", resposta.status_code)
                except Exception as e:
                    print("Erro durante o envio da imagem:", e)
            else:
                print('Face não identificado')

    def read_frame(self, cam):
        while True:
            try:
                _, frame = cam.read()

                # roi = cv2.selectROI(frame)
                # print(roi)  
                x,y,h,w = ((333, 106, 658, 430))
                cutFrame = frame[y:y+w, x:x+h]

                face_locations = face_recognition.face_locations(cutFrame)

                if( len(face_locations) >= 1):
                    self.validation = True

                    for face_location in face_locations:
                        top, right, bottom, left = face_location
                        start_point = (right, top)
                        end_point = (left, bottom)

                        cv2.rectangle(cutFrame, start_point, end_point, (0, 255, 0), 2)
                        cv2.imshow('Frame', cutFrame)

                else:
                        cv2.imshow('Frame', cutFrame)
                        self.validation = False
                        
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


    tr_imgShow = threading.Thread(target=p.read_frame, args=(capturaImage,))
    tr_qr = threading.Thread(target=p.enviar_imagem, args=(capturaImage,))
    tr_qr.start()
    tr_imgShow.start()

    while True:
        pass

captureImage() 