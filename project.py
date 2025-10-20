import mysql.connector

#Etape 2: connexion Mysql
db_config = {
    'user': 'root',
    'password': 'cbayoub4', 
    'host': 'localhost',
    'database': 'gestion_db'
}

try:
    conn = mysql.connector.connect(**db_config)     #<=>connect(user='root', password='cbayoub4', host='localhost', database='gestion_db')
    print("Connexion réussie à la base de données.")
    conn.close()
except mysql.connector.Error as err:
    print(f"Erreur MySQL : {err}")

#Etape 3: recuperation et insertion des produits
import requests  

def recuperer_produits_api():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    return response.json()

def inserer_produits():
    try:
        produits = recuperer_produits_api()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for product in produits:
            query = """
                INSERT INTO produits (id, nom, categorie, prix, stock)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE nom=%s, categorie=%s, prix=%s, stock=%s
            """
            values = (
                product['id'], product['title'], product['category'], product['price'], 204,
                product['title'], product['category'], product['price'], 204
            )
            cursor.execute(query, values)

            # Insérer ou mettre à jour dans Inventaire
            seuil_defaut = 5
            cursor.execute("""
                INSERT INTO Inventaire (id, stock, seuil_alerte)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE stock = VALUES(stock), seuil_alerte = VALUES(seuil_alerte)
            """, (product['id'], 204, seuil_defaut))
        conn.commit()
        cursor.close()
        conn.close()
        print("Produits insérés avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        
inserer_produits()

#Etape 4: Simulation des ventes
def enregistrer_vente(id_produit, quantite_vendue):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT prix FROM produits WHERE id = %s", (id_produit,)) #recuperer le prix
        produit = cursor.fetchone()

        if produit:
            prix = produit[0]

            # Récupération du stock dans la table inventaire
            cursor.execute("SELECT stock, seuil_alerte FROM inventaire WHERE id = %s", (id_produit,))
            inventaire = cursor.fetchone()

            stock_actuel = inventaire[0]
            seuil_alerte = inventaire[1]

            # Vérification si le stock est suffisant pour la vente
            if stock_actuel < quantite_vendue:
                print(f"Stock insuffisant. Stock actuel: {stock_actuel}, Quantité demandée: {quantite_vendue}")
                return  
            # Vérification si le stock après vente serait sous le seuil d'alerte
            nouveau_stock = stock_actuel - quantite_vendue
            if nouveau_stock < seuil_alerte:
                print(f" Alerte : Après cette vente, le stock du produit ID {id_produit} serait sous le seuil d'alerte ({seuil_alerte}).")

            # Enregistrer la vente dans la table des ventes
            revenu = prix * quantite_vendue
            cursor.execute(
                "INSERT INTO ventes (id_produit, quantite, revenu, date_vente) VALUES (%s, %s, %s, NOW())",
                (id_produit, quantite_vendue, revenu)
            )
            #mise a jour des stocks
            cursor.execute("UPDATE inventaire SET stock = %s WHERE id = %s", (nouveau_stock, id_produit))  #inventaire
            cursor.execute("UPDATE produits SET stock = %s WHERE id = %s", (nouveau_stock, id_produit)) #produits

            conn.commit()
            print("Vente enregistrée et stock mis à jour.")
        else:
            print(f"Produit avec ID {id_produit} non trouvé dans la table produits.")

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
    finally:
        cursor.close()
        conn.close()


while True:
    try:
        id_produit = int(input("\nSaisir l'ID du produit vendu (ou entrez 0 pour arrêter): "))
        if id_produit == 0:  
            print("Arrêt de l'enregistrement des ventes.")
            break  

        quantite_vendue = int(input("Saisir la quantité vendue: "))
        enregistrer_vente(id_produit, quantite_vendue)
    except ValueError:
        print("Veuillez entrer un nombre valide pour l'ID du produit et la quantité.")

import schedule
import time
schedule.every().day.at("10:00").do(inserer_produits)
while True:
    schedule.run_pending()
    time.sleep(1)
    