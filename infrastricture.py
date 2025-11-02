class Infrastructure:
    def __init__(self, id_infra, type_infra, longueur=0, nb_maisons=1):
        self.id = id_infra
        self.type = type_infra
        self.longueur = longueur
        self.nb_maisons = nb_maisons
        self.difficulte = self.calculer_difficulte()

    def calculer_difficulte(self):
        """Formule : difficulté = longueur / nb_maisons"""
        if self.nb_maisons == 0:
            return float('inf')
        return self.longueur / self.nb_maisons

    def cout_par_m(self):
        """Retourne le coût selon le type"""
        couts = {"aerien": 500, "semi-aerien": 750, "fourreau": 900}
        return couts.get(self.type.lower(), 0)

    def duree_par_m(self):
        """Retourne la durée selon le type"""
        durees = {"aerien": 2, "semi-aerien": 4, "fourreau": 5}
        return durees.get(self.type.lower(), 0)

    def __repr__(self):
        return f"<Infra {self.id} ({self.type}) - {self.longueur}m>"
