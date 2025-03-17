
from distutils.command.install_egg_info import to_filename
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar, Treeview
from tkinter import ttk
from turtle import bgcolor

#creation fenetre principale 
ma_fenetre_principale = Tk()
ma_fenetre_principale.title("Organisation de mon repas")
ma_fenetre_principale["bg"]= "bisque1"
ma_fenetre_principale.geometry("480x380")


#creation de variables de départ
resultatpers_m = IntVar()
resultatpers_m.set(0)
resultatentree_m = IntVar()
resultatentree_m.set(0)
resultatplat_m = IntVar()
resultatplat_m.set(0)
resultatdessert_m = IntVar()
resultatdessert_m.set(0)
resultatboisson_m = IntVar()
resultatboisson_m.set(0)
liste_entree = []
liste_plat = []
liste_dessert = []
liste_boisson = []

def couleur_barre(p_total, p_souhaite, p_barreprog):
    style = ttk.Style()
    style.theme_use('alt')
    style.configure("red.Horizontal.TProgressbar", background="red")
    style.configure("yellow.Horizontal.TProgressbar", background="yellow")
    style.configure("orange.Horizontal.TProgressbar", background="orange")
    style.configure("green.Horizontal.TProgressbar", background="green")

    calcul = p_total/p_souhaite
    if calcul < 0.4 :
        p_barreprog.config(style = "red.Horizontal.TProgressbar")
    elif 0.4 <= calcul <0.7 :
        p_barreprog.config(style= "orange.Horizontal.TProgressbar")
    elif 0.7 <= calcul < 1 :
        p_barreprog.config(style= "yellow.Horizontal.TProgressbar")
    elif calcul == 1 :
        p_barreprog.config(style= "green.Horizontal.TProgressbar")

#========================================FENETRE [MODIFIER PARAMETRES DU SYSTEME]=================================================

#fonction du bouton [OK] appartenant à la fenetre "fenetre_modifier_param"
#permet de modifier les objectifs que cherche l'utilisateur dans les quantités
def modifier_param(p_champ_nbpers_m, p_champ_nbentree_m, p_champ_nbplat_m, p_champ_nbdessert_m, p_champ_nbboisson_m, p_fenetre):
    #mise à jour des valeurs du nombre d'entrée/plat/dessert/boisson en fonction du nombre souhaité

    #(1)détection des erreurs 
    b_erreur = FALSE 
    
    if p_champ_nbpers_m.isnumeric() == FALSE or p_champ_nbentree_m.isnumeric() == FALSE or p_champ_nbplat_m.isnumeric() == FALSE or p_champ_nbdessert_m.isnumeric() == FALSE or p_champ_nbboisson_m.isnumeric() == FALSE : #verification que l'utilisateur entre seulement des entiers
        messagebox.showerror(title = "Erreur insertion", message = "Vous devez saisir uniquement des entiers")
        b_erreur = TRUE

    if b_erreur == FALSE :
        if int(p_champ_nbentree_m) < iv_nb_entree_total.get() :
            messagebox.showerror(title = "Erreur modification", message = str(iv_nb_entree_total.get()) + " entrée(s) sont déjà enregistrée(s). Vous avez demandé " + str(p_champ_nbentree_m) + " entrées souhaitée(s). Veuillez saisir un entier supérieur ou égal à " + str(iv_nb_entree_total.get()) + ".")
            b_erreur = TRUE
        if int(p_champ_nbplat_m) < iv_nb_plat_total.get():
            messagebox.showerror(title = "Erreur modification", message = str(iv_nb_plat_total.get()) + " plat(s) sont déjà enregistré(s). Vous avez demandé " + str(p_champ_nbplat_m) + " plats souhaité(s). Veuillez saisir un entier supérieur ou égam à " + str(iv_nb_plat_total.get()) + ".")
            b_erreur = TRUE             
        if int(p_champ_nbdessert_m) < iv_nb_dessert_total.get():
            messagebox.showerror(title = "Erreur modification", message = str(iv_nb_dessert_total.get()) + " dessert(s) sont déjà enregistré(s). Vous avez demandé " + str(p_champ_nbdessert_m) + " plats souhaité(s). Veuillez saisir un entier supérieur ou égal à " + str(iv_nb_dessert_total.get()) + ".")
            b_erreur = TRUE
        if int(p_champ_nbboisson_m) < iv_nb_boisson_total.get():
            messagebox.showerror(title = "Erreur modification", message = str(iv_nb_boisson_total.get()) + " boisson(s) sont déjà enregistrée(s). Vous avez demandé " + str(p_champ_nbboisson_m) + " boissons souhaitée(s). Veuillez saisir un entier supérieur ou égal à " + str(iv_nb_boisson_total.get()) + ".")
            b_erreur = TRUE
        
    #(2)Code si pas d'erreur
    if b_erreur == FALSE :
        sv_nb.set(p_champ_nbpers_m)  #on met la valeur que l'utilisateur a saisi pour le nombre de personne (on remplace la valeur affichée auparavant par la nouvelle valeur)
        iv_nb_entree_souhaite.set(p_champ_nbentree_m)
        progressbar_entree.configure(maximum = iv_nb_entree_souhaite.get())
        iv_nb_plat_souhaite.set(p_champ_nbplat_m)
        progressbar_plat.configure(maximum =  iv_nb_plat_souhaite.get())
        iv_nb_dessert_souhaite.set(p_champ_nbdessert_m)
        progressbar_dessert.configure(maximum = iv_nb_dessert_souhaite.get())
        iv_nb_boisson_souhaite.set(p_champ_nbboisson_m)
        progressbar_boisson.configure(maximum = iv_nb_boisson_souhaite.get()) 

    #(3)Code si erreur
    if b_erreur == TRUE :
        # je réinitialise mes objets graphiques à l'aide des variables globales
        resultatpers_m.set(sv_nb.get()) 
        resultatentree_m.set(iv_nb_entree_souhaite.get())
        resultatplat_m.set(iv_nb_plat_souhaite.get())
        resultatdessert_m.set(iv_nb_dessert_souhaite.get())
        resultatboisson_m.set(iv_nb_boisson_souhaite.get())

    p_fenetre.destroy()

