import pandas as pd
import geopandas as gpd

# --- 1. Lecture des fichiers CSV ---
batiments = pd.read_csv("new_data/batiment.csv")
infra = pd.read_csv("new_data/infra.csv")

print("=== Aperçu des bâtiments ===")
print(batiments.head(), "\n")

print("=== Aperçu des infrastructures ===")
print(infra.head(), "\n")

# --- 2. Lecture du fichier Excel reseau_en_arbre ---
reseau = pd.read_excel("data/reseau_en_arbre.xlsx")
print("=== Réseau en arbre ===")
print(reseau.head())

# --- 3. Lecture des shapefiles (si besoin) ---
batiments_geo = gpd.read_file("data/batiments.shp")
infra_geo = gpd.read_file("data/infrastructure.shp")

print("\nColonnes du shapefile bâtiments :", batiments_geo.columns)
print("Colonnes du shapefile infrastructures :", infra_geo.columns)

# --- 4. Nettoyage simple (exemple) ---
batiments = batiments.dropna(subset=["id batiment"])
infra = infra.dropna(subset=["id_infra"])

# Nettoyage des identifiants
batiments["id batiment"] = batiments["id batiment"].str.replace("=", "E").str.strip()
infra["id_infra"] = infra["id_infra"].str.strip()

print("\n=== Données nettoyées ===")
print(batiments.head())
print(infra.head())
