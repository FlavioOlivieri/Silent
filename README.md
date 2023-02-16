# Silent
Translator Sign Language - Italian

Questo progetto si chiama Silent e ha come obiettivo quello di aiutare le persone audiolese
a comunicare attraverso un riconoscimento in real-time dei segni. Questi segni verranno 
associati alle corrispettive lettere dell'alfabeto e da ciò si potrà ottenere una parola.
Attraverso la parola, sarà possibile ottenere delle informazioni con delle query al database,
che saranno visualizzate nell'app mobile ed esposte attraverso un text-to-speech.

Step per il funzionamento del programma (se vuoi rifare le foto dei segni da capo):
1.1) Scaricare il template da: https://github.com/nicknochnack/RealTimeObjectDetection, 
oppure scaricarlo dal prompt, utilizzando il comando git clone + link (opportunatamente 
aggiunto al cmd)
1.2) Avviare il programma collected_images.py (opportunatamente commentato), selezionare il
nome delle cartelle che si vogliono creare e il numero di immagini che il programma dovrà
fotografare
1.3) Uscire le foto dalle cartelle appena create e inserirle tutte insieme nella cartella
"collectedimages" e poi eliminare le cartelle appena svuotate
1.4) Spostarsi con il cmd nella cartella "Tensorflow". Con la git clone scaricare un 
programma per il label delle immagini da questo link: https://github.com/tzutalin/labelImg
1.5) Spostarsi con il cmd nella cartella che si è appena venuta a creare e avviare il 
programma con: python labelimg.py
1.6) Open Dir e selezionare la cartella collectedimages, fare la stessa cosa con Change Save
Dir e abilitare dal menù View, l'Auto Save Mode. Premere "w" e selezionare l'area della mano
e il nome del gesto, questo processo andrà ripetuto per tutte le immagini e creerà dei file 
xml che conterrà tutte le informazioni della selezione che noi abbiamo fatto (posizione, 
nome, altezza, larghezza...)
1.7) Ora le immagini andranno divise per le cartelle train e test. Es: abbiamo 15 immagini
per segno + relativi file xml, andranno messe 13 immagini + xml nella cartella test e il
resto nella cartella train, questo processo andrà ripetuto per tutti i segni (la scelta di 
come dividere le immagini spetta all'utente)
1.8) Installare jupyter, tutorial a questo link: https://jupyter.org/install (installare
jupyter notebook)
1.9) Avviare jupyter spostandosi nella cartella RealTimeObjectDetection e dal cmd inserire:
jupyter notebook, si avvierà jupyter sul browser predefinito. Aprire il file Tutorial.ipynb
1.10) Da qui in poi si illustreranno i vari step (si omette il fatto che per ogni step
bisogna cliccare il bottone run presente sulla barra in alto, per qualche errore bisogna
controllare se il bottone in alto sia impostato su trusted):
0. Setup Paths: sono i vari path che ci serviranno per il nostro programma
1. Create Label Map: verrà creata una "mappa" con le nostre classi (quindi bisogna modificare
il nome e l'id)
2. Create TF records: verrano creati dei record in riferimento al train e al test, serviranno
per il training del programma, sono file specifici che tensorflow usa per il suo object
detection API
3. Download TF Models Pretrained Models from Tensorflow Model Zoo: spostarsi nella cartella
Tensorflow e verrà scaricato con la git clone da github la cartella models (la libreria
ufficiale di tensorflow per la object detection)
4. Copy Model Config to Training Folder: questo passaggio funziona per metà. Crea la cartella,
sostituendo a "!mkdir" "makedirs", ma non copia il file pipeline.config, quindi bisogna farlo 
a mano: andare nella cartella pre-trained-models e poi ssd_mobilenet... e copiare il file 
pipeline.config nella cartella models, my_ssd_mobnet
5. Update Config For Transfer Learning: modifica il file pipeline.config appena copiato,
bisogna modificare a mano solo il num_classes con il numero delle nostre classi
6. Train the model: il programma verrà addestrato attraverso questo comando da inserire nel 
cmd. Bisogna spostarsi nella cartella RealTimeObjectDetection e incollare il comando, farà 
tutto da solo (il numero di steps, sarà a scelta dell'utente)
1.11) Sono presenti anche gli step 7 e 8, ma sono stati copiati e modificati nel file silent.
py, quindi bisogna aprirlo e avviarlo, il programma dovrebbe riconoscere il segno che la mano
ha fatto, mostrando a video, il nome del segno e la percentuale di riconoscimento e poi,
salverà la parola in un file txt. Il programma sarà opportunatamente commentato.

Step per il funzionamento del programma (se vanno bene i segni già inseriti):
1) Avviare silent(GUI) se vuoi il programma solo su un pc Windows (cliccare il pulsante avvia nella
GUI e poi silent)
1.1) Avviare silent server sul server e silent client sul client se si vuole il programma splittato
(cliccare il pulsante silent nella GUI sia nel client, sia nel server, a questo punto il programma
effettuare il collegamento tra client e server)
2) Verrà aperta una finestra di riconoscimento, se riconosce per 5 volte consecutivamente il segno,
verrà inserito nella parola, premere q per fermare il programma e salvare la parola.
3) La parola verrà inviata automaticamente al server
4) Le informazioni saranno disponibili sull'app
5) Il programma sarà tutto commentato
6) Le immagini dei segni sono disponibili in \Tensorflow\workspace\images\test o train, il file jpg
dei segni è affidabile, ma la lettera B è americana e per altre piccole modifiche è consigliata la
visione del path sopracitato