#fonction du bouton [MODIFIER PARAMETRES] appartenant à la fenêtre "fenetre_principale"
#permet d'ouvrir une nouvelle fenêtre temporaire qui sert a saisir toutes les informations nécessaires
def ouvrir_fenetre_modifier_param():
    #creation des interfaces graphiques
    fenetre_modifier_param = Toplevel(ma_fenetre_principale)
    label_nbpers_m = Label(fenetre_modifier_param, text = "Le nombre de personne au repas est de : ")
    champ_nbpers_m = Entry(fenetre_modifier_param, textvariable = resultatpers_m)
    label_nbentree_m = Label(fenetre_modifier_param, text = "Le nombre d'entrées à prévoir : ")
    champ_nbentree_m = Entry(fenetre_modifier_param, textvariable= resultatentree_m)
    label_nbplat_m = Label(fenetre_modifier_param, text = "Le nombre de plats à prévoir : ")
    champ_nbplat_m = Entry(fenetre_modifier_param, textvariable= resultatplat_m)
    label_nbdessert_m = Label(fenetre_modifier_param, text = "Le nombre de dessert à prévoir : ")
    champ_nbdessert_m = Entry(fenetre_modifier_param, textvariable= resultatdessert_m)
    label_nbboisson_m = Label(fenetre_modifier_param, text = "Le nombre de boissons à prévoir : ")
    champ_nbboisson_m = Entry(fenetre_modifier_param, textvariable= resultatboisson_m)
    bouton_ok_m = Button(fenetre_modifier_param, text = "OK", command = lambda : modifier_param(champ_nbpers_m.get(), champ_nbentree_m.get(), champ_nbplat_m.get(), champ_nbdessert_m.get(), champ_nbboisson_m.get(), fenetre_modifier_param))
    bouton_annuler_m = Button(fenetre_modifier_param, text = "ANNULER", command = lambda : fenetre_modifier_param.destroy())

    #placement des interfaces graphiques
    label_nbpers_m.grid(row=1, column = 1)
    champ_nbpers_m.grid(row=2, column=1)
    label_nbentree_m.grid(row=3, column = 1)
    champ_nbentree_m.grid(row=4, column=1)
    label_nbplat_m.grid(row=5, column=1)
    champ_nbplat_m.grid(row=6, column=1)
    label_nbdessert_m.grid(row=7, column=1)
    champ_nbdessert_m.grid(row=8, column=1)
    label_nbboisson_m.grid(row=9, column=1)
    champ_nbboisson_m.grid(row=10, column=1)
    bouton_ok_m.grid(column= 3, row=11)
    bouton_annuler_m.grid(column=2, row=11)

#=============================================FENETRE [SELECTIONNER LA LISTE SUR ACTION AJOUTER]==============================================
#fonction du bouton [AJOUTER] de la fenêtre principale
#affiche les catégories et demande à l'utilisateur dans quelle catégorie il souhaite ajouter
def ouvrir_fenetre_choix_a():
    #creation des interfaces graphiques
    fenetre_choix_ca = Toplevel(ma_fenetre_principale)
    label_question_ca = Label(fenetre_choix_ca, text = "Dans quelle catégorie voulez-vous ajouter ?")
    bouton_entree_ca = Button(fenetre_choix_ca, image = photo_entree, command = lambda : ouvrir_fenetre_ajouter("Entrée"))
    bouton_plat_ca = Button(fenetre_choix_ca, image = photo_plat, command = lambda: ouvrir_fenetre_ajouter("Plat"))
    bouton_dessert_ca = Button(fenetre_choix_ca, image = photo_dessert, command = lambda : ouvrir_fenetre_ajouter("Dessert"))
    bouton_boisson_ca = Button(fenetre_choix_ca, image = photo_boisson, command = lambda : ouvrir_fenetre_ajouter("Boisson"))

    #placement des interfaces graphiques
    label_question_ca.grid(row=0, column = 0)
    bouton_entree_ca.grid(row=0, column =1)
    bouton_plat_ca.grid(row=0, column=2)
    bouton_dessert_ca.grid(row=0,column=3)
    bouton_boisson_ca.grid(row=0,column=4)


#=============================================FENETRE [AJOUTER]======================================================

