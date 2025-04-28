""" RonAaron - Mouse Virtual"""
#https://pyautogui.readthedocs.io/en/latest/
#https://google.github.io/mediapipe/solutions/hands.html

import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui as pg

cam = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

screenWidth, screenHeight = pg.size()   #Ukuran dari gambarnya
print(screenWidth, screenHeight)

frameR = 100

tipid = [4,8,12,16,20]  #ID dari tiap ujung jari, source webnya mediapipe

clk = 1

while True:
    succes, img = cam.read()

    img = cv.flip(img, 1)

    h,w,c = img.shape

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    cv.rectangle(img, (frameR, frameR), (w-frameR, h-frameR), (255,0,0), 2) #Menggambar kotak di gambar

    if (results.multi_hand_landmarks):

        tangan = results.multi_handedness[0].classification[0].label    #Mengecek ari mana yang nampoak 
        if tangan == "Right":   #Kode hanya jalan ketika tangan kanan yang muncul - bisa kalian hapus kalo ingin - jangan lupa geser ke kiri lagi semua fungsinya tapi ya
            lmlist = []

            for handLms in results.multi_hand_landmarks:
                for id, landmarks in enumerate(handLms.landmark):
                    cx, cy = int(landmarks.x*w), int(landmarks.y*h)
                    lmlist.append([id,cx,cy])

            #mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)   #gambar di img, point titik, garis koneksinya

            """Jumlah jari"""
            fingers = []
            if lmlist[tipid[0]][1] < lmlist[tipid[0]-2][1]: #JEMPOL
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):   #JARI TELUNJUKJ - KELINGKING
                if lmlist[tipid[id]][2] < lmlist[tipid[id]-3][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            """Kode ngegerakin mousenya"""
            if fingers == [0,1,1,0,0]:
                cv.circle(img, (lmlist[12][1], lmlist[12][2]), 10, (0,0,255), cv.FILLED)    #Menggambar lingkaran di jari tengah

                X = np.interp(lmlist[12][1], (frameR, w-frameR), (0, screenWidth))  #Nilai sumbu X Akhir
                Y = np.interp(lmlist[12][2], (frameR, h-frameR), (0, screenHeight)) #Nilai sumbu Y Akhir

                length = abs(lmlist[8][1] - lmlist[12][1])  #Panang jarak X antara jari tengah dan ari telunjuk

                pg.moveTo(X, Y, duration = 0.3)

                #CLICK
                if (lmlist[8][2] > lmlist[7][2]) and clk > 0:
                    pg.click()
                    clk = -1
                elif (lmlist[8][2] < lmlist[7][2]):
                    clk = 1
                
                #DRAG
                if length > 50:
                    #pg.mouseDown(button = 'left')
                    pg.scroll(100)
                else:
                    pg.scroll(-100)
                    #pg.mouseUp(button = 'left')

    cv.imshow("webcam", img)

    if cv.waitKey(20) & 0xFF==ord('d'): #Ketika tombol 'd' ditekan looping berhenti
        break

cv.destroyAllWindows()