# WALKER
Le bracelet connecté pour la randonnée liée à l'application GEOTREK.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=hwP3JeXwsJ0
" target="_blank"><img src="http://img.youtube.com/vi/hwP3JeXwsJ0/0.jpg" 
alt="Walker" width="240" height="180" border="10" /></a>


# DOCUMENTATION WALKER
Pour ce projet, nous avons utilisé :
une Raspberry PI 3 possédant un module BLE;
un module SenseHat muni d’un carré de LED, d’un accéléromètre, d’un magnétomètre;
une clé GPS ;
une clé 3G/GMS Huawei E3531. 

Pour l’application qui est reliée à la RPI 3,  nous avons choisi l’application Geotrek Mobile qui utilise les technologies suivantes:  Cordova 3.6, AngularJS 1.2, Ionic beta 9, Leaflet, jQuery, Bourbon et les outils : Grunt, Bower, Sass.
Voir les installations à faire pour l’application sur : https://github.com/GeotrekCE/Geotrek-mobile



LIGNES DE COMMANDES RPI :

## INSTALLATION DU BLUETOOTH SUR LA RPI3
Pour implémenter le Bluetooth Low Energy entre le bracelet et l’application Cordova, il faut faire quelques installations sur la RPI3.
### Installer les logiciels, pi-bluetooth, bluez et blueman
sudo apt-get install pi-bluetooth
(Bluez et Blueman devraient déjà être installé si vous utilisez une Raspbian Jessie)
sudo apt-get install bluetooth bluez blueman
Redémarrez  la RPI3
sudo reboot