#fonction du bouton [AJOUTER] appartenant a la fenetre "fenetre_ajouter"
#permet de rajouter, selon la categorie, toutes les informations
def ajouter_nourriture(pp_categorie, p_nom, p_prenom, p_nourriture, p_quantite,p_fenetre):

    #(1)détection des erreurs de saisie de l'utilisateur 
    b_erreur = FALSE 

    if len(p_nom)== 0 or len(p_prenom) == 0 or len(p_nourriture) == 0 or len(p_quantite)== 0 :
        b_erreur = TRUE 
        messagebox.showerror(title = "Erreur ajout", message = "Vous devez saisir une valeur dans tous les champs")
        return

    if p_nom.isnumeric() == TRUE or p_nom.isnumeric() == TRUE or p_nourriture.isnumeric() == TRUE or p_quantite.isnumeric() == FALSE :
        b_erreur = TRUE
        messagebox.showerror(title = "Erreur ajout", message = "Certaines conditions de votre saisie n'ont pas été respecté : Nom, Prénom, Nourriture doivent être des caractères et Quantité doit être un entier")
        return

    if pp_categorie == "Entrée" :
        total_e = int(p_quantite) + iv_nb_entree_total.get() #on comptabilise toutes les quantités présentes la liste (ici liste_entrée)
        if total_e > iv_nb_entree_souhaite.get() :
            diff_e = total_e - iv_nb_entree_souhaite.get()
            b_erreur = TRUE
            messagebox.showerror(title = "Erreur", message= "Vous avez entré trop d'entrées (+" +str(diff_e) + ")") #on n'ajoute pas les valeurs de l'utilisateur si elles ne respectent pas les contraintes fixées avant par  l'utilisateur (dans la fenetre "fenetre_modifier_param")

    if pp_categorie == "Plat" :
        total_p = int(p_quantite) + iv_nb_plat_total.get()
        if total_p > iv_nb_plat_souhaite.get():
            diff_p = total_p - iv_nb_plat_souhaite.get()
            b_erreur = TRUE
            messagebox.showerror(title = "Erreur", message= "Vous avez entré trop de plats (+" +str(diff_p) + ")")    

    if pp_categorie == "Dessert" :
        total_d = int(p_quantite) + iv_nb_dessert_total.get()
        if total_d > iv_nb_dessert_souhaite.get():
            diff_d = total_d - iv_nb_dessert_souhaite.get()
            b_erreur = TRUE
            messagebox.showerror(title = "Erreur", message= "Vous avez entré trop de desserts (+" +str(diff_d) + ")")    
        
    if pp_categorie == "Boisson" :
        total_b = int(p_quantite) + iv_nb_boisson_total.get()
        if total_b > iv_nb_boisson_souhaite.get():
            diff_b = total_b - iv_nb_boisson_souhaite.get()
            b_erreur = TRUE
            messagebox.showerror(title = "Erreur", message= "Vous avez entré trop de boissons (+" +str(diff_b) + ")")
        
    #(2)code si pas d'erreur 
    if b_erreur == FALSE :
        if pp_categorie == "Entrée":
            liste_entree.append((p_nom, p_prenom,pp_categorie, p_nourriture, p_quantite)) #on rajoute toutes les informations dans la liste concernée
            iv_nb_entree_total.set(total_e) #on actualise le total d'entrées
            couleur_barre(total_e, iv_nb_entree_souhaite.get(), progressbar_entree)
        elif pp_categorie == "Plat":
            liste_plat.append((p_nom, p_prenom,pp_categorie, p_nourriture, p_quantite))
            iv_nb_plat_total.set(total_p)
            couleur_barre(total_p, iv_nb_plat_souhaite.get(), progressbar_plat)
        elif pp_categorie == "Dessert":
            liste_dessert.append((p_nom, p_prenom,pp_categorie, p_nourriture, p_quantite))
            iv_nb_dessert_total.set(total_d)
            couleur_barre(total_d, iv_nb_dessert_souhaite.get(), progressbar_dessert )
        elif pp_categorie == "Boisson":
            liste_boisson.append((p_nom, p_prenom,pp_categorie, p_nourriture, p_quantite))
            iv_nb_boisson_total.set(total_b)
            couleur_barre(total_b, iv_nb_boisson_souhaite.get(), progressbar_boisson )
    


    p_fenetre.destroy()

#fonction du bouton [AJOUTER] appartenant a la fenetre fenetre_choix_action
#permet l'ouverture de la fenetre "fenetre_ajouter" où l'on peut entrer toutes les informations
def ouvrir_fenetre_ajouter(p_categorie):
        fenetre_ajouter = Toplevel(ma_fenetre_principale)
        #création des interfaces graphiques
        label_nom_a = Label(fenetre_ajouter, text = "Nom : ")
        champ_nom_a = Entry(fenetre_ajouter)
        label_prenom = Label(fenetre_ajouter, text = "Prénom : ")
        champ_prenom_a = Entry(fenetre_ajouter)
        label_categorie_a = Label(fenetre_ajouter, text = "Catégorie :")
        text_categorie_a = Text(fenetre_ajouter, width = 15, height = 1)
        text_categorie_a.insert(END, p_categorie)
        text_categorie_a.configure(state = "disabled")
        label_nomnourriture_a = Label(fenetre_ajouter, text = "Nom de l'aliment : ")
        champ_nomnourriture_a = Entry(fenetre_ajouter)
        label_quantite_a = Label(fenetre_ajouter, text = "Quantité : ")
        champ_quantite_a = Entry(fenetre_ajouter)
        bouton_ajouter_a = Button(fenetre_ajouter, text = "AJOUTER", command = lambda : ajouter_nourriture(p_categorie, champ_nom_a.get(), champ_prenom_a.get(), champ_nomnourriture_a.get(), champ_quantite_a.get(), fenetre_ajouter))
        bouton_annuler_a = Button(fenetre_ajouter, text = "ANNULER", command = lambda : fenetre_ajouter.destroy())

        #placement des interfaces graphiques
        label_nom_a.grid(row=0, column=0)
        champ_nom_a.grid(row=0, column=1)
        label_prenom.grid(row=1,column=0)
        champ_prenom_a.grid(row=1,column=1)
        label_categorie_a.grid(row=2,column=0)
        text_categorie_a.grid(row=2,column=1)
        label_nomnourriture_a.grid(row=3, column=0)
        champ_nomnourriture_a.grid(row=3, column=1)
        label_quantite_a.grid(row=4, column=0)
        champ_quantite_a.grid(row=4, column=1)
        bouton_ajouter_a.grid(row= 5, column = 3)
        bouton_annuler_a.grid(row=5, column=2)

