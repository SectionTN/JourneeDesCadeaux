from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from pickle import load, dump
from numpy import array


def premier(x):
    result = True
    for i in range(2, x // 2 + 1):
        if x % i == 0:
            result = False
    return result


def sum_div(n):
    div_sum = 1

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            div_sum += i
            if i != n // i:
                div_sum += n // i

    return div_sum


def est_amicale(a, b):
    sum_a_div = sum_div(a)
    sum_b_div = sum_div(b)

    return sum_a_div == b and sum_b_div == a


def remplir():
    nom = window.nom.text()
    prenom = window.prenom.text()
    telephone = window.telephone.text()
    clientFidele = window.clientFidele.isChecked()
    if nom.isdigit() is True or len(nom) == 0:
        QMessageBox.critical(window, "Votre nom est incorrecte", "corriger là", QMessageBox.Ok)
    elif prenom.isdigit() is True or len(prenom) == 0:
        QMessageBox.critical(window, "Votre prenom est incorrecte", "corriger là", QMessageBox.Ok)
    elif telephone.isdigit() is False or len(telephone) != 8:
        QMessageBox.critical(window, "Votre telephone est incorrecte", "corriger là", QMessageBox.Ok)
    else:
        personnel = dict(nom=str, prenom=str, telephone=str, clientFidele=bool)
        personnel['nom'] = nom
        personnel['prenom'] = prenom
        personnel['telephone'] = telephone
        personnel['clientFidele'] = clientFidele
        file = open("client.dat", "ab")
        dump(personnel, file)
        file.close()


def afficher_tous_clinets():
    T = array([dict()] * 10)
    file = open("client.dat", "rb")
    estFinFichier = False
    i = 0
    while not estFinFichier:
        try:
            T[i] = load(file)
            i += 1
        except:
            estFinFichier = True
            file.close()

    N = i + 1
    window.table.setRowCount(N - 1)
    window.table.setColumnCount(4)
    window.table.setHorizontalHeaderLabels((["Nom", "Prenom", "Telephone", "Fidele"]))
    for i in range(N):
        client = T[i]
        nom = ""
        if "nom" in client:
            nom = client["nom"]
        prenom = ""
        if "prenom" in client:
            prenom = client["prenom"]
        telephone = ""
        if "telephone" in client:
            telephone = client["telephone"]
        clientFidele = ""
        if "clientFidele" in client:
            if client['clientFidele'] is True:
                clientFidele = "Oui"
            else:
                clientFidele = "Non"
        window.table.setItem(i, 0, QTableWidgetItem(nom))
        window.table.setItem(i, 1, QTableWidgetItem(prenom))
        window.table.setItem(i, 2, QTableWidgetItem(telephone))
        window.table.setItem(i, 3, QTableWidgetItem(clientFidele))


def afficher_clients_gagnants():
    T = array([dict()] * 10)
    G = array([dict()] * 10)
    file = open("client.dat", "rb")
    estFinFichier = False
    i = 0
    while not estFinFichier:
        try:
            T[i] = load(file)
            i += 1
        except:
            estFinFichier = True
            file.close()
    N = i + 1
    j = 0
    for i in range(N):
        client = T[i]
        if "nom" in client and "prenom" in client and "telephone" in client and "clientFidele" in client:
            G[i] = client
            j += 1
    taille = j + 1
    file_gagnants = open("gagnats.txt", "w")
    taille_fich = 0
    for i in range(taille):
        gagnants = G[i]
        if "nom" in gagnants and "prenom" in gagnants and "telephone" in gagnants and "clientFidele" in gagnants:
            nomg = gagnants["nom"]
            prenomg = gagnants["prenom"]
            tel = gagnants["telephone"]
            fidele = bool(gagnants['clientFidele'])
            gagne = True
            if premier(int(tel[0: 2])) is False:
                gagne = False
            elif est_amicale(int(tel[2: 5]), int(tel[5:8])) is False:
                gagne = False
            if gagne is True:
                file_gagnants.write(nomg + " " + prenomg + "\n")
                taille_fich += 1
            elif gagne is False and fidele is True:
                file_gagnants.write(nomg + " " + prenomg + "\n")
                taille_fich += 1
    file_gagnants.close()
    file_gagnants = open("gagnats.txt", "r")
    taille_fich = taille_fich + 1
    for i in range(taille_fich):
        window.list.addItem(str(file_gagnants.readline()))


print(est_amicale(284, 220))
print(premier(13))

application = QApplication([])
window = loadUi('gamesday.ui')
window.ajouter.clicked.connect(remplir)
window.tlclients.clicked.connect(afficher_tous_clinets)
window.lcgagnats.clicked.connect(afficher_clients_gagnants)
window.show()
application.exec_()
