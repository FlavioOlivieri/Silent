import cv2    #libreria di intelligenza artificiale (opencv)
import os      #libreria che permette di interfacciarsi con il sistema operativo, per aiutare con i path
import time  #libreria che permette di manipolare date e tempo, per aiutare con le pause
import uuid  #libreria che genera ID univoci, per nominare le immagini

IMAGES_PATH = 'Tensorflow/workspace/images/collectedimages'   #il path dove andranno salvate le immagini

labels = ['u','z']  #cartelle di immagini che si creeranno sotto il path precedente
number_imgs = 50 #numero di foto che il programma dovrà scattare per ogni label
i = 1 #semplice contatore

for label in labels:   #per ogni label presente in labels 
    os.mkdir ('Tensorflow/workspace/images/collectedimages//'+label)  #crea una cartella sotto il path di prima con il nome della label (se non funziona provare con makedirs)
    cap = cv2.VideoCapture(0) #utilizzo di opencv per inizializzare la webcam predefinita del dispositivo
    print('Colleziono immagini per {}'.format(label)) #una semplice print che mi dice per quale label il programma stia scattando foto
    time.sleep(3.5) #pausa tra una foto e l'altra (secondi)
    for imgnum in range(number_imgs): #per ogni immagine nel range del numero di foto scattate
        ret, frame = cap.read() #cattura il frame della webcam
        imgname = os.path.join(IMAGES_PATH, label, label+'.'+'{}.jpg'.format(str(uuid.uuid1()))) #do all'immagine il path completo, sommato al nome da avere in formato jpg (attraverso l'uso della libreria uuid)
        cv2.imwrite(imgname, frame) #salvo l'immagine in quel path 
        print('Numero immagine salvata:  ',i) #scrivo in output il numero dell'immagine appena salvata
        cv2.imshow('Silent', frame)  #mostro a video la finestra che mi mostra ciò che la mia webcam sta vedendo in quel momento
        #time.sleep(2.5) #altra pausa, stavolta di 2 secondi
        i=i+1 #incremento del contatore

        if cv2.waitKey(1) & 0xFF == ord('q'): #se qualcosa va male possiamo premere il tasto di interruzione, in questo caso q (quit)
            break #interruzione del programma
    cap.release() #rilasciamo la webcam alla fine dell'esecuzone del programma