#============================================FENETRE [SELECTIONNER LA LISTE SUR ACTION LISTER]========================================

#fonction du bouton [LISTER] de la fenetre principale
#affiche les catégories et demande à l'utilisateur quelle catégorie souhaite-t-il visualiser
def ouvrir_fenetre_choix_l():
    #creation des interfaces graphiques
    fenetre_choix_cl = Toplevel(ma_fenetre_principale)
    label_question_cl = Label(fenetre_choix_cl, text = "Quelle catégorie voulez-vous lister ?")
    bouton_entree_cl = Button(fenetre_choix_cl, image = photo_entree, command = lambda : ouvrir_fenetre_lister("Entrée"))
    bouton_plat_cl = Button(fenetre_choix_cl, image = photo_plat, command = lambda: ouvrir_fenetre_lister("Plat"))
    bouton_dessert_cl = Button(fenetre_choix_cl, image = photo_dessert, command = lambda : ouvrir_fenetre_lister("Dessert"))
    bouton_boisson_cl = Button(fenetre_choix_cl, image = photo_boisson, command = lambda : ouvrir_fenetre_lister("Boisson"))

    #placement des interfaces graphiques
    label_question_cl.grid(row=0, column = 0)
    bouton_entree_cl.grid(row=0, column =1)
    bouton_plat_cl.grid(row=0, column=2)
    bouton_dessert_cl.grid(row=0,column=3)
    bouton_boisson_cl.grid(row=0,column=4)


#============================================FENETRE [LISTER]=========================================

#fonction de mise à jour qui calcule la somme des quantités sur tous les enregistrements d'une liste spécifique
def somme_quantite(p_liste):
    somme_q = 0
    for i in range (0,len(p_liste)):
        somme_q = somme_q + int(p_liste[i][4])

    return somme_q

#fonction du bouton [VALIDER] appartenant à la fenetre "fenetre_modification_info"
#permet de changer les informations de la ligne sélectionnée auparavant
def modification_enregistrement(p_nom, p_prenom, p_cate, p_nourriture, p_quantite, p_curItem, pp_tableau, p_listeselect, p_fenetre):
    #récupération de la quantité de l'enregistrement avant la modification
    quantite_avant = p_listeselect[int(p_curItem)][4]
    if p_cate == "Entrée":
        res = somme_quantite(liste_entree)
        total = res - int(quantite_avant) + int(p_quantite) # on prend la somme des quantités de la liste à laquelle on retire la quantite de l'élément à modifier puis on rajoute la quantité du nouvel élément
        if total > iv_nb_entree_souhaite.get():
            messagebox.showerror(title = "Erreur modification", message = "Vous avez saisi trop d'entrées, le total est de : " + str(total) + " alors que le nombre d'entrées maximal est de : " + str(iv_nb_entree_souhaite.get()))
            return

    if p_cate == "Plat":
        res = somme_quantite(liste_plat)
        total = res - int(quantite_avant) + int(p_quantite) # on prend la somme des quantités de la liste à laquelle on retire la quantite de l'élément à modifier puis on rajoute la quantité du nouvel élément
        if total > iv_nb_plat_souhaite.get():
            messagebox.showerror(title = "Erreur modification", message = "Vous avez saisi trop de plats, le total est de : " + str(total) + " alors que le nombre de plats maximal est de : " + str(iv_nb_plat_souhaite.get()))
            return

    if p_cate == "Dessert":
        res = somme_quantite(liste_dessert)
        total = res - int(quantite_avant) + int(p_quantite) # on prend la somme des quantités de la liste à laquelle on retire la quantite de l'élément à modifier puis on rajoute la quantité du nouvel élément
        if total > iv_nb_dessert_souhaite.get():
            messagebox.showerror(title = "Erreur modification", message = "Vous avez saisi trop de desserts, le total est de : " + str(total) + " alors que le nombre de desserts maximal est de : " + str(iv_nb_dessert_souhaite.get()))
            return

    if p_cate == "Boisson":
        res = somme_quantite(liste_boisson)
        total = res - int(quantite_avant) + int(p_quantite) # on prend la somme des quantités de la liste à laquelle on retire la quantite de l'élément à modifier puis on rajoute la quantité du nouvel élément
        if total > iv_nb_boisson_souhaite.get():
            messagebox.showerror(title = "Erreur modification", message = "Vous avez saisi trop de boissons, le total est de : " + str(total) + " alors que le nombre de boissons maximal est de : " + str(iv_nb_boisson_souhaite.get()))
            return

    #pour la catégorie en cours, cas où la somme des quantités n'est pas supérieure à la quantité souhaitée
    pp_tableau.delete(p_curItem) #on supprime la valeur sélectionnée dans le tableau
    del((p_listeselect[int(p_curItem)])) #on supprime la valeur sélectionnée dans la liste lui correspondant
    pp_tableau.insert(parent = '', index = 'end', iid= p_curItem , values = (p_nom, p_prenom, p_cate, p_nourriture, p_quantite)) #on ajoute les nouvelles valeurs dans le tableau selon les instructions de l'utilisateur dans "fenetre_modification_info"
    p_listeselect.insert(int(p_curItem), (p_nom, p_prenom, p_cate, p_nourriture, p_quantite))

    if p_cate == "Entrée":
        res = somme_quantite(liste_entree)
        iv_nb_entree_total.set(res)
        couleur_barre(res, iv_nb_entree_souhaite.get(), progressbar_entree)

    if p_cate == "Plat":
        res = somme_quantite(liste_plat)
        iv_nb_plat_total.set(res)
        couleur_barre(res, iv_nb_plat_souhaite.get(), progressbar_plat)

    if p_cate == "Dessert":
        res = somme_quantite(liste_dessert)
        iv_nb_dessert_total.set(res)
        couleur_barre(res, iv_nb_dessert_souhaite.get(), progressbar_dessert)

    if p_cate == "Boisson":
        res = somme_quantite(liste_boisson)
        iv_nb_boisson_total.set(res)
        couleur_barre(res, iv_nb_boisson_souhaite.get(), progressbar_boisson)

    p_fenetre.destroy()


