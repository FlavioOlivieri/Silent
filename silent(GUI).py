import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image

home = tk.Tk()
home.geometry("1217x506")
home.title("Silent")
home.resizable(False,False)
home.configure(background="#99CCFF")
home.iconbitmap("silent.ico")

def colleziona_immagini():
    home.destroy()
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

def silent():
    home.destroy()
    #vengono riportati i path che serviranno al programma
    WORKSPACE_PATH = 'Tensorflow/workspace'
    SCRIPTS_PATH = 'Tensorflow/scripts'
    APIMODEL_PATH = 'Tensorflow/models'
    ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
    IMAGE_PATH = WORKSPACE_PATH+'/images'
    MODEL_PATH = WORKSPACE_PATH+'/models'
    PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'/pre-trained-models'
    CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
    CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/'
    import cv2 #libreria di intelligenza artificiale (opencv)
    import numpy as np #libreria che consente di lavorare con vettori e matrici in modo più efficiente e la chiameremo np, per richiamarla più facilmente
    from object_detection.utils import label_map_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
    import os #libreria che permette di interfacciarsi con il sistema operativo, per aiutare con i path
    from object_detection.utils import label_map_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
    from object_detection.utils import visualization_utils as viz_utils #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
    from object_detection.builders import model_builder #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
    from object_detection.utils import config_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
    import tensorflow as tf#libreria utilizzata per la creazione di reti neurali e la la chiameremo tf, per richiamarla più facilmente
    import time #libreria che permette di manipolare date e tempo, per aiutare con le pause

    #Carica la pipeline configurata e crea un modello su cui si basera l'identificazione
    configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    #Ripristina l'ultimo checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-4')).expect_partial() #in questo caso il programma è stato addestrato per 500 steps e il checkpoint più alto era il 2, ma se viene allenato di più, bisogna cambiare il ckpt

    @tf.function #questa è la funzione che il programma userà per l'identificazione
    def detect_fn(image): #viene passata l'immagine
        image, shapes = detection_model.preprocess(image) #l'immagine diventa 320x320
        prediction_dict = detection_model.predict(image, shapes) #qui fa la predizione
        detections = detection_model.postprocess(prediction_dict, shapes) #la predizione viene messa nella variabile detections
        return detections #faremo tornare quella predizione

    category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt') #è la rappresentazione della nostra label_map

    #Setta la webcam
    cap = cv2.VideoCapture(0) #utilizzo di opencv per inizializzare la webcam predefinita del dispositivo
    history = [] #creazione di un array che servirà per far uscire in output ciò che identifica
    word_old="" #creazione di una variabile d'appoggio per fare i confronti
    i=0 #creazione di un contatore

    while True: #per sempre
        ret, frame = cap.read() #cattura il frame della webcam
        image_np = np.array(frame) #convertiamo quel frame in un vettore numpy
    
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32) #convertiamo il tutto in tensorflow tensor
        detections = detect_fn(input_tensor) #avviene l'identificazione utilizzando la funzione
    
        num_detections = int(detections.pop('num_detections')) #abbiamo un numero di indentificazioni per darlo in pasto alla prossima istruzione
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections #viene identificato il num_detections

        # detection_classes deve essere intero
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64) #viene identificato il num_classes

        label_id_offset = 1 #specifichiamo il primo indice della label
        image_np_with_detections = image_np.copy()
    
        word = category_index[detections['detection_classes'][np.argmax(detections['detection_scores'])]+1]['name'] #trasforma il numpy.array in una stringa
        listaNumpy = (detections['detection_scores']).astype(float)  #mette i valori del vettore numpy in una lista di float
        massimo = (max(listaNumpy))*100 #mette in massimo il valore massimo rilevato
        massimo = int(massimo) #rende massimo intero
        if massimo > 40: #se rileva un valore con percentuale di riconoscimento maggiore di 70%, allora mi mostra il riquadro di riconoscimento
        #visualizza a schermo il box, la classe identificata e la percentuale di riconoscimento, una sorta di funzione a cui passiamo vari valori
            viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True, #usiamo le coordinate normali, per avere una corretta identificazione
                    max_boxes_to_draw=1, #numero di box disegnati
                    min_score_thresh=0.01, #soglia minima di riconoscimento, si può cambiare
                    agnostic_mode=False)
            if word_old == word: i=i+1 #se la lettera vecchia è uguale a quella appena trovata incrementa l'indice
            if word_old != word: i=0 #se la lettera vecchia è diversa a quella appena trovata riporta l'indice a 0
            if i>5: #se la stessa lettera è stata trovata per 5 volte di seguito allora...
                history.append(word) #mette la lettera nel vettore
                print(history) #stampa la lettera
                i=0 #riporta il contattore a 0
            word_old = word #mette la lettera in una variabile d'appoggio per effettuare dei confronti
            time.sleep(0.5) #pausa di 0.5 secondi tra un segno e l'altro

        cv2.imshow('Silent',  cv2.resize(image_np_with_detections, (800, 600))) #mostro a video la finestra che mi mostra ciò che la mia webcam sta vedendo in quel momento e ridimensiono il tutto
        if cv2.waitKey(1) & 0xFF == ord('q') : #se qualcosa va male possiamo premere il tasto di interruzione, in questo caso q (quit)
            cap.release() #rilasciamo la webcam alla fine dell'esecuzone del programma
            subprocess.run('scp parola_trovata.txt silent@semeraro.ddns.net:/var/www/html/silent', shell=True) #invio del file txt al server Linux 1, ovviamente da cambiare
            subprocess.run('scp parola_trovata.txt silent@giovane8.ddns.net:/var/www/html/silent', shell=True) #invio del file txt al server Linux 2, ovviamente da cambiare
            break #interruzione del programma
    parola = open("parola_trovata.txt", "w") #apre il file txt in scrittura
    history = "".join(history) #trasforma il vettore in stringa
    parola.write(history) #scrive nel file
    parola.close() #chiude il file
    cap.release()#rilasciamo la webcam alla fine dell'esecuzone del programma

def esci():
    home.destroy()

my_menu = Menu(home)
home.config(menu=my_menu)

img = ImageTk.PhotoImage(Image.open('./silent.png'))
label = tk.Label(home, image=img)
label.pack()

file_menu=Menu(my_menu)
my_menu.add_cascade(label="Avvia", menu=file_menu)
file_menu.add_command(label="Colleziona immagini", command=colleziona_immagini)
file_menu.add_separator()
file_menu.add_command(label="Silent", command=silent)

my_menu2 = Menu(my_menu)
my_menu.add_cascade(label="Altro", menu=my_menu2)
my_menu2.add_command(label="Esci", command=esci)

home.mainloop()



