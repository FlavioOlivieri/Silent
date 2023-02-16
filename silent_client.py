#Creato da: Flavio Olivieri e Davide Calella 5Bi IISS E. Majorana Martina Franca (TA) A.S. 2020/2021
#Ringraziamenti speciali a Nicholas Renotte (yt) e PyMike (yt)

import socket #rende possibile la creazione di un socket
import sys #serie di parametri che sono utili per interagire con il SO
import cv2 #libreria per streaming video in real-time
import numpy as np #supporto per grandi matrici e array multidimensionali
import pickle #per trasformare un oggetto in una serie di byte
import time #per manipolare date e tempo
import tkinter as tk #libreria per interfaccia grafica
from tkinter import * #libreria per interfaccia grafica
from PIL import ImageTk,Image #libreria per l'inserimento delle immagini nell'interfaccia grafica

home = tk.Tk() #creazione della finestra principale
home.geometry("1217x506") #dimensioni della finestra
home.title("Silent") #titolo della schermata
home.resizable(False,False) #non è possibile ridimensionare la finestra
home.configure(background="#99CCFF") #colore di sfondo (inutile con l'immagine)
home.iconbitmap("silent.ico") #icona della finestra

def invia_comandi(s): #funzione per l'invio dei comandi al server
    cap = cv2.VideoCapture(0) #inizializzo la webcam
    while True: 
        ret, frame = cap.read() #cattura il frame dalla webcam
        cv2.imshow('Silent', frame) #mostro la finestra della webcam
        cv2.waitKey(1) #tempo di attesa
        comando = pickle.dumps(frame) #codifica in byte della variabile frame
        #condizione che non si avvererà mai, per questo esce un warning, visto che inviamo immagini e non comandi
        if comando == "esc":
            s.send(comando.encode()) #invia il comando al server
            print("Sto chiudendo la connessione col Server. ")
            s.close() #chiude l'invio
            sys.exit() #esce dal programma
        else:
            s.send(comando) #invia il comando al server
            data = s.recv(4096) #riceve risposta dal server nel buffer
            data = data.decode() #decodifica la risposta da byte a stringa
            print(data) #stampa la risposta
            
def conn_sub_server(indirizzo_server): #funzione per la connessione al server
    try:
        s = socket.socket() #creazione socket 
        s.connect(indirizzo_server) #connessione al server
        print(f"Connessione al Server: {indirizzo_server} stabilita")
    except socket.error as errore: #eccezione che si attiva per un qualsiasi errore 
        print(f"Qualcosa è andato storto, sto uscendo..... \n{errore}")
        sys.exit() #esce dal programma
    invia_comandi(s) #funzione che passa il frame al server

def connessione(): #funzione che permette la connessione al server
    home.destroy() #chiusura della finestra grafica
    conn_sub_server(("192.168.1.140",15000)) #connessione tramite socket al server (questo è l'indirizzo server che viene passato), ovviamente da cambiare

def esci(): #funzione che fa uscire dal programma
    home.destroy() #chiusura della finestra grafica
    sys.exit() #esce dal programma
    
if __name__=="__main__": #capire se stia venendo eseguito come script a se stante, o se è invece stato richiamato come modulo
    my_menu = Menu(home) #creazione menu
    home.config(menu=my_menu) #inserimento del menu nella home

    img = ImageTk.PhotoImage(Image.open('./silent.png')) #dichiarazione immagine
    label = tk.Label(home, image=img)  #inserimento dell'immagine in una label
    label.pack() #inserimento dell'immagine nella GUI

    #configurazione del menu 1
    file_menu=Menu(my_menu)
    my_menu.add_command(label="Silent", command=connessione)

    #configurazione del menu 2
    my_menu2 = Menu(my_menu)
    my_menu.add_cascade(label="Altro", menu=my_menu2)
    my_menu2.add_command(label="Esci", command=esci)

    home.mainloop() #visualizza la GUI
    
