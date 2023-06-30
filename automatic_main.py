# Importation des bibliothèques
import cv2
import numpy as np
import trim
# from commande import commande, commande_2, commande_test
from time import perf_counter, sleep
from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port
import struct
# from create_and_train_model import create_model
import tensorflow as tf

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

# Définition de la vitesse des roues pour le contrôle manuel (entre 0 et 100 points)
CMD = 100

# Connexion avec l'Arduino
serial_file = open_serial_port(baudrate=115200, timeout=1)
is_connected = False
b = 0

while not is_connected:
    b = b + 1
    write_order(serial_file, Order.HELLO)
    bytes_array = bytearray(serial_file.read(1))
    if not bytes_array:
        sleep(2)
        continue
    byte = bytes_array[0]
    if byte in [Order.HELLO.value, Order.ALREADY_CONNECTED.value]:
        is_connected = True
print(b)

c = 1
while (c != b''):
    c = serial_file.read(1)
    print(c)


# Définition de certains paramètres
theta_max = 50 * np.pi / 180  # Angle du cône de la camera
hauteur_cam = 0.108  # Auteur de la camera par rapport au sol (en cm)
delta = 5 * np.pi / 180  # Angle mort en-dessous de la camera


# Définition de paramètres pour le suivi de piste
v_consigne = 126
sample_time = 0.1
amplify_coef = 10
CMD_seuil = 126
t = perf_counter()


def get_speed():
    write_order(serial_file, Order.READENCODER)
    while True:
        try:
            vitesse = read_i16(serial_file)
            break
        except struct.error:
            pass
    return vitesse


write_order(serial_file, Order.ResetENCODER)

moving = False

INPUT_SHAPE = (32, 32, 3)
MODE = 'CLASSIFICATION'             # Set to 'CLASSIFICATION' or 'REGRESSION'

# model = create_model('Dense', num_classes=3, input_shape=INPUT_SHAPE)
# model.load_weights('model/Dense_512_64.h5')
model = tf.keras.models.load_model('models/Dense_512_64')


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
        print(get_speed())
        write_order(serial_file, Order.STOP)

    if k == keys["avant"]:
        moving = True

    if moving:

        if MODE == 'CLASSIFICATION':
            prediction = np.argmax(model.predict(
                cv2.resize(frm, INPUT_SHAPE)).numpy())

            if prediction == 0:                             # Move forward
                write_order(serial_file, Order.MOTOR)
                write_i8(serial_file, 0*CMD)
                write_i8(serial_file, 0*CMD)
                write_i8(serial_file, 0*CMD)
                write_i8(serial_file, 0*CMD)

            elif prediction == 1:                             # Move left
                write_order(serial_file, Order.MOTOR)
                write_i8(serial_file, -CMD)
                write_i8(serial_file, CMD)
                write_i8(serial_file, CMD)
                write_i8(serial_file, -CMD)

            elif prediction == 2:                             # Move right
                write_order(serial_file, Order.MOTOR)
                write_i8(serial_file, CMD)
                write_i8(serial_file, -CMD)
                write_i8(serial_file, -CMD)
                write_i8(serial_file, CMD)

        elif MODE == 'REGRESSION':

            prediction = model.predict(cv2.resize(frm, INPUT_SHAPE))[0].numpy()
            forward = prediction[0]
            left = prediction[1]
            right = prediction[2]

            if left > forward and left > right:
                write_order(serial_file, Order.MOTOR)
                write_i8(serial_file, -left * CMD)
                write_i8(serial_file, left * CMD)
                write_i8(serial_file, left * CMD)
                write_i8(serial_file, -left * CMD)

            elif right > forward and right > left:
                write_order(serial_file, Order.MOTOR)
                write_i8(serial_file, right * CMD)
                write_i8(serial_file, -right * CMD)
                write_i8(serial_file, -right * CMD)
                write_i8(serial_file, right * CMD)

        else:
            raise ValueError(f'Unknown mode : {MODE}')

# Dans tous les cas, arrêter le robot par sécurité
write_order(serial_file, Order.STOP)

# Fermer les fenêtres d'affichage des images et libérer la caméra
cv2.destroyAllWindows()
cap.release()
