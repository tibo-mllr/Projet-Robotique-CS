# Importation des bibliothèques
import cv2
import numpy as np
import trim
from tflite_runtime.interpreter import Interpreter
from robust_serial import write_order, Order, write_i8, write_i16, read_i16, read_i32, read_i8
from robust_serial.utils import open_serial_port
from PID import PID
from commande import commande, commande_2, commande_test
from time import perf_counter, sleep


def main(interpreter):
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
            write_order(serial_file, Order.STOP)
            break

        if k == keys["stop"]:
            write_order(serial_file, Order.STOP)
            moving = False

        if k == keys["avant"]:
            moving = True

        if moving:

            input = np.array([cv2.resize(frm, INPUT_SHAPE[:2])])/128 - 1

            interpreter.allocate_tensors()

            # Get input and output tensors.
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            tensor_index = input_details[0]['index']
            input_tensor = interpreter.tensor(tensor_index)()
            input_tensor[:, :] = input

            interpreter.set_tensor(input_details[0]['index'], input_tensor)
            interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            prediction = interpreter.get_tensor(output_details[0]['index'])[0]

            forward = prediction[0]
            left = prediction[1]
            right = prediction[2]

            # grads = gradients(model, input_tensor)

            if MODE == 'CLASSIFICATION':

                pred = {0: "devant", 1: "gauche", 2: "droite"}[
                    np.argmax(prediction)]

                print(prediction*100, pred)

                if pred == "devant":
                    write_order(serial_file, Order.STOP)

                elif pred == "gauche":
                    write_order(serial_file, Order.MOTOR)
                    write_i8(serial_file, -cmd)
                    write_i8(serial_file, cmd)
                    write_i8(serial_file, -cmd)
                    write_i8(serial_file, cmd)

                elif pred == "droite":
                    write_order(serial_file, Order.MOTOR)
                    write_i8(serial_file, cmd)
                    write_i8(serial_file, -cmd)
                    write_i8(serial_file, cmd)
                    write_i8(serial_file, -cmd)

            elif MODE == 'REGRESSION':

                if left > forward and left > right:
                    print(left*cmd)

                elif right > forward and right > left:
                    print(right*cmd)

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

    keys = keys4

    # Définition de la vitesse des roues pour le contrôle manuel (entre 0 et 100 points)
    cmd = 60

    # Connexion à l'Arduino
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

    moving = True

    INPUT_SHAPE = (32, 32, 3)
    MODE = 'CLASSIFICATION'             # Set to 'CLASSIFICATION' or 'REGRESSION'

    # model = tf.keras.models.load_model('models/Dense_512_64')

    interpreter = Interpreter(model_path="models/Dense_512_64.tflite")

    main(interpreter)

    cv2.destroyAllWindows()
    cap.release()
