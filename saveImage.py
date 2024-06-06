import cv2
from connection import ConnectionDb
import os
import psycopg2
from psycopg2 import sql

connect = ConnectionDb()


PATHIMG = "C:/Users/bc2g8321/Desktop/PROJETOS_ICCT/COMPAL/sistema/TESTES_COMPAL/imgs/"

list = os.listdir(PATHIMG)

class saveImg:

    def save(self):
        
        con = connect.connection()
        cur = con.cursor()

        # with open('image.jpg', 'rb') as file:
        # image_data = file.read()
        id = 6
        for img in list:

            if 'jpg' in img:
                image = PATHIMG+img
                with open(image, 'rb') as file:
                    image_data = file.read()

                bytea_data = psycopg2.Binary(image_data)

                try:
                    cur.execute(
                        sql.SQL("INSERT INTO employee (id, name, photo ) VALUES (%s, %s, %s)"),
                        [id, img, bytea_data]
                    )
                    con.commit()
                    print("Image inserted successfully.")
                    id += 1
                except psycopg2.Error as e:
                    con.rollback()
                    print("Error inserting image:", e)


q = saveImg()
q.save()