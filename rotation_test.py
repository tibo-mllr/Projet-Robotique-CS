# Importation des bibliothèques
import cv2
import numpy as np
import trim
import tensorflow as tf
from create_and_train_model import create_model


def main(model):
    global moving
    # Boucle d'exécution principale
    while True:
        # Lecture de l'image de la caméra
        frm = trim.getFrame(cap)

        # Affichage de l'image
        cv2.imshow("robo", frm)

        # Récupération de la touche sur laquelle l'utilisateur a appuyé
        k = cv2.waitKeyEx(1)

        if k == keys["quitter"]:
            # Arrêt de la boucle d'exécution
            break

        if k == keys["stop"]:
            moving = False

        if k == keys["avant"]:
            moving = True

        if moving:

            input = np.array([cv2.resize(frm, INPUT_SHAPE[:2])])/128 - 1

            prediction = model(input)[0]

            forward = prediction[0]
            left = prediction[1]
            right = prediction[2]

            # grads = gradients(model, input_tensor)

            if MODE == 'CLASSIFICATION':

                pred = {0: "devant", 1: "gauche", 2: "droite"}[
                    np.argmax(prediction)]

                if pred == "devant":
                    print("devant")

                elif pred == "gauche":
                    print("à gauche")

                elif pred == "droite":
                    print("à droite")

            elif MODE == 'REGRESSION':

                if left > forward and left > right:
                    print(left)

                elif right > forward and right > left:
                    print(right)

            else:
                raise ValueError(f'Unknown mode : {MODE}')


if __name__ == '__main__':

    # Récupération de la caméra
    cap = trim.getCamera()

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

    keys = keys3

    moving = True

    INPUT_SHAPE = (32, 32, 3)
    MODE = 'CLASSIFICATION'             # Set to 'CLASSIFICATION' or 'REGRESSION'

    model = create_model(model_type='CNN_3_layers',
                         num_classes=3, input_shape=(32, 32, 3))
    model.load_weights('models/CNN_32_64_128_128.h5')

    main(model)

    cv2.destroyAllWindows()
    cap.release()
