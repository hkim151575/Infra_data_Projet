# ============================================
# main.py – Projet de planification de raccordement électrique
# Étapes 1 → 4 : Lecture, Modélisation, Difficulté, Planification
# ============================================

import pandas as pd
from batiment import Batiment
from infrastricture import Infrastructure


# =======================
# ÉTAPE 1 : Chargement et nettoyage des données
# =======================
def charger_et_nettoyer_donnees():
    print("=== Étape 1 : Lecture et nettoyage des données ===")

    batiments_df = pd.read_csv("new_data/batiments.csv")
    infra_df = pd.read_csv("new_data/infra.csv")

    # Harmoniser les noms de colonnes
    batiments_df.columns = batiments_df.columns.str.lower().str.strip().str.replace(" ", "_")
    infra_df.columns = infra_df.columns.str.lower().str.strip().str.replace(" ", "_")

    print("\nColonnes bâtiments :", batiments_df.columns.tolist())
    print("Colonnes infrastructures :", infra_df.columns.tolist())

    # Supprimer les lignes vides
    batiments_df = batiments_df.dropna(subset=["id_batiment"])
    infra_df = infra_df.dropna(subset=["id_infra"])

    # Nettoyer les identifiants
    batiments_df["id_batiment"] = (
        batiments_df["id_batiment"]
        .astype(str)
        .str.replace("=", "E")
        .str.replace(" ", "")
        .str.strip()
    )
    infra_df["id_infra"] = infra_df["id_infra"].astype(str).str.replace(" ", "").str.strip()

    print(f"{len(batiments_df)} bâtiments chargés")
    print(f"{len(infra_df)} infrastructures chargées\n")

    return batiments_df, infra_df


# =======================
# ÉTAPE 2 : Création des objets Batiment et Infrastructure
# =======================
def creer_objets(batiments_df, infra_df):
    print("=== Étape 2 : Création des objets ===")

    batiments = {}
    infrastructures = {}

    for _, row in batiments_df.iterrows():
        bat = Batiment(row["id_batiment"], row["type_batiment"], row["nb_maisons"])

        batiments[bat.id] = bat

    for _, row in infra_df.iterrows():
        infra = Infrastructure(row["id_infra"], row["type_infra"])
        infrastructures[infra.id] = infra

    print(f"{len(batiments)} objets Batiment créés")
    print(f"{len(infrastructures)} objets Infrastructure créés\n")

    return batiments, infrastructures


# =======================
# ÉTAPE 3 : Liaison bâtiment ↔ infrastructure via reseau_en_arbre.xlsx
# =======================
def lier_batiments_infras(batiments, infrastructures):
    print("=== Étape 3 : Liaison bâtiments ↔ infrastructures ===")

    reseau_df = pd.read_excel("data/reseau_en_arbre.xlsx")

    # Exemple : chaque ligne contient une relation (id_batiment, id_infra, longueur, nb_maisons)
    for _, row in reseau_df.iterrows():
        id_bat = str(row.get("id_batiment", "")).strip()
        id_infra = str(row.get("id_infra", "")).strip()

        if id_bat in batiments and id_infra in infrastructures:
            infra = infrastructures[id_infra]

            # Mettre à jour longueur et nb maisons si dispo
            if "longueur" in reseau_df.columns:
                infra.longueur = row["longueur"]
            if "nb_maisons" in reseau_df.columns:
                infra.nb_maisons = row["nb_maisons"]

            infra.difficulte = infra.calculer_difficulte()
            batiments[id_bat].ajouter_infrastructure(infra)

    print("Liaisons effectuées avec succès !\n")


# =======================
# ÉTAPE 4 : Calcul des difficultés et planification
# =======================
def calculer_difficultes(batiments):
    print("=== Étape 4 : Calcul des difficultés ===")

    for bat in batiments.values():
        bat.calculer_difficulte()

    # Tri des bâtiments par difficulté croissante
    batiments_tries = sorted(batiments.values(), key=lambda b: b.difficulte)
    print("Bâtiments triés par difficulté :")
    for b in batiments_tries[:10]:
        print(f"{b.id} → difficulté = {b.difficulte:.2f}")

    return batiments_tries


def planifier_phases(batiments_tries):
    print("\n=== Étape 5 : Planification des phases ===")

    total_bats = len(batiments_tries)
    phase_0 = [b for b in batiments_tries if "hopital" in b.type.lower()]  # ex : hôpital
    autres = [b for b in batiments_tries if b not in phase_0]

    n1 = int(0.4 * len(autres))
    n2 = int(0.2 * len(autres))

    phase_1 = autres[:n1]
    phase_2 = autres[n1 : n1 + n2]
    phase_3 = autres[n1 + n2 : n1 + 2 * n2]
    phase_4 = autres[n1 + 2 * n2 :]

    print(f"Phase 0 : {len(phase_0)} bâtiments (hôpital)")
    print(f"Phase 1 : {len(phase_1)} bâtiments (~40%)")
    print(f"Phase 2 : {len(phase_2)} bâtiments (~20%)")
    print(f"Phase 3 : {len(phase_3)} bâtiments (~20%)")
    print(f"Phase 4 : {len(phase_4)} bâtiments (~20%)\n")

    return {
        "phase_0": phase_0,
        "phase_1": phase_1,
        "phase_2": phase_2,
        "phase_3": phase_3,
        "phase_4": phase_4,
    }


# =======================
# MAIN PROGRAMME
# =======================
if __name__ == "__main__":
    batiments_df, infra_df = charger_et_nettoyer_donnees()
    batiments, infrastructures = creer_objets(batiments_df, infra_df)
    lier_batiments_infras(batiments, infrastructures)
    batiments_tries = calculer_difficultes(batiments)
    phases = planifier_phases(batiments_tries)

    print("✅ Planification terminée avec succès !")