[Référence](http://helloraspberrypi.blogspot.fr/2016/03/setup-bluetooth-for-raspberry-pi.html)

### Mettre en place le “Serial Port Profile” SPP sur la Pi. 
Modifier ce fichier:
sudo nano /etc/systemd/system/dbus-org.bluez.service 
Ajouter ‘-C’ à la fin de la ligne ‘'ExecStart=' line,  pour démarrer le démon bluetooth en mode 'compatibilité'.
Ajoutez un nouveau 'ExecStartPost =' immédiatement après cette ligne, pour ajouter le profil SP.
Les deux lignes devraient ressembler à ceci:
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP

Sauvegarder et redémarrez la RPI3

Voilà vous avez maintenant réussi à mettre en place le Bluetooth sur la RPI3 ! 

### Executer les scripts au démarrage de la RPI3
Utilisez CRON pour exécuter un fichier au démarrage de la pi 
Ouvrir un terminal et entrez cette ligne de commande 
sudo crontab -e 
2.  Ajouter à la fin du fichier: 
@reboot username /usr/bin/python  absolute_path_to_file 	
Selon l’architecture de nos fichiers, nous avons écrit cette commande
@reboot username /usr/bin/python /home/pi/Documents/Test_BLE/init.py
@reboot permet au fichier d'être exécuté au démarrage de la RPI3.

3. Redémarrez la RPI3 pour enregistrer les modifications.

[Référence](https://stackoverflow.com/questions/30005635/why-doesnt-my-python-script-open-a-text-file-when-run-via-cron?lq=1)

## INSTALLATION DE LA LIBRAIRE SENSEHAT 
sudo apt-get install sense-hat 



## UTILISATION DU GPS
Avant de brancher la clé GPS à la Raspberry Pi, exécutez la commande suivante pour faire les installations nécessaires :
```sudo apt-get install python gpsd gpsd-clients```
Vous pouvez ensuite brancher la clé GPS à la Raspberry Pi, et exécuter la commande :
```cgps```
Vous devriez voir les informations reçues par le GPS dans votre terminal. Si aucune valeur ne s’affiche, c’est surement que le GPS n’arrive à se connecter à aucun satellite. Il est préférable d’être à l’extérieur ou vers une fenêtre et d’attendre quelques instants pour que le GPS capte une localisation.
Votre clé GPS est maintenant prête à être utilisée par le code de Walker.

Référence: http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/ 




## ENVOI DE SMS 
Afin d’envoyer un SMS depuis une Raspberry Pi, il faut installer le logiciel Gammu. Gammu est un logiciel libre de gestion de téléphone portable fonctionnant sous Linux ou Windows. Il permet de gérer l’envoi de SMS (avec ou sans accusé de réception), la gestion du répertoire, des appels et la création de sauvegardes (messages, répertoires). Ici nous nous intéressons uniquement à l’envoi de SMS.
Branchez votre clé GSM à un port USB de la Raspberry Pi. Dans notre cas, nous avons utilisé une clé Huawei E3531. Ci-dessous un lien contenant la liste des clés compatibles avec Gammu : 
https://fr.wammu.eu/phones/
### Vérifiez si la clé est bien détectée par le système et compatible. 
```dmesg | grep tty | grep usb``` 

exemple de résultat obtenu : 

 	[ 5806.660785] usb 1-1.5: GSM modem (1-port) converter now attached to ttyUSB0
 	[ 5806.662796] usb 1-1.5: GSM modem (1-port) converter now attached to ttyUSB1
 	[ 5806.664577] usb 1-1.5: GSM modem (1-port) converter now attached to ttyUSB2

ou 

```lsusb | grep -i Huawei```

exemple de résultat obtenu : 

  Bus 001 Device 009: ID 12d1:1001 Huawei Technologies Co., Ltd. E169/E620/E800 HSDPA Modem
 
### Mettre à jour le système 
```sudo apt-get update```
```sudo apt-get upgrade```

### Installez Gammu 
```sudo apt-get install gammu``` 
### Détectez la configuration de gammu 
```gammu-detect``` 

Récupérez la configuration affichée à l’écran pour la mettre dans le fichier /etc/gammurc  

exemple de contenu du fichier : 

```[gammu]
device = /dev/ttyUSB0
connection = at19200
name = Phone on USB serial port ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ HUAWEI_Mobile
synchronizetime = yes
gammucoding = utf8
 
[gammu1]
device = /dev/ttyUSB1
connection = at19200
name = Phone on USB serial port ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ HUAWEI_Mobile
synchronizetime = yes
gammucoding = utf8
 
[gammu2]
device = /dev/ttyUSB2
connection = at19200
name = Phone on USB serial port ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ HUAWEI_Mobile
synchronizetime = yes
gammucoding = utf8```

### Vérifiez les caractéristiques de la clé 3g 
```gammu --identify```

exemple de résultat obtenu :

          Périphérique : /dev/ttyUSB0
          Fabricant : Huawei
          Modèle : E169 (E169)
          Firmware : 11.314.13.51.156
          IMEI : 352835031664512

En cas d’erreur le message suivant apparaît : Carte SIM non accessible. Dans ce cas soit : 
- La carte SIM n’est pas compatible avec le modèle de clé GMS 
- La clé GSM n’est pas compatible avec Gammu. Dans ce cas, se référer à la liste des clé compatibles. 
Si un code PIN est activé 
```gammu getsecuritystatus```
      Waiting for PIN.
```gammu entersecuritycode PIN 1234```
```gammu getsecuritystatus```
      Nothing to enter.

### Envoyez un SMS 
```gammu sendsms TEXT 06xxxxxxxx -text "Test 1"```
ou
```echo "Tapez ici votre SMS" | gammu --sendsms TEXT 06XXXXXX```
En réponse, voici ce que la console affiche : 
If you want break, press Ctrl+C...
Sending SMS 1/1....waiting for network answer..OK, message reference=1

## EXPLICATION DE LA COMMUNICATION BLUETOOTH POUR LE TRANSFERT DES DONNEES
L’utilisateur doit pousser le joystick de la Sense HAT vers le haut afin d’ouvrir une connexion bluetooth côté Raspberry Pi. 
En effet, cet action déclenche le script bash “walker.sh” qui ouvre le port rfcomm hci0 en et lance en parallèle un script python “read.py” : 
Ligne de commande afin d’ouvrir le port (dans le fichier walker.sh) : sudo rfcomm listen hci0
Le script “read.py” attend une connexion bluetooth côté application mobile.
exemple avec l’envoi des contacts d’urgence : 
Une fois les contacts d’urgence définis dans l’application mobile (Paramètres → Conacts d’urgence), l’utilisateur clique sur le bouton “Envoyer au bracelet”. Ceci permet de créer une connexion bluetooth avec le bracelet et d’envoyer les contacts d’urgence. 
Le bracelet détecte la réception d’un message sur le port rfcomm et agit en conséquence.
Le type de message est reçu est défini grâce à un ID : 
ID “1” pour la l’envoi de randonnée 
ID “2” pour l’envoi des numéros de contacts d’urgence 
ID “3” pour l’envoi d’une demande de déconnexion. 
 Dans le cas d’une réception de numéros d’urgence [ID 2], les numéros de téléphones sont enregistrés dans le fichier “numeros.txt”.  Lors du transfert de données, la matrice de LED affiche l’icône DU bluetooth. 
Il est important de noter que l’application mobile envoie automatiquement 2 messages : le premier contenant les information, puis un message de demande déconnexion. C’est pourquoi, une fois les numéros  écrits dans le fichier, le port rfcomm toujours en écoute reçoit une demande de déconnexion et la connexion bluetooth se ferme automatiquement (fermeture du port côté bracelet)
Ce fonctionnement est identique pour l’envoi de l’ID de randonnée. Dans ce cas, l’ID envoyée est enregistrée dans le fichier “idrando.txt” 


## GESTION DU BLUETOOTH SUR L’APPLICATION CORDOVA
Pour gérer le Bluetooth depuis l’application Cordova de Geotrek Mobile, il faut ajouter le plugin suivant:
cordova plugin add cordova-plugin-bluetooth-serial
[Référence](https://github.com/don/BluetoothSerial/tree/master/examples/SimpleSerial)

Ensuite, configurez l’adresse MAC de votre bracelet. 
Vous devez modifier la variable “macAddress” des fonction “openPort” et “closePort”  dans les fichiers:
“www/trek/controllers.js” ;
“www/scripts/user_settings/controllers.js “ en entrant l'adresse MAC de votre appareil à coupler. 

Afin que les fonctionnalités bluetooth s’effectuent, il faut obligatoirement que votre appareil soit déjà appairé à la RPI3.

## ENVOI DE SMS DEPUIS L’APPLICATION CORDOVA 
Pour envoyer des SMS depuis l’application Cordova de Geotrek Mobile, il faut ajouter le plugin suivant:
cordova plugin add cordova-sms-plugin
[Référence](https://github.com/cordova-sms/cordova-sms-plugin)

## Génération et déploiement du code sur votre appareil
Si ce n’est pas encore fait, ajoutez les plateformes android et/ou ios
cordova platform add android
cordova platform add ios

Ensuite déployez le code avec la commande:
cordova run 

## PROBLEME/SOLUTION

BIND -> address already in use  -> sudo rfcomm release 0 


## GUIDE UTILISATEUR

### Définition et envoi des contacts d’urgence
1)	L’utilisateur clique sur le bouton « Paramètres »
2)	L’utilisateur définit ses contacts d’urgence dans la rubrique « Contacts d’urgence » (ajouts/suppressions)
3)	L’utilisateur pousse le joystick du bracelet connecté vers le haut afin d’ouvrir une connexion bluetooth bracelet/téléphone 
4)	L’utilisateur clique sur le bouton « Envoyer au bracelet » de la rubrique « Contacts d’urgence » de l’application mobile afin de les transférer au bracelet connecté.
5)	Une icône « bluetooth » bleue et blanche apparaît sur la matrice de LED du bracelet connecté pour informer l’utilisateur qu’une connexion et un envoi sont en cours. 
6)	La matrice de LED s’éteint pour informer l’utilisateur de la fin du transfert et de la fermeture de la connexion.

