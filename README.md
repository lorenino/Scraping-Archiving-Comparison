Projet d'archivage Web
Ce projet est un script Python conçu pour archiver le contenu HTML de pages Web spécifiées dans un fichier Excel, comparer les versions archivées pour détecter les changements et envoyer des notifications par e-mail en cas de différences détectées.

Contenu du Projet
main.py: Ce fichier contient le script principal qui orchestre le processus d'archivage, de comparaison et d'envoi d'e-mails.
email_config.py: Ce fichier contient la configuration pour l'envoi d'e-mails, y compris les détails du serveur SMTP et les informations d'identification.
archivage.py: Un fichier supplémentaire où les fonctions spécifiques à l'archivage peuvent être définies et appelées depuis le script principal, si nécessaire.
crawl.log: Ce fichier contient les logs générés lors de l'exécution du script.
Configuration
Avant d'utiliser ce script, assurez-vous d'installer toutes les dépendances Python répertoriées dans le fichier requirements.txt.

Pour configurer l'envoi d'e-mails, ouvrez le fichier email_config.py et modifiez les valeurs suivantes :

SENDER_EMAIL: Adresse e-mail de l'expéditeur.
RECEIVER_EMAIL: Adresse e-mail du destinataire.
PASSWORD: Mot de passe de l'expéditeur pour le serveur SMTP.
SMTP_SERVER: Adresse du serveur SMTP.
SMTP_PORT: Port du serveur SMTP.
Utilisation
Assurez-vous d'avoir installé Python sur votre système.
Installez les dépendances en exécutant pip install -r requirements.txt.
Placez votre fichier Excel contenant les URLs à archiver dans le même répertoire que main.py.
Exécutez le script en utilisant la commande suivante dans votre terminal :
bash
Copy code
python main.py nom_du_fichier.xlsx
Assurez-vous de remplacer nom_du_fichier.xlsx par le nom de votre fichier Excel contenant les URLs.

Logs
Toutes les opérations effectuées par le script seront enregistrées dans le fichier crawl.log, y compris les erreurs rencontrées lors de l'exécution.