#fonction du bouton [MODIFIER] appartenant a la fenetre "fenetre_lister"
#fonction qui permet d'ouvrir la fenetre "fenetre_modification_info" ou l'on peut voir et changer les informations que l'on souhaite
def saisie_modifier_enregistrement(p_tableau, pp_categorie):
    if len(p_tableau.selection()) == 0:
        messagebox.showerror(title = "Erreur modification", message = "Vous devez sélectionner une ligne à modifier")
    else :
        fenetre_modication_info = Toplevel(p_tableau)
        curItem = p_tableau.selection()[0]

        if pp_categorie == "Entrée":
            liste_select = liste_entree.copy()
        elif pp_categorie == "Plat":
            liste_select = liste_plat.copy()
        elif pp_categorie == "Dessert":
            liste_select = liste_dessert.copy()
        elif pp_categorie == "Boisson":
            liste_select = liste_boisson.copy()

        #creation de variables pour modifier les anciennes données
        nom_intermediaire = StringVar()
        prenom_intermediaire = StringVar()
        categorie_intermediaire = StringVar()
        nourriture_intermediaire = StringVar()
        quantite_intermediaire = StringVar()
        
        #modification de ses variables pour leur mettre les valeurs initiales
        nom_intermediaire.set(liste_select[int(curItem)][0])
        prenom_intermediaire.set(liste_select[int(curItem)][1])
        categorie_intermediaire.set(liste_select[int(curItem)][2])
        nourriture_intermediaire.set(liste_select[int(curItem)][3])
        quantite_intermediaire.set(liste_select[int(curItem)][4])

        #creation des interfaces graphiques
        label_nom_mi = Label(fenetre_modication_info, text = "Nom : ")
        champ_nom_mi = Entry(fenetre_modication_info, textvariable = nom_intermediaire)
        label_prenom_mi = Label(fenetre_modication_info, text = "Prénom : ")
        champ_prenom_mi = Entry(fenetre_modication_info, textvariable = prenom_intermediaire)
        label_categorie_mi = Label(fenetre_modication_info, text = "Catégorie : ")
        text_categorie_mi = Text(fenetre_modication_info, width = 15, height = 1)
        text_categorie_mi.insert(END, categorie_intermediaire.get())
        text_categorie_mi.configure(state = "disabled")
        label_nourriture_mi = Label(fenetre_modication_info, text = "Nourriture : ")
        champ_nourriture_mi = Entry(fenetre_modication_info, textvariable = nourriture_intermediaire)
        label_quantite_mi = Label(fenetre_modication_info, text = "Quantité : ")
        champ_quantite_mi = Entry(fenetre_modication_info, textvariable = quantite_intermediaire)

        #la liste concernée par le bouton [VALIDER] dépend de la catégorie concernée
        if pp_categorie == "Entrée":
            bouton_valider_mi = Button(fenetre_modication_info, text = "VALIDER", command = lambda : modification_enregistrement(champ_nom_mi.get(), champ_prenom_mi.get(), categorie_intermediaire.get(), champ_nourriture_mi.get(), champ_quantite_mi.get(), curItem, p_tableau, liste_entree, fenetre_modication_info))
        elif pp_categorie == "Plat":
            bouton_valider_mi = Button(fenetre_modication_info, text = "VALIDER", command = lambda : modification_enregistrement(champ_nom_mi.get(), champ_prenom_mi.get(), categorie_intermediaire.get(), champ_nourriture_mi.get(), champ_quantite_mi.get(), curItem, p_tableau, liste_plat, fenetre_modication_info))
        elif pp_categorie == "Dessert":
            bouton_valider_mi = Button(fenetre_modication_info, text = "VALIDER", command = lambda : modification_enregistrement(champ_nom_mi.get(), champ_prenom_mi.get(), categorie_intermediaire.get(), champ_nourriture_mi.get(), champ_quantite_mi.get(), curItem, p_tableau, liste_dessert, fenetre_modication_info))
        elif pp_categorie == "Boisson":
            bouton_valider_mi = Button(fenetre_modication_info, text = "VALIDER", command = lambda : modification_enregistrement(champ_nom_mi.get(), champ_prenom_mi.get(), categorie_intermediaire.get(), champ_nourriture_mi.get(), champ_quantite_mi.get(), curItem, p_tableau, liste_boisson, fenetre_modication_info))
        
        bouton_annuler_mi = Button(fenetre_modication_info, text = "ANNULER", command = lambda : fenetre_modication_info.destroy())
        
        #placement des interfaces graphiques
        label_nom_mi.grid(row=0, column=0)
        champ_nom_mi.grid(row=0, column=1)
        label_prenom_mi.grid(row=1, column=0)
        champ_prenom_mi.grid(row=1, column=1)
        label_categorie_mi.grid(row=2, column=0)
        text_categorie_mi.grid(row=2, column=1)
        label_nourriture_mi.grid(row=3,column=0)
        champ_nourriture_mi.grid(row=3, column=1)
        label_quantite_mi.grid(row=4, column=0)
        champ_quantite_mi.grid(row=4, column=1)
        bouton_valider_mi.grid(row=5, column=3)
        bouton_annuler_mi.grid(row=5, column=2)