### Sélection, envoi de l’itinéraire de la randonnée et lancement de la randonnée

1)	L’utilisateur retourne sur la page d’accueil pour choisir un itinéraire de randonnée parmi la liste proposée et clique sur la randonnée souhaitée.
2)	L’utilisateur pousse une nouvelle fois le joystick du bracelet connecté vers le haut afin de relancer une connexion pour envoyer l’identifiant de l’itinéraire concerné.
3)	L’utilisateur clique sur le bouton « Commencer de la randonnée »
4)	Une icône « bluetooth » bleue et blanche apparaît sur la matrice de LED du bracelet connecté pour informer l’utilisateur qu’une connexion et un envoi sont en cours. 
5)	La matrice de LED s’éteint pour informer l’utilisateur de la fin du transfert et de la fermeture de la connexion.
6)	La randonnée commence.

### Affichage des données environnantes 
1)	L’utilisateur clique sur le bouton du milieu du joystick pour afficher la température (T en degrés), la pression (P en %) et l’humidité (H en milliBar)

### Envoi de SMS
Envoi de SMS d’urgence aux contacts d’urgence (via l’application mobile):
1)	L’utilisateur clique sur le bouton « Envoyer SOS » dans la rubrique « Contacts d’urgence » des « Paramètres »

Envoi de SMS d’arrivée aux contacts d’urgence (via l’application mobile):
1)	L’utilisateur clique sur le bouton « Envoyer arrivée » dans la rubrique « Contacts d’urgence » des « Paramètres »

### Annuler l’envoi de SMS d’urgence depuis le bracelet connecté à la suite d’une détection de chute
1)	A la suite d’une détection de chute, la matrice de LED affiche un point d’exclamation blanc sur un fond rouge pour informer l’utilisateur qu’un compteur de 30 secondes a été déclenché avant l’envoi d’un SMS d’urgence aux contacts d’urgence. 
2)	L’utilisateur pousse le bouton gauche pour annuler l’envoi de SMS dans le délai de 30 secondes.
3)	L’envoi de SMS est annulé.

### Fermeture forcée de la connexion bluetooth 
1)	En cas d’erreur lors de la déconnexion : la déconnexion ne s’effectue pas côté bracelet connecté, l’icone affichant le symbole « bluetooth » restera affiché sur la matrice de LED. Pour forcer la déconnexion, il suffit de pousser longuement le joystick du bracelet connecté vers le bas. 
2)	La matrice de LED devrait s’éteindre pour montrer que la connexion est désormais fermée.

### Fermer une randonnée
1)	Si l’utilisateur souhaite arrêter une randonnée en cours il lui suffit de pousser longuement le joystick vers la droite. 
3)	La matrice de LED devrait s’éteindre pour montrer que le guidage/géolocalisation ont été stoppés. 

### Téléchargement des itinéraires
1)	Si de nouveaux itinéraires ont été mis en ligne sur le site « walkerpfe-rando.ovh », l’utilisateur peut mettre à jour son bracelet en récupérant les coordonnées des itinéraires.
2)	L’utilisateur pousse le joystick du bracelet connecté vers le bas.
3)	Les données se téléchargent depuis le site.


