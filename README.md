🛒 Projet de Gestion de Produits et de Ventes MySQL
📘 Description

Ce projet Python permet de gérer des produits, des ventes et des stocks à partir d’une base de données MySQL.
Il récupère automatiquement des produits depuis une API externe (FakeStore API
), les insère ou met à jour dans la base de données, simule des ventes et met à jour les stocks en conséquence.

Le script inclut également une tâche planifiée qui met à jour les produits chaque jour à 10h.

⚙️ Fonctionnalités principales

🔗 Connexion à une base MySQL

🌐 Récupération automatique des produits depuis une API publique

💾 Insertion et mise à jour des produits dans les tables produits et inventaire

💸 Simulation de ventes avec mise à jour des stocks

🚨 Alerte de seuil de stock bas

⏰ Mise à jour automatique quotidienne via la librairie schedule

🧱 Structure de la base de données

Le projet utilise une base de données gestion_db contenant au minimum les tables suivantes :

Table produits

| Colonne   | Type              | Description            |
| --------- | ----------------- | ---------------------- |
| id        | INT (PRIMARY KEY) | Identifiant du produit |
| nom       | VARCHAR(255)      | Nom du produit         |
| categorie | VARCHAR(255)      | Catégorie du produit   |
| prix      | FLOAT             | Prix du produit        |
| stock     | INT               | Stock disponible       |

Table inventaire
| Colonne      | Type                                            | Description                |
| ------------ | ----------------------------------------------- | -------------------------- |
| id           | INT (PRIMARY KEY, FOREIGN KEY vers produits.id) | Identifiant du produit     |
| stock        | INT                                             | Quantité en stock          |
| seuil_alerte | INT                                             | Seuil minimal avant alerte |

Table ventes
| Colonne    | Type                               | Description               |
| ---------- | ---------------------------------- | ------------------------- |
| id         | INT (AUTO_INCREMENT, PRIMARY KEY)  | Identifiant de la vente   |
| id_produit | INT (FOREIGN KEY vers produits.id) | Produit vendu             |
| quantite   | INT                                | Quantité vendue           |
| revenu     | FLOAT                              | Revenu généré             |
| date_vente | DATETIME                           | Date et heure de la vente |


🔧 Prérequis

Python 3.x

MySQL installé et configuré

Une base de données gestion_db créée avec les tables ci-dessus

Les modules Python suivants :

pip install mysql-connector-python requests schedule

🚀 Exécution du projet

Configurer la connexion MySQL
Dans le fichier Python, modifier les informations suivantes :

db_config = {
    'user': 'root',
    'password': 'votre_mot_de_passe',
    'host': 'localhost',
    'database': 'gestion_db'
}


Lancer le script principal

python main.py


Simulation de ventes

Le programme demande l’ID du produit vendu et la quantité.

Tapez 0 pour arrêter la simulation.

Mise à jour automatique

Chaque jour à 10h00, le script récupère les produits de l’API et met à jour la base.

🧠 Exemple de fonctionnement
Connexion réussie à la base de données.
Produits insérés avec succès.

Saisir l'ID du produit vendu (ou entrez 0 pour arrêter): 3
Saisir la quantité vendue: 2
Vente enregistrée et stock mis à jour.

Saisir l'ID du produit vendu (ou entrez 0 pour arrêter): 0
Arrêt de l'enregistrement des ventes.

🛠️ Points d’amélioration possibles

Ajouter une interface graphique ou web (Flask/Django).

Générer des rapports automatiques sur les ventes.

Envoyer une notification (email/SMS) lors d’un stock bas.

Gérer les utilisateurs et leurs droits d’accès.

👨‍💻 Auteur

Nom : EL BOURAQQADI Ayoub
Email : aelbouraqqadi@gmail.com