#fonction du bouton [SUPPRIMER] appartenant a la fenetre "fenetre_lister"
#permet de supprimer les informations d'un individu sélectionné
def supprimer_enregistrement(p_tableau, pp_categorie):
    if len(p_tableau.selection()) == 0:
        messagebox.showerror(title = "Erreur suppression", message = "Vous devez sélectionner une ligne à supprimer")
    else :
        curItem = p_tableau.selection()[0] #permet de savoir quelle ligne a sélectionné l'utilisateur
        reponse = messagebox.askyesno(title = "Confirmation de suppression", message = "Voulez-vous vraiment supprimer la ligne ?")
        if reponse :
            if pp_categorie == "Entrée":
                del(liste_entree[int(curItem)])
                p_tableau.delete(curItem)
                res = somme_quantite(liste_entree)
                iv_nb_entree_total.set(res) #on met à jour le total saisi pour la catégorie 
                couleur_barre(res, iv_nb_entree_souhaite.get(), progressbar_entree) #on met à jour la barre de progression

            if pp_categorie == "Plat":
                del(liste_plat[int(curItem)])
                p_tableau.delete(curItem)
                res = somme_quantite(liste_plat)
                iv_nb_plat_total.set(res)
                couleur_barre(res, iv_nb_plat_souhaite.get(), progressbar_plat)

            if pp_categorie == "Dessert":
                del(liste_dessert[int(curItem)])
                p_tableau.delete(curItem)
                res = somme_quantite(liste_dessert)
                iv_nb_dessert_total.set(res)
                couleur_barre(res, iv_nb_dessert_souhaite.get(), progressbar_dessert)

            if pp_categorie == "Boisson":
                del(liste_boisson[int(curItem)])
                p_tableau.delete(curItem)
                res = somme_quantite(liste_boisson)
                iv_nb_boisson_total.set(res) 
                couleur_barre(res, iv_nb_boisson_souhaite.get(), progressbar_boisson)   



#fonction du bouton [LISTER] appartenant a la fenetre principale
#permet d'ouvrir une nouvelle fenetre nommée "fenetre_lister"
def ouvrir_fenetre_lister(p_categorie):
    fenetre_lister = Toplevel(ma_fenetre_principale)

    tableau_lister = Treeview(fenetre_lister)
    tableau_lister["columns"]=("Nom", "Prénom", "Catégorie", "Nourriture", "Quantité")
    tableau_lister.column("#0", width=0, stretch=NO)
    tableau_lister.column("Nom", anchor=CENTER)
    tableau_lister.column("Prénom", anchor = CENTER)
    tableau_lister.column("Catégorie", anchor = CENTER)
    tableau_lister.column("Nourriture", anchor = CENTER)
    tableau_lister.column("Quantité", anchor = CENTER)

    tableau_lister.heading("#0", text ="", anchor = CENTER)
    tableau_lister.heading("Nom", text = "Nom", anchor = CENTER)
    tableau_lister.heading("Prénom", text = "Prénom", anchor = CENTER)
    tableau_lister.heading("Catégorie", text = "Catégorie", anchor = CENTER)
    tableau_lister.heading("Nourriture", text = "Nourriture", anchor = CENTER)
    tableau_lister.heading("Quantité", text="Quantité", anchor = CENTER)
    
    if p_categorie == "Entrée" :
        for j in tableau_lister.get_children() :
            tableau_lister.delete(j)#on supprime les valeurs du tableau qui pouvaient être présentes avant pour ne pas mélanger les listes
        for i in range (0,len(liste_entree)):
            tableau_lister.insert(parent = '', index = 'end', iid= i , values = (liste_entree[i][0], liste_entree[i][1], "Entrée", liste_entree[i][3], liste_entree[i][4])) #on insère tous les éléments de la liste entrée

    if p_categorie == "Plat":
        for j in tableau_lister.get_children() :
            tableau_lister.delete(j)
        for i in range (0,len(liste_plat)):
            tableau_lister.insert(parent = '', index = 'end', iid= i , values = (liste_plat[i][0], liste_plat[i][1], "Plat", liste_plat[i][3], liste_plat[i][4]))

    if p_categorie == "Dessert":
        for j in tableau_lister.get_children() :
            tableau_lister.delete(j)
        for i in range (0,len(liste_dessert)):
            tableau_lister.insert(parent = '', index = 'end', iid= i , values = (liste_dessert[i][0], liste_dessert[i][1], "Dessert", liste_dessert[i][3], liste_dessert[i][4]))

    if p_categorie == "Boisson":
        for j in tableau_lister.get_children() :
            tableau_lister.delete(j)
        for i in range (0,len(liste_boisson)):
            tableau_lister.insert(parent = '', index = 'end', iid= i , values = (liste_boisson[i][0], liste_boisson[i][1], "Boisson", liste_boisson[i][3], liste_boisson[i][4]))


    bouton_modifier_l = Button(fenetre_lister, text = "MODIFIER", command = lambda : saisie_modifier_enregistrement(tableau_lister, p_categorie))
    bouton_supprimer_l = Button(fenetre_lister, text = "SUPPRIMER", command = lambda : supprimer_enregistrement(tableau_lister, p_categorie))
    bouton_fermer_l = Button(fenetre_lister, text = "FERMER", command = lambda : fenetre_lister.destroy())

    tableau_lister.grid(column=0, row=0)
    bouton_modifier_l.grid(column = 1, row=1)
    bouton_supprimer_l.grid(column=1, row=2)
    bouton_fermer_l.grid(column=0, row=3)

