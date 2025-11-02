class Batiment:
    def __init__(self, id_batiment, type_batiment, nb_maisons):
        self.id = id_batiment
        self.type = type_batiment
        self.nb_maisons = nb_maisons
        self.infrastructures = []  # liste des infrastructures qui le relient
        self.difficulte = 0        # sera calculée plus tard

    def ajouter_infrastructure(self, infra):
        """Associe une infrastructure à ce bâtiment"""
        self.infrastructures.append(infra)

    def calculer_difficulte(self):
        """Somme des difficultés des infrastructures associées"""
        if not self.infrastructures:
            self.difficulte = float('inf')  # pas de connexion possible
        else:
            self.difficulte = sum(infra.difficulte for infra in self.infrastructures)

    def __repr__(self):
        return f"<Batiment {self.id} ({self.type}) - {self.nb_maisons} maisons>"
