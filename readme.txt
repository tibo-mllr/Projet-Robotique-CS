# Projet P19 Robotique 2021/22 : Conception d'une base robotique mobile rapide

## Constitution de l'équipe
* AMMAR Mariem
* ANTOINE Matthieu
* BEN SELMA Hadil
* CHÊNE Samuel
* CONSTANT Evrard
* EL HELOU Jason
* GOULLET DE RUGY Bastien
* LAMARQUE Paul-Arno
* MULLER Thibault
* VILLAIN Ronan


## Commandes du robot :

* Attention, cela est pris en compte uniquement lorsque la fenêtre de vidéo est sélectionnée (elle l'est par défaut lors de son ouverture au lancement du programme)
* Pavé numérique 8 (flèche vers le haut) : avancer
* Pavé numérique 2 (flèche vers le bas) : reculer
* Pavé numérique 4 (flèche vers la gauche) : aller/tourner à gauche (selon le mode de mouvement)
* Pavé numérique 6 (flèche vers la droite) : aller/tourner à droite (selon le mode de mouvement)
* Pavé numérique 7 (flèche vers le haut gauche) : avancer en diagonale vers la gauche
* Pavé numérique 9 : avancer en diagonale vers la droite
* Pavé numérique 1 : reculer en diagonale vers la gauche
* Pavé numérique 3 : reculer en diagonale vers la droite
* Pavé numérique 5 : arrêter le robot
* Touche s : arrêter le robot (sur PC sans pavé numérique, et avec le bon dictionnaire keys sélectionné)
* Touche q : arrêter le programme
* Touche t : changement le mode de mouvement : translation(par défaut) / rotation
* touche m : changer le mode de commande : manuel(par défaut) / autonome

### Pour faire fonctionner le robot en mode manuel, lancer le ficher "main.py"
### Pour faire fonctionner l'IA, lancer le fichier "rotation_test.py"


## Liste des dossiers et fichiers :

* ./Documentation/ :
	* Documents utiles

* ./models/ :
	* Dossier contenant les modèle d'IA
		* *.h5 : fichiers TF
		* *.tflite : fichiers TF Lite pour faire tourner sur Raspberry
		* CNN_* : dernier modèle entraîné

* ./robust_serial/ :
	* Programmes Python pour communiquer avec l'Arduino

* ./test_quadri/ :
	* Programmes Arduino

* ./automatic_main.py :
	* Programme pour faire fonctionner l'IA entière (non fonctionnel car l'IA n'est entraînée que pour la rotation pour l'instant)

* ./commande.py :
    * Programme pour générer la commande des moteurs.

* ./create_and_train_model.py :
	* Programme pour créer et entraîner un modèle à partir d'une base de donnée d'images et de labels

* ./get_dataset.py :
	* Programme pour enregistrer le dataset (mieux à faire sur PC car enregistre plus vite, et pas besoin de transférer ensuite)

* ./get_gradients.py :
	* Programme test pour calculer les gradients des images traîtées par l'IA pour vérifier son apprentissage

* ./main.py :
    * Programme à lancer pour faire fonctionner le robot en mode manuel, ou en mode autonome mais avec l'ancien code

* ./PID.py :
	* Programme pour le correcteur PID.

* ./reformat_images.py :
	* Programme pour reformater les images que l'IA va traîter, pour ne pas qu'elles soient trop lourdes

* ./rotation_test.py :
	* Programme pour faire fonctionner l'IA sur PC : la console est simplement mise à jour avec la prédiction de l'IA

* ./rotation.py :
	* Programme pour faire fonctionner l'IA sur Raspberry, en mode rotation

* ./shuffle_and_split_data.py :
	* Programme pour sélectionner des images aléatoire du dataset pour entraîner et tester l'IA

* ./stats_dataset.py :
	* Programme pour recevoir les stats des tests de l'IA

* ./test.py :
	* Programme pour faire des tests unitaires, à changer à chaque fois qu'on veut tester un petit truc (actuellement utilisé pour voir la résolution des images)

* ./tests.py :
	* Programme pour tester l'IA

* ./trim.py :
	* Programme pour le traitement d'images.