#===========================================FENETRE [SELECTIONNER ACTION SUR LA LISTE]==================================================
#fonction du bouton d'une des images appartenant à la fenêtre principale
#permet l'ouverture de la fenetre "fenetre_choix_action"
def ouvrir_fenetre_choix_action(p_categorie):
    fenetre_choix_action = Toplevel(ma_fenetre_principale)
    label_question_caa = Label(fenetre_choix_action, text = "Quelle action voulez-vous effectuer sur la catégorie : ")
    label_categorie_caa = Label(fenetre_choix_action, textvariable = p_categorie)
    bouton_ajouter_caa = Button(fenetre_choix_action, text = "AJOUTER", command = lambda : ouvrir_fenetre_ajouter(p_categorie))
    bouton_lister_caa = Button(fenetre_choix_action, text = "LISTER", command = lambda : ouvrir_fenetre_lister(p_categorie))

    label_question_caa.grid(row=0, column=0)
    label_categorie_caa.grid(row = 0, column=1)
    bouton_ajouter_caa.grid(row=0, column=2)
    bouton_lister_caa.grid(row=0,column=3)
#============================================FENETRE [PRINCIPALE]================================================

#creation des couleurs qui entourent les images
def couleur1e(e):
    frame_entree.configure(bg="red")

def couleur2e(e):
    frame_entree.configure(bg="black")

def couleur1p(e):
    frame_plat.configure(bg="red")

def couleur2p(e):
    frame_plat.configure(bg="black")

def couleur1d(e):
    frame_dessert.configure(bg="red")

def couleur2d(e):
    frame_dessert.configure(bg="black")

def couleur1b(e):
    frame_boisson.configure(bg="red")

def couleur2b(e):
    frame_boisson.configure(bg="black")

#creation des interfaces graphiques
sv_nb = IntVar()
sv_nb.set(0)
label_presentation = Label(ma_fenetre_principale, text = "Organisation d'un repas pour : ", bg = "bisque1")
label_nbpers = Label(ma_fenetre_principale, textvariable = sv_nb, bg = "bisque1")
photo_param = PhotoImage(file = "./images/image_param.png")
bouton_modifier_param = Button(ma_fenetre_principale, image = photo_param , command = lambda : ouvrir_fenetre_modifier_param())
categorie = StringVar()
categorie.set("initialisation")
frame_boutons = Frame(ma_fenetre_principale, bg= "bisque1", height = 1)
bouton_ajouter = Button(frame_boutons, text = "AJOUTER", command = lambda : ouvrir_fenetre_choix_a(), width = 7)
bouton_lister = Button(frame_boutons, text = "LISTER", command = lambda : ouvrir_fenetre_choix_l(), width = 7)
bouton_fermer = Button(ma_fenetre_principale, text = "FERMER", command = lambda : ma_fenetre_principale.quit())

    ##interface liée à "l'entrée"
iv_nb_entree_total = IntVar()
iv_nb_entree_total.set(0)
iv_nb_entree_souhaite = IntVar()
iv_nb_entree_souhaite.set(0)

frame_entree = Frame(ma_fenetre_principale, bd=1, bg= "black")
photo_entree= PhotoImage(file='./images/image_entree2.png')
bouton_entree = Button(frame_entree, image = photo_entree, command = lambda : ouvrir_fenetre_choix_action("Entrée"))
frame_entree.bind('<Enter>', couleur1e) #changement du couleur quand le curseur passe dessus
frame_entree.bind('<Leave>', couleur2e)
progressbar_entree = Progressbar(ma_fenetre_principale, orient = HORIZONTAL, variable = iv_nb_entree_total ,length = 100, maximum = 1)

label_nb_entree_total = Label(ma_fenetre_principale, textvariable = iv_nb_entree_total, bg = "bisque1")
label_division_entree = Label(ma_fenetre_principale, text = "/", bg ="bisque1")
label_nb_entree_souhaite = Label(ma_fenetre_principale, textvariable=iv_nb_entree_souhaite, bg = "bisque1")

    ##interface liée au "plat"
