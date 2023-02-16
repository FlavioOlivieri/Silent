#Creato da: Flavio Olivieri e Davide Calella 5Bi IISS E. Majorana Martina Franca (TA) A.S. 2020/2021
#Ringraziamenti speciali a Nicholas Renotte (yt) e PyMike (yt)

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

import socket #rende possibile la creazione di un socket
import subprocess #fornisce interfaccia per lavorare a riga di comando
import cv2 #libreria per streaming video in real-time
import numpy as np #supporto per grandi matrici e array multidimensionali
import pickle #per trasformare un oggetto in una serie di byte
from object_detection.utils import label_map_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
import os #libreria che permette di interfacciarsi con il sistema operativo, per aiutare con i path
from object_detection.utils import label_map_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
from object_detection.utils import visualization_utils as viz_utils #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
from object_detection.builders import model_builder #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
from object_detection.utils import config_util #dalla libreria di intelligenza artificiale che rileva gli oggetti, importiamo i file che ci servono
import tensorflow as tf #libreria utilizzata per la creazione di reti neurali e la la chiameremo tf, per richiamarla più facilmente
import time #per manipolare date e tempo
import sys #serie di parametri che sono utili per interagire con il SO
import tkinter as tk #libreria per interfaccia grafica
from tkinter import * #libreria per interfaccia grafica
from PIL import ImageTk,Image #libreria per l'inserimento delle immagini nell'interfaccia grafica

home = tk.Tk() #creazione della finestra principale
home.geometry("1217x506") #dimensioni della finestra
home.title("Silent") #titolo della schermata
home.resizable(False,False) #non è possibile ridimensionare la finestra
home.configure(background="#99CCFF") #colore di sfondo (inutile con l'immagine)
home.iconbitmap("silent.ico") #icona della finestra

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
history = "" #creazione di una variabile stringa che rappresenta la parola trovata formata dai vari segni 
word_old = "" #creazione di una variabile d'appoggio per fare i confronti
i=0 #creazione di un contatore

def analizza_frame(frame): #funzione che riconosce il segno passatogli dal client
    global history #richiamo della variabile globale
    global word_old
    global i
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
    if massimo > 20: #se rileva un valore con percentuale di riconoscimento maggiore di 70%, allora mi mostra il riquadro di riconoscimento
        #visualizza a schermo il box, la classe identificata e la percentuale di riconoscimento, una sorta di funzione a cui passiamo vari valori
        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True, #usiamo le coordinate normali, per avere una corretta identificazione
                    max_boxes_to_draw=1, #numero di box disegnati
                    min_score_thresh=0.001, #soglia minima di riconoscimento, si può cambiare
                    agnostic_mode=False)
        if word_old == word:  i=i+1 #se la lettera vecchia è uguale a quella appena trovata incrementa l'indice
        if  word_old != word:  i=0 #se la lettera vecchia è diversa a quella appena trovata riporta l'indice a 0
        if  i>4: #se la stessa lettera è stata trovata per 5 volte di seguito allora...
             history = history+word #mette la lettera in append alla variabile
             print(history) #stampa la lettera
             i=0 #riporta il contattore a 0
             parola = open("parola_trovata.txt", "w") #apre il file txt in scrittura
             parola.write(history) #scrive nel file
             parola.close() #chiude il file
        word_old = word #mette la lettera in una variabile d'appoggio per effettuare dei confronti
        time.sleep(0.5) #pausa di 0.5 secondi tra un segno e l'altro

    cv2.imshow('Silent',  cv2.resize(image_np_with_detections, (800, 600))) #mostro la finestra della webcam
    if cv2.waitKey(1) & 0xFF == ord('q'): #se qualcosa va male possiamo premere il tasto di interruzione, in questo caso q (quit)
        print("Parola riconosciuta: ",history) #stampa della parola completa
        subprocess.run('scp parola_trovata.txt silent@semeraro.ddns.net:/var/www/html/silent', shell=True) #invio del file txt al server Linux 1, ovviamente da cambiare
        subprocess.run('scp parola_trovata.txt silent@giovane8.ddns.net:/var/www/html/silent', shell=True) #invio del file txt al server Linux 2, ovviamente da cambiare
        sys.exit() #esce dal programma
    return word #manda la lettera trovata al client

def ricevi_comandi(conn): #funzione che riceve i comandi dal client
    while True:
        richiesta = conn.recv(1048576) #buffer di ricezione della trasmissione (2^20) 1048576
        #condizione che non si avvererà mai, per questo esce un warning, visto che inviamo immagini e non comandi
        if pickle.loads(richiesta) == "esc": 
            conn.close() #chiude connessione
            break #ferma il programmaa
        else:
            frame = pickle.loads(richiesta) #decodifica della richiesta, da byte a frame di cv2
            word = analizza_frame(frame) #richiamo della funzione analizza frame
            print(word," : ",i) #stampa della lettera e dell'indice
            word = word.encode() #codifica da stringa a byte
            conn.send(word) #invia la lettera al client

def sub_server(indirizzo, backlog=1): #funzione che rende il server disponibile (backlog specifica il numero massimo di connessioni accodabili)
    try:
        s = socket.socket() #creazione socket 
        s.bind(indirizzo) #lega il socket all'indirizzo
        s.listen(backlog) #si mette in ascolto
        print("Server inizializzato, ora è in ascolto....")
    except socket.error as errore: #eccezione che si attiva per un qualsiasi errore
        print(f"Qualcosa è andato storto.... \n{errore}")
        print("Sto tentando di reinizializzare il Server...")
        sub_server(indirizzo, backlog=1) #richiama se stessa 
    conn, indirizzo_client = s.accept() #conferma della connessione avvenuta
    print(f"Connessione Server - Client Stabilita: {indirizzo_client} ")
    ricevi_comandi(conn) #richiama la funzione ricevi comandi

def connessione(): #funzione che permette al server di essere in ascolto
    home.destroy() #chiusura della finestra grafica
    while True: #while true per rendere sempre disponibile il server
        sub_server(("192.168.1.140",15000)) #connessione tramite socket al client, ovviamente da cambiare

def esci(): #funzione che fa uscire dal programma
    home.destroy() #chiusura della finestra grafica
    sys.exit() #esce dal programma

if __name__ == "__main__": #capire se stia venendo eseguito come script a se stante, o se è invece stato richiamato come modulo
    my_menu = Menu(home) #creazione menu
    home.config(menu=my_menu) #inserimento del menu nella home

    img = ImageTk.PhotoImage(Image.open('./silent.png')) #dichiarazione immagine
    label = tk.Label(home, image=img) #inserimento dell'immagine in una label
    label.pack() #inserimento dell'immagine nella GUI

    #configurazione del menu 1
    file_menu=Menu(my_menu) 
    my_menu.add_command(label="Silent", command=connessione) 

    #configurazione del menu 2
    my_menu2 = Menu(my_menu)
    my_menu.add_cascade(label="Altro", menu=my_menu2)
    my_menu2.add_command(label="Esci", command=esci)

    home.mainloop() #visualizza la GUI


