# Importation des bibliothèques
import cv2


def getCamera():
    """ Se connecte à la caméra et la renvoie """

    return cv2.VideoCapture(0)


def getFrame(cap):
    """ Renvoie une image prise par la caméra """

    _, frm = cap.read()
    return frm


def resizeFrame(frm, w, h):
    """ Renvoie l'image redimensionnée """

    return cv2.resize(frm, (w, h))


def cropFrame(frm, x, y, w, h):
    """ Renvoie une région de l'image """

    return frm[y:y+h, x:x+w]


def grayscale(frm):
    """ Renvoie l'image en niveaux de gris """

    return cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)


def blackAndWhite(frm, thresh):
    """ Applique un filtre de seuil à l'image et la renvoie """

    _, temp = cv2.threshold(frm, thresh, 255, cv2.THRESH_BINARY)
    return temp


def getContour(frm):
    """ Retourne le contour de plus grande aire détécté sur l'image """

    _, contours, hierarchy = cv2.findContours(
        frm, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
        cnt = max(contours, key=cv2.contourArea)
    except:
        cnt = "STOP"
    return cnt


def getLine(cnt):
    """ Retourne la ligne droite qui interpole le mieux le contour """

    line = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
    return line
