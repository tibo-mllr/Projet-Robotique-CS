# Importation des bibliothèques
import cv2
import numpy as np
import trim
from time import perf_counter, sleep

# Récupération de la caméra
cap = trim.getCamera()

# Initialisation du mode de fonctionnement
mvt_modes = ["Translation", "Rotation"]
mvt = 0

# Initialisation des indices des touches

# Sur Rapsberry, pavé numérique non activé, majuscules non activées
keys1 = {"mode": 109, "quitter": 113, "stop": 115, "gauche": 65430,
         "avant": 65431, "droite": 65432, "arriere": 65433, "mouvement": 116, "AvG": 65429, "AvD": 65434, "ArG": 65436, "ArD": 65435}
# Sur Raspberry, pavé numérique activé, majuscules non activées
keys2 = {"mode": 1048685, "quitter": 1048689, "stop": 1114037, "gauche": 1114036,
         "avant": 1114040, "droite": 1114038, "arriere": 1114034, "mouvement": 1048692, "AvG": 1114039, "AvD": 1114041, "ArG": 1114033, "ArD": 1114035}
# Sur PC sans pavé numérique, majuscules non activées (pour des tests par exemple)
# Ne pas oublier de commenter les lignes où il y a des clés qui n'aparaissent pas dans ce dictionnaire
keys3 = {"mode": 109, "quitter": 113, "stop": 115, "gauche": 2424832,
         "avant": 2490368, "droite": 2555904, "arriere": 2621440, "mouvement": 116}
# Sur PC avec clavier branché, pavé numérique activé, majuscules désactivées (pour enregistrer le dataset par exemple)
# Ne pas oublier de commenter les lignes où il y a des clés qui n'aparaissent pas dans ce dictionnaire
keys4 = {"mode": 109, "quitter": 113, "stop": 53,
         "gauche": 52, "avant": 56, "droite": 54, "mouvement": 116}

keys = keys4


# Pour récupérer le dataset. Labels : 0 : avant, 1 : gauche, 2 : droite, 3 : AvG, 4 : AvD
images = []
labels = []
current_label = None
i = 0


# Boucle d'exécution principale
while True:
    # Lecture de l'image de la caméra
    frm = trim.getFrame(cap)

    # Affichage de l'image
    cv2.imshow("robo", frm)

    # Récupération de la touche sur laquelle l'utilisateur a appuyé
    k = cv2.waitKeyEx(1)

    if k == keys["mouvement"]:
        mvt = 1 - mvt

    if k == keys["quitter"]:
        # Arrêt de la boucle d'exécution
        break

    # En contrôle manuel
    if mvt_modes[mvt] == "Rotation":
        if k == keys["stop"]:
            np.save(f'images_{i}', images)
            np.save(f'labels_{i}', labels)
            print("Stop")
            images = []
            labels = []
            current_label = None

        elif k == keys["avant"]:
            print("Avant")
            current_label = 0

        elif k == keys["gauche"]:
            print("Gauche")
            current_label = 1

        elif k == keys["droite"]:
            print("Droite")
            current_label = 2

    if current_label is not None and i % 5 == 0:
        images.append(frm)
        labels.append(current_label)

    i += 1

# Fermer les fenêtres d'affichage des images et libérer la caméra
cv2.destroyAllWindows()
cap.release()
