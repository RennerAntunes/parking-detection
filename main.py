import cv2
import numpy as np

vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]

cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    
    vagas_vazias = 0
    vagas_ocupadas = 0

    if not ret:
        break

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tresh = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,16)
    img_blur = cv2.medianBlur(tresh, 5)
    dilatada = cv2.dilate(img_blur, np.ones((3,3)))


    for x,y,w,h in vagas:
        spot = dilatada[y: y + h, x: x + w]
        brancos = cv2.countNonZero(spot)
        cv2.putText(frame, str(brancos), (x, (y+h)-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (136,255,244), 1)
        
        if brancos > 3000:
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,0,255), 3)
            vagas_ocupadas += 1
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 3)
            vagas_vazias += 1
        


    cv2.putText(frame, f"{vagas_vazias} vagas livres de 8", (30,45), cv2.FONT_HERSHEY_COMPLEX, 1, (136,45,4), 2)
    cv2.imshow("frame", frame)
    cv2.imshow("tresh", tresh)
    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()