# Importation des bibliothèques
import numpy as np


def commande(t, v_consgine, derive_dist, derive_angle, pid, preference_coef=1):
    """ Retourne la commande de vitesses pour les moteurs gauche et droite """

    v = (1-np.exp(-2*t))*v_consgine
    # alpha = derive_angle - atan(derive_dist)
    dv = pid(derive_angle)
    return v+dv, v-dv


def commande_2(t, v_consigne, D, derive_dist, alpha, derive_angle, pid):
    """Retourne la commande de vitesses pour les moteurs gauche et droite

        Argument
        --------
        t : ? (float)
        v_consigne : Vitesse nominale (int)
        D : Distance entre la piste et le robot, sur son axe (float)
        derive_dist : Distance la plus petite entre le robot et la piste (float)
        alpha : Angle entre le robot et le point le plus proche de la piste (float, en rd)
        derive_angle : Angle de dérive (float, en rd)
        pid : Correcteur PID (function)

        Sortie
        ------
        Tuple (float, float)
    """

    # On prend en compte la courbe pour ne pas le faire avancer à pleine vitesse
    # S'il doit faire un virage de 90° par exemple
    v = (1-np.exp(-2*t)) * min(v_consigne, v_consigne *
                               (np.cos(derive_angle)+derive_dist/0, 1))
    # Ya sûrement un coeff à mettre devant encore, ou une addition, faudra voir quoi

    dv = pid(derive_angle)
    print("Avec l'angle de dérive :", pid(
        derive_angle), "Avec alpha :", pid(alpha))
    # On normalise par rapport à la vitesse qu'on donne
    dv *= v / ((1-np.exp(-2*t)) * v_consigne)

    return v+dv, v-dv


def commande_test(t, v_consigne, D, derive_dist, alpha, derive_angle, pid):
    """Retourne la commande de vitesses pour les moteurs gauche et droite

        Argument
        --------
        t : ? (float)
        v_consigne : Vitesse nominale (int)
        D : Distance entre la piste et le robot, sur son axe (float)
        derive_dist : Distance la plus petite entre le robot et la piste (float)
        alpha : Angle entre le robot et le point le plus proche de la piste (float, en rd)
        derive_angle : Angle de dérive (float, en rd)
        pid : Correcteur PID (function)

        Sortie
        ------
        Tuple (float, float)
    """

    # On prend en compte la courbe pour ne pas le faire avancer à pleine vitesse
    # S'il doit faire un virage de 90° par exemple
    v = (1-np.exp(-2*t)) * min(v_consigne, v_consigne *
                               (np.cos(derive_angle)+derive_dist/0, 1))
    # Ya sûrement un coeff à mettre devant encore, ou une addition, faudra voir quoi

    dv = derive_angle
    print("Avec l'angle de dérive :", pid(
        derive_angle), "Avec alpha :", pid(alpha))
    # On normalise par rapport à la vitesse qu'on donne
    dv *= v / ((1-np.exp(-2*t)) * v_consigne)

    return v+dv, v-dv
