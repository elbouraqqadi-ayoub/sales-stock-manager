CREATE DATABASE gestion_db;
USE gestion_db;

-- Table des produits
CREATE TABLE produits (
    id INT PRIMARY KEY,
    nom VARCHAR(255),
    categorie VARCHAR(255),
    prix FLOAT,
    stock INT
);

-- Table des ventes
CREATE TABLE ventes (
    id_produit INT ,
    date_vente DATE,
    quantite INT,
    revenu FLOAT,
    FOREIGN KEY (id_produit) REFERENCES produits(id)
);

-- Table d'inventaire
CREATE TABLE inventaire (
    id INT PRIMARY KEY,
    stock INT,
    seuil_alerte INT
);