This project is called Silent and aims to help deaf people
to communicate through real-time sign recognition. These signs will come
associated with the corresponding letters of the alphabet and from this a word can be obtained.
Through the word, it will be possible to obtain information with database queries,
which will be displayed in the mobile app and exposed through a text-to-speech.

Steps for the functioning of the program (if you want to redo the photos of the signs from scratch):
1.1) Download the template from: https://github.com/nicknochnack/RealTimeObjectDetection,
or download it from the prompt, using the command git clone + link (suitably
added to cmd)
1.2) Start the collected_images.py program (properly commented), select the
name of the folders that you want to create and the number of images that the program will have to
photograph
1.3) Take the photos out of the newly created folders and put them all together in the folder
"collectedimages" and then delete the folders you just emptied
1.4) Move with the cmd in the "Tensorflow" folder. With the git clone download a
image label program from this link: https://github.com/tzutalin/labelImg
1.5) Move with the cmd to the folder that has just been created and start the
program with: python labelimg.py
1.6) Open Dir and select collectedimages folder, do the same with Change Save
Dir and enable the Auto Save Mode from the View menu. Press "w" and select the hand area
and the name of the gesture, this process will be repeated for all images and will create files
xml which will contain all the information of the selection we have made (position,
name, height, width...)
1.7) Now the images will be divided by the train and test folders. Ex: we have 15 images
by sign + related xml files, 13 images + xml will be placed in the test folder and the
rest in the train folder, this process will be repeated for all signs (the choice of
how to split the images is up to the user)
1.8) Install jupyter, tutorial at this link: https://jupyter.org/install (install
jupyter notebooks)
1.9) Start jupyter moving to the RealTimeObjectDetection folder and from the cmd enter:
jupyter notebook, it will start jupyter on the default browser. Open the Tutorial.ipynb file
1.10) From here on, the various steps will be illustrated (the fact is omitted that for each step
you have to click the run button on the top bar, for some errors you have to
check if the top button is set to trusted):
0. Setup Paths: these are the various paths that we will need for our program
1. Create Label Map: a "map" will be created with our classes (so we need to modify
name and id)
2. Create TF records: records will be created in reference to the train and the test, they will be needed
for program training, they are specific files that tensorflow uses for its object
detection API
3. Download TF Models Pretrained Models from Tensorflow Model Zoo: navigate to folder
Tensorflow and will be downloaded with the git clone from github the models folder (the library
officer of tensorflow for object detection)
4. Copy Model Config to Training Folder: This step works halfway. Create folder,
replacing "!mkdir" with "makedirs", but it doesn't copy the pipeline.config file, so you have to
by hand: go to the pre-trained-models folder and then ssd_mobilenet... and copy the file
pipeline.config in the models folder, my_ssd_mobnet
5. Update Config For Transfer Learning: Edit the pipeline.config file you just copied,
you have to manually change only the num_classes with the number of our classes
6. Train the model: the program will be trained through this command to be inserted in the
cmd. You need to navigate to RealTimeObjectDetection folder and paste the command, it will do
all by itself (the number of steps, will be chosen by the user)
1.11) Steps 7 and 8 are also present, but they have been copied and modified in the file silent.
py, so you need to open and run it, the program should recognize the sign that the hand
did, showing the name of the sign and the percentage of recognition on the screen and then,
will save the word in a txt file. The program will be suitably commented.

Steps for the functioning of the program (if the signs already entered are fine):
1) Start silent(GUI) if you want the program only on a Windows pc (click the start button in the
GUI and then silent)
1.1) Start silent server on the server and silent client on the client if you want the program split
(click the silent button in the GUI both in the client and in the server, at this point the program
connect between client and server)
2) A recognition window will pop up, if it recognizes the sign 5 times consecutively,
will be inserted into the word, press q to stop the program and save the word.
3) The word will be sent automatically