iv_nb_plat_total = IntVar()
iv_nb_plat_total.set(0)
iv_nb_plat_souhaite = IntVar()
iv_nb_plat_souhaite.set(0)

frame_plat = Frame(ma_fenetre_principale, bd=1, bg= "black")
photo_plat = PhotoImage(file = './images/image_plat2.png')
bouton_plat = Button(frame_plat, image = photo_plat, command = lambda : ouvrir_fenetre_choix_action("Plat"))
frame_plat.bind('<Enter>', couleur1p)
frame_plat.bind('<Leave>', couleur2p)
progressbar_plat = Progressbar(ma_fenetre_principale, orient = HORIZONTAL, length = 100, variable = iv_nb_plat_total, maximum=1)

label_nb_plat_total = Label(ma_fenetre_principale, textvariable = iv_nb_plat_total, bg = "bisque1")
label_division_plat = Label(ma_fenetre_principale, text = "/", bg ="bisque1")
label_nb_plat_souhaite = Label(ma_fenetre_principale, textvariable=iv_nb_plat_souhaite, bg = "bisque1")

    ##interface liée au "dessert"
iv_nb_dessert_total = IntVar()
iv_nb_dessert_total.set(0)
iv_nb_dessert_souhaite = IntVar()
iv_nb_dessert_souhaite.set(0)

frame_dessert = Frame(ma_fenetre_principale, bd=1, bg="black")
photo_dessert = PhotoImage(file = './images/image_dessert2.png')
bouton_dessert = Button(frame_dessert, image = photo_dessert, command = lambda :ouvrir_fenetre_choix_action("Dessert"))
frame_dessert.bind('<Enter>', couleur1d)
frame_dessert.bind('<Leave>', couleur2d)
progressbar_dessert = Progressbar(ma_fenetre_principale, orient = HORIZONTAL, length = 100, variable = iv_nb_dessert_total, maximum = 1)

label_nb_dessert_total = Label(ma_fenetre_principale, textvariable = iv_nb_dessert_total, bg = "bisque1")
label_division_dessert = Label(ma_fenetre_principale, text = "/", bg ="bisque1")
label_nb_dessert_souhaite = Label(ma_fenetre_principale, textvariable=iv_nb_dessert_souhaite, bg = "bisque1")

    ##interface liée à la "boisson"
iv_nb_boisson_total = IntVar()
iv_nb_boisson_total.set(0)
iv_nb_boisson_souhaite = IntVar()
iv_nb_boisson_souhaite.set(0)

frame_boisson = Frame(ma_fenetre_principale, bd = 1, bg = "black")
photo_boisson = PhotoImage(file = './images/image_boisson3.png')
bouton_boisson = Button(frame_boisson, image = photo_boisson, command = lambda : ouvrir_fenetre_choix_action("Boisson"))
frame_boisson.bind('<Enter>', couleur1b)
frame_boisson.bind('<Leave>', couleur2b)
progressbar_boisson = Progressbar(ma_fenetre_principale, orient = HORIZONTAL, length = 100, variable = iv_nb_boisson_total, maximum = 1)

label_nb_boisson_total = Label(ma_fenetre_principale, textvariable = iv_nb_boisson_total, bg = "bisque1")
label_division_boisson = Label(ma_fenetre_principale, text = "/", bg ="bisque1")
label_nb_boisson_souhaite = Label(ma_fenetre_principale, textvariable=iv_nb_boisson_souhaite, bg = "bisque1")

#positionnement des interfaces graphiques
label_presentation.grid(row = 0, column = 1)
label_nbpers.grid(row= 0, column = 2)
bouton_modifier_param.grid(row=0, column=7)
bouton_ajouter.grid(row=0, column=0, pady=20)
bouton_lister.grid(row=0, column=1, pady=20)
bouton_fermer.grid(row=7, column=8)
frame_boutons.grid(row=7, column=2, columnspan = 2, pady=10)

frame_entree.grid(row=1, column=1)
bouton_entree.grid(row=1, column=1)
progressbar_entree.grid(row=1, column = 2)
label_nb_entree_total.grid(row=1, column=3)
label_division_entree.grid(row=1, column=4)
label_nb_entree_souhaite.grid(row=1, column=5)

frame_plat.grid(row=2, column=1)
bouton_plat.grid(row=2,column=1)
progressbar_plat.grid(row=2, column = 2)
label_nb_plat_total.grid(row=2, column = 3)
label_division_plat.grid(row=2, column = 4)
label_nb_plat_souhaite.grid(row=2, column = 5)

frame_dessert.grid(row=3, column = 1)
bouton_dessert.grid(row=3, column=1)
progressbar_dessert.grid(row=3, column = 2)
label_nb_dessert_total.grid(row=3, column=3)
label_division_dessert.grid(row=3, column =4)
label_nb_dessert_souhaite.grid(row=3, column=5)

frame_boisson.grid(row=4, column=1)
bouton_boisson.grid(row=4, column=1)
progressbar_boisson.grid(row=4, column=2)
label_nb_boisson_total.grid(row=4, column=3)
label_division_boisson.grid(row=4, column=4)
label_nb_boisson_souhaite.grid(row=4, column=5)

ma_fenetre_principale.mainloop()