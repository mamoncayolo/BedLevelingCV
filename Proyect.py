import cv2
import numpy as np

#Captar la imagen por video
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)

#Determinacion de rangos de deteccion de color
redBajo1=np.array([45,60,70],np.uint8)
redAlto1=np.array([70,255,255],np.uint8)


#######################################################
while True:

	ret, frame = cap.read()
	ancho=frame.shape[1]
	largo=frame.shape[0]
	
	if ret == False: break
	#frame = imutils.resize(frame, width=1080)
	puntos = [[0,0], [0,largo], [ancho,0], [ancho,largo]]			
	pts1 = np.float32(puntos)
	pts2 = np.float32([[0,0], [ancho,0], [0,largo], [ancho,largo]])
	M = cv2.getPerspectiveTransform(pts1, pts2)
	imagen_A4 = cv2.warpPerspective(frame, M, (ancho,largo))

	

	if imagen_A4 is not None:
		puntos = []
		imagenHSV = cv2.cvtColor(imagen_A4, cv2.COLOR_BGR2HSV)
		verdeBajo = np.array([45, 60, 70], np.uint8)
		verdeAlto = np.array([70, 255, 255], np.uint8)
		maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)

		cnts = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:2]

		for c in cnts:
			x, y, w, h = cv2.boundingRect(c)
			cv2.rectangle(imagen_A4, (x, y), (x+w, y+h), (255, 0, 0), 2)
			puntos.append([x, y, w, h])

		if len(puntos) == 2:
			x1, y1, w1, h1 = puntos[0]
			x2, y2, w2, h2 = puntos[1]
			
			if x1 < x2:
				distancia_pixeles = abs(x2 - (x1+w1)) 
				distancia_cm = (distancia_pixeles*29.7)/720
				cv2.putText(imagen_A4, "{:.2f} cm".format(distancia_cm), (x1+w1+distancia_pixeles//2, y1-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
				cv2.line(imagen_A4,(x1+w1,y1-20),(x2, y1-20),(0, 0, 255),2)
				cv2.line(imagen_A4,(x1+w1,y1-30),(x1+w1, y1-10),(0, 0, 255),2)
				cv2.line(imagen_A4,(x2,y1-30),(x2, y1-10),(0, 0, 255),2)
			else:
				distancia_pixeles = abs(x1 - (x2+w2))
				distancia_cm = (distancia_pixeles*29.7)/720
				cv2.putText(imagen_A4, "{:.2f} cm".format(distancia_cm), (x2+w2+distancia_pixeles//2, y2-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
				cv2.line(imagen_A4,(x2+w2,y2-20),(x1, y2-20),(0, 0, 255),2)
				cv2.line(imagen_A4,(x2+w2,y2-30),(x2+w2, y2-10),(0, 0, 255),2)
				cv2.line(imagen_A4,(x1,y2-30),(x1, y2-10),(0, 0, 255),2)

		
		''''##IMPRESION DE LA IMAGEN VERTICAL
		M1=cv2.getRotationMatrix2D((ancho//2, largo//2),-90,1)
		imagen_A41 = cv2.warpAffine(imagen_A4, M1, (ancho,largo))'''
		cv2.imshow('imagen_A4',imagen_A4)

	cv2.imshow('frame',frame)	
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()








