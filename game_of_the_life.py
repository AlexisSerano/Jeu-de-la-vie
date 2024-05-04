import numpy as np
import time
import msvcrt
import os

class Cellule:

    def __init__(self,etat):
        #on initialise l'objet cellule qui prend des valeurs booléennes associées a son statut : vivant ou morte
        self.etat = etat



class Grille:


    def __init__(self,taille):
        #on initialise une grille numpy de taille n en fonction du choix de l'utilisateur
        self.taille = taille
        self.grille = np.zeros((taille , taille) , dtype=object)
        for i in range(taille):
            for j in range(taille):
                #pour chaque element de la grille on y place une instance de la classe Cellule avec des Cellules mortes
                self.grille[i,j] = Cellule(False)

    def add_cellule(self):
        try:
            #Ajout d'une cellule vivante dans la grille
            print("Donner la colonne")
            colonne = int(input())
            if colonne > len(self.grille):
                print("la collonne n'est pas assez grande")
                return
            print("Donner la ligne")
            ligne = int(input())
            if colonne > len(self.grille):
                print("la collonne n'est pas assez grande")
                return
            self.grille[ligne,colonne].etat = True
            print("Cellule ajouter , en ajouter une autre ?(Y,N)")
            choise = input()
            if choise.lower() == "y":
                return self.add_cellule()
            else:
                return
        except ValueError:
            print("Une erreur est survenue.")
            return
        
    def kill_cellule(self):
        #Tuer une cellule vivante dans la grille
        try:
            print("Donner la colonne")
            colonne = int(input())
            if colonne > len(self.grille):
                print("la collonne n'est pas assez grande")
                return
            print("Donner la ligne")
            ligne = int(input())
            if colonne > len(self.grille):
                print("la collonne n'est pas assez grande")
                return
            self.grille[colonne,ligne].etat = False
            print("Cellule Tuer , en Tuer une autre ?(Y,N)")
            choise = input()
            if choise.lower() == "y":
                return self.kill_cellule()
            else:
                return
        except ValueError:
            print("Une erreur est survenue.")
            return

    def actualiser_etat_cellule(self):
        nouvelle_grille = np.zeros((self.taille, self.taille), dtype=object)

        # Parcourir chaque cellule de la grille actuelle
        for i in range(self.taille):
            for j in range(self.taille):
                cellule = self.grille[i, j]
                nb_voisins_vivants = 0

                # compter le nombre de voisins vivants
                #-1 est la cellule avant , 0 la cellule actuelle et 1 la cellule prochaine sur l'axe des abcisses
                for di in [-1, 0, 1]:
                    #-1 est la cellule avant , 0 la cellule actuelle et 1 la cellule prochaine sur l'axe des ordonnées
                    for dj in [-1, 0, 1]:
                        #si nous nous trouvont sur la cellule actuelle l'ignorer
                        if di == 0 and dj == 0:
                            continue
                        #ni et nj sont les coordonnées de la cellules voisine a la cellule actuelle
                        ni, nj = i + di, j + dj
                        #si la cellule voisine est dans la grille et vivante , alors c'est une voisine vivante
                        if 0 <= ni < self.taille and 0 <= nj < self.taille:
                            if self.grille[ni, nj].etat:
                                nb_voisins_vivants += 1

                # appliquer les règles du jeu de la vie
                if cellule.etat:
                    if nb_voisins_vivants == 2 or nb_voisins_vivants == 3:
                        nouvelle_grille[i, j] = Cellule(True)  # reste vivante
                    else:
                        nouvelle_grille[i, j] = Cellule(False)  # meurt
                else:  # cellule morte
                    if nb_voisins_vivants == 3:
                        nouvelle_grille[i, j] = Cellule(True)  # nait
                    else:
                        nouvelle_grille[i, j] = Cellule(False)  # reste morte
        return nouvelle_grille

    def observer(self):
        #choix du temps entre les génerations
        try:
            print("Combien de temps (en seconde) entre chaque genérations ?")
            n = float(input())
        except ValueError:
            print("Erreur d'entrée")
            return
        #afficher "." si la cellule est morte et "*" si elle est vivante
        while True:
            print("Quitter : Appuyez sur 'q' pour revenir au menu principal.")
            c = [k for k in range(self.taille)]
            
            print(" "*9 , *c , sep= " ")
            for i in range(self.taille):
                if i < 10:
                    print(f"ligne :  {i}" , end= " ")
                else:
                    print(f"ligne : {i}" , end= " ") 
                for j in range(self.taille):                    
                    if self.grille[i, j].etat:
                        print("*", end=" ")
                    else:
                        print(".", end=" ")
                print()

            # vérifiez si une touche a été pressée
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'q' or key == b'Q':
                    break

            self.grille = self.actualiser_etat_cellule()
            #attendre n secondes pour nettoyer le terminal et afficher la nouvelle grille
            time.sleep(n)
            os.system('cls')

    def reset_game(self):
        #redémarer le jeu
        start()

    def interface(self):
        while True:
            try:
                print("Bienvenue dans le jeu de la vie. Que voulez-vous faire ?")
                print("1 - Ajouter des cellules vivantes")
                print("2 - Tuer des cellules")
                print("3 - Observer le jeu de la vie")
                print("4 - Reset le jeu")
                print("5 - Quitter")

                choice = int(input("Choix : "))

                if choice == 1:
                    self.add_cellule()
                elif choice == 2:
                    self.kill_cellule()
                elif choice == 3:
                    self.observer()
                elif choice == 4:
                    self.reset_game()
                elif choice == 5:
                    return
                else:
                    print("Choix invalide. Veuillez choisir une option valide.")

            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier pour choisir une option.")


#premiere étape du jeu , le choix de la taille
def start():
    try:
        print("Choissez la taille de la grille pour votre jeu")
        choise = int(input())
        grille = Grille(choise)
        grille.interface()
    except ValueError:
        print("Entrée invalide.")
start()