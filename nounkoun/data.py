# -*- coding: utf-8 -*-
"""
data.py — Base de connaissances Nounkoun (fusion des versions v1 à v4)

Toutes les données agricoles vivent ICI, séparées de la logique (matcher.py,
intents.py, responder.py). C'est ce qui permet de grossir jusqu'à v8+ sans
dupliquer du code : pour ajouter une culture, on ajoute une entrée ici, rien
d'autre à toucher.

Chaque culture suit le même schéma (les clés absentes sont simplement
ignorées par le reste du programme) :

{
    "noms": {"francais": ..., "fon": ..., "yoruba": ..., "bariba": ..., "dendi": ...},
    "alias": [...],                # synonymes / variantes d'écriture
    "categorie": "cereale" | "tubercule" | "rente" | ...,
    "cycle": "...",
    "saison": "...",
    "zone": "...",
    "resistance": "...",
    "importance": "...",
    "varietes": {nom: {"fon": ..., "caractere": ..., "zone": ...}},
    "problemes": {nom_probleme: "description / symptôme"},
    "solutions_naturelles": {nom_solution: "recette / dose / usage"},
    "prix_marche": {lieu: "prix"},
    "calendrier_lunaire": {"plantation": ..., "dicton": ..., "interdit": ..., "recolte": ...},
    "recettes_post_recolte": {nom_recette: "procédé"},
}
"""

CULTURES = {

    # ------------------------------------------------------------- CÉRÉALES
    "mais": {
        "noms": {"francais": "Maïs", "fon": "Gbadé", "yoruba": "Agbado",
                 "bariba": "Kparika", "dendi": "Hamo"},
        "alias": ["cereale", "blé de guinée", "maïs jaune", "maïs blanc"],
        "categorie": "cereale",
        "cycle": "90-120 jours",
        "saison": "1ère saison avril-juin (Sud), 2ème saison sept-oct. Nord : mai-août",
        "zone": "Tout le Bénin — 31,3% des terres arables",
        "problemes": {
            "chenille légionnaire": "Feuilles trouées, cœur de la plante mangé",
            "striga": "Plante parasite, maïs jaune et chétif",
            "sécheresse": "Feuilles enroulées, épis vides",
        },
        "solutions_naturelles": {
            "purin de neem": "1L de purin + 10L d'eau, pulvériser le soir 2x/semaine",
            "cendre": "1 poignée au pied, tous les 15 jours",
            "association niébé": "Semer du niébé entre les lignes, repousse la chenille",
        },
        "calendrier_lunaire": {
            "plantation": "Lidosun (mars) pour la 1ère saison, Zosun (sept) pour la 2ème",
        },
    },

    "sorgho": {
        "noms": {"francais": "Sorgho", "fon": "Abla", "yoruba": "Okababa",
                 "bariba": "Yerumaru", "dendi": "Hamo bii"},
        "alias": ["mil rouge", "gros mil", "sorghum"],
        "categorie": "cereale",
        "zone": "8,7% des terres arables — Nord (Kandi, Banikoara)",
        "resistance": "Sols pauvres, résiste avec seulement 400 mm de pluie/an",
    },

    "mil": {
        "noms": {"francais": "Mil", "fon": "Likoun", "yoruba": "Okaka",
                 "bariba": "Gawri", "dendi": "Hamo"},
        "alias": ["petit mil", "mil chandelle"],
        "categorie": "cereale",
        "zone": "2,1% des terres arables — extrême Nord, zone sahélienne",
        "resistance": "200-600 mm de pluie/an",
    },

    "riz": {
        "noms": {"francais": "Riz", "fon": "Mɔlu", "yoruba": "Iresi",
                 "bariba": "Shinkafa", "dendi": "Mo"},
        "categorie": "cereale",
        "cycle": "120-150 jours",
        "zone": "0,9% des terres arables — bas-fonds (Malanville, vallée de l'Ouémé)",
        "problemes": {
            "pyriculariose": "Taches brunes sur les feuilles",
            "oiseaux": "Mangent les grains au stade laiteux",
            "inondation": "Risque en bas-fond mal drainé",
        },
        "solutions_naturelles": {
            "repiquage précoce": "Repiquer avant 21 jours",
            "épouvantails": "Sacs plastique qui bougent au vent",
            "digues": "Contrôler l'inondation",
        },
    },

    # -------------------------------------------------------- CULTURES DE RENTE
    "coton": {
        "noms": {"francais": "Coton", "fon": "Koton", "yoruba": "Owu",
                 "bariba": "Koton", "dendi": "Koton"},
        "alias": ["or blanc"],
        "categorie": "rente",
        "importance": "80% des recettes d'export du Bénin, fait vivre environ 2 millions "
                      "de personnes. Zone : Nord (Kandi, Banikoara)",
        "problemes": {
            "chenille Helicoverpa": "Capsules percées",
            "puceron": "Feuilles recroquevillées",
            "jasside": "Feuilles jaunes en bordure",
            "cours mondiaux bas": "Pression économique sur les producteurs",
        },
        "solutions_naturelles": {
            "purin de neem renforcé": "2kg de feuilles de neem + 10L d'eau, fermenter 5 jours. "
                                       "Appliquer 1,5L de purin + 15L d'eau tous les 7 jours dès "
                                       "la floraison (45e au 90e jour après semis)",
            "ail + piment": "200g d'ail + 200g de piment + 10L d'eau, macérer 24h, filtrer et pulvériser",
            "tourteau de neem": "100 kg/ha au sol avant semis",
            "rotation maïs-soja": "Casse le cycle des ravageurs",
        },
        "attention": "Ne jamais traiter en plein soleil — toujours entre 17h et 18h",
    },

    "anacarde": {
        "noms": {"francais": "Anacarde", "fon": "Kajou", "yoruba": "Kaju", "bariba": "Kaju"},
        "alias": ["cajou", "pomme cajou"],
        "categorie": "rente",
        "zone": "Centre-Nord (Djougou, Bassila)",
        "importance": "Culture de rente en pleine diversification",
        "problemes": {"anthracnose": "Taches sur le fruit"},
    },

    "palmier": {
        "noms": {"francais": "Palmier à huile", "fon": "Dètin", "yoruba": "Ope", "bariba": "Dè"},
        "alias": ["huile de palme"],
        "categorie": "rente",
        "zone": "Sud (Porto-Novo, Pobè) — 8% des terres",
        "importance": "Culture de rente principale du Sud",
    },

    "ananas": {
        "noms": {"francais": "Ananas"},
        "categorie": "rente",
        "zone": "Sud (Atlantique)",
        "importance": "Culture d'export, diversification",
    },

    # ------------------------------------------------------------ TUBERCULES
    "igname": {
        "noms": {"francais": "Igname", "fon": "Tè", "yoruba": "Isu",
                 "bariba": "Yam", "dendi": "Donyi"},
        "categorie": "tubercule",
        "cycle": "8-10 mois",
        "zone": "7,7% des terres arables — Centre-Nord (Zè, Allada, Savalou, Djougou)",
        "varietes": {
            "tè sin": {"caractere": "Igname d'eau, gros tubercule, chair blanche", "zone": "Zè, Allada, Toffo"},
            "tè afan": {"caractere": "Igname ailée, résiste à la sécheresse", "zone": "Savalou, Dassa, Glazoué"},
            "tè vɔvɔ": {"caractere": "Igname jaune, riche en carotène (vitamine A)", "zone": "Collines, Djougou"},
        },
        "problemes": {
            "cochenille": "Insectes blancs sur le tubercule stocké",
            "anthracnose": "Taches noires sur les feuilles, tubercule qui pourrit",
            "nématodes": "Tubercules déformés, gales",
        },
        "solutions_naturelles": {
            "cendre + piment": "500g de cendre + 100g de piment pilé, dans le trou avant plantation",
            "buttage": "Monter la terre au pied : 1er buttage à 30 jours, 2e à 90 jours, 3e à 150 jours "
                       "après semis, hauteur 30 cm",
            "paillage": "Couvrir le sol de feuilles sèches pour garder l'humidité",
            "neem au grenier": "Branches de neem sèches dans le grenier, repousse les insectes 6 mois",
        },
        "prix_marche": {
            "Dantokpa": "1 tas de 3 gros tubercules : 2000-3500 FCFA selon saison",
            "Parakou": "Sac de 100kg : 25 000-40 000 FCFA",
            "Malanville": "Export Nigeria, 1 tas : 1500-2500 FCFA",
            "soudure (mars-mai)": "Prix x2",
            "récolte (déc-jan)": "Prix bas",
        },
        "recettes_post_recolte": {
            "igname pilée": "Bouillir 30 min, piler au mortier, servir avec sauce",
            "cossettes": "Éplucher, couper, sécher au soleil 7 jours — se conserve 2 ans",
            "foufou": "Cossettes + eau chaude, tourner — avec sauce arachide",
            "conservation": "Grenier aéré sur claie, cendre entre les couches contre le charançon",
        },
        "calendrier_lunaire": {
            "plantation": "Lune montante de Lidosun (mars-avril), 3 jours après la nouvelle lune",
            "interdit": "Ne jamais planter en lune descendante d'Ayidosun (mai) — le tubercule pourrit",
        },
    },

    "manioc": {
        "noms": {"francais": "Manioc", "fon": "Agbeli", "yoruba": "Ege",
                 "bariba": "Bankye", "dendi": "Roogo"},
        "alias": ["tapioca", "gari"],
        "categorie": "tubercule",
        "cycle": "12-18 mois (variétés précoces : 6-8 mois)",
        "zone": "10,7% des terres arables — Sud-Centre (Allada, Pobè, Kétou, Abomey)",
        "varietes": {
            "agbeli vivɛ": {"caractere": "Doux, peu toxique, se mange bouilli"},
            "agbeli vɛvɛ": {"caractere": "Amer, 90% de la production, destiné au gari — "
                                          "contient du cyanure, trempage obligatoire avant consommation"},
            "TMS 92/0326": {"caractere": "Variété précoce, récolte en 6-8 mois"},
        },
        "problemes": {
            "mosaïque": "Feuilles jaunes marbrées (virus transmis par la mouche blanche)",
            "cochenille farineuse": "Insectes blancs qui sucent la sève",
            "pourriture des racines": "Sol trop humide",
        },
        "solutions_naturelles": {
            "boutures saines": "Prendre des tiges de 20 cm au milieu d'un plant sain, 5 nœuds",
            "cendre": "1 poignée/plant contre la cochenille, 1x/semaine",
            "association maïs/haricot": "Entre les lignes, gêne la mouche blanche",
            "rotation": "Ne pas remettre du manioc au même endroit avant 3 ans",
        },
        "prix_marche": {
            "Dantokpa (gari)": "Sac de 100kg : 15 000-25 000 FCFA",
            "Parakou (tubercules)": "Bâchée tricycle : 30 000-45 000 FCFA",
            "Pobè (tapioca)": "Sac de 50kg : 12 000-18 000 FCFA",
        },
        "recettes_post_recolte": {
            "gari": "Râper, presser 2 jours, tamiser, griller — rendement ~25kg gari/100kg de manioc frais",
            "tapioca": "Amidon décanté puis séché, cuisson à l'eau bouillante",
            "lafun": "Fermenter 4 jours, sécher, piler — farine blanche",
            "atchèkè": "Manioc fermenté râpé, cuit à la vapeur",
            "conservation": "Le tubercule frais ne tient que 2 semaines en terre, sinon transformer directement",
        },
        "calendrier_lunaire": {
            "plantation": "Lune descendante d'Ayidosun (mai-juin) — la bouture prend mieux",
        },
    },

    "patate_douce": {
        "noms": {"francais": "Patate douce", "fon": "Patat", "yoruba": "Odunkun", "bariba": "Dankali"},
        "alias": ["patate"],
        "categorie": "tubercule",
        "cycle": "3-5 mois",
        "zone": "Tout le Bénin, surtout Nord (nutrition)",
        "varietes": {
            "chair orange": {"caractere": "Riche en vitamine A", "zone": "Atacora, Donga"},
            "chair blanche": {"caractere": "Traditionnelle, farineuse"},
            "chair violette": {"caractere": "Antioxydants, marché urbain"},
        },
        "problemes": {
            "charançon": "Larves dans le tubercule",
            "virus": "Feuilles recroquevillées",
        },
        "solutions_naturelles": {
            "rotation": "Ne pas remettre 2 ans au même endroit",
            "boutures saines": "Prendre seulement la tête de la vigne",
        },
        "prix_marche": {
            "Dantokpa": "Tas de 5 tubercules : 500-1000 FCFA",
            "Natitingou": "Sac de 50kg : 8000-12 000 FCFA en saison pluvieuse",
        },
        "recettes_post_recolte": {
            "bouillie": "Bouillir 15 min, saler",
            "frite": "Couper en bâtons, frire",
            "farine": "Sécher en tranches puis moudre",
            "conservation": "Endroit sec et aéré, 3 mois — pas de frigo",
        },
    },

    "taro": {
        "noms": {"francais": "Taro", "fon": "Glazoui", "yoruba": "Koko", "bariba": "Koko"},
        "categorie": "tubercule",
        "cycle": "8-12 mois",
        "zone": "Bas-fonds — vallée de l'Ouémé, Mono, Zou",
        "problemes": {
            "mildiou": "Feuilles brûlées en saison des pluies",
            "pourriture": "Excès d'eau",
        },
        "solutions_naturelles": {
            "drainage": "Planches surélevées de 30 cm",
            "décoction de prêle": "Pulvériser contre le mildiou",
        },
        "prix_marche": {
            "Porto-Novo": "Tas de 4 gros : 1000-1500 FCFA",
            "Lokossa": "Sac de 50kg : 18 000-25 000 FCFA",
        },
        "recettes_post_recolte": {
            "sauce feuilles": "Feuilles de taro + pâte d'arachide + poisson",
            "tubercule bouilli": "Éplucher, bouillir 40 min, servir à l'huile rouge",
            "conservation": "Laisser en terre, récolter au fur et à mesure — jusqu'à 6 mois",
        },
    },

    "pomme_de_terre": {
        "noms": {"francais": "Pomme de terre", "fon": "Ablatata", "yoruba": "Potato"},
        "categorie": "tubercule",
        "cycle": "90-120 jours",
        "zone": "Atacora (Djougou, Natitingou), saison sèche irriguée",
        "problemes": {
            "mildiou": "Taches noires, tue la plante en 3 jours",
            "doryphore": "Insecte rayé qui mange les feuilles",
        },
        "solutions_naturelles": {
            "bouillie bordelaise": "20g de sulfate de cuivre + 20g de chaux + 1L d'eau, en préventif",
            "purin d'ortie": "Fortifie la plante",
            "rotation": "4 ans sans pomme de terre/tomate/aubergine au même endroit",
        },
        "prix_marche": {
            "Dantokpa": "Kg : 600-1000 FCFA (80% importé)",
            "Djougou (local)": "Kg : 400-600 FCFA en déc-fév",
        },
        "recettes_post_recolte": {
            "frite": "Base des friteries de Cotonou",
            "purée": "Bouillir, écraser, ajouter du lait",
            "conservation": "Chambre froide à 4°C, 3 mois — sinon germe vite",
        },
    },

    "souchet": {
        "noms": {"francais": "Souchet", "fon": "Afio", "yoruba": "Imumu",
                 "bariba": "Tchiya", "haoussa": "Aya"},
        "categorie": "tubercule",
        "cycle": "3-4 mois",
        "zone": "Nord (Malanville, Karimama), sols sableux",
        "usage": "Se mange cru, en jus, ou en farine — très nutritif",
        "solutions_naturelles": {
            "cendre": "Contre les termites",
            "rotation après mil": "Le souchet profite des résidus du mil",
        },
        "prix_marche": {
            "Malanville": "1 kg : 800-1200 FCFA",
            "Cotonou (export)": "1 kg : 1500-2500 FCFA",
        },
        "recettes_post_recolte": {
            "jus": "Tremper 12h, mixer, filtrer, sucrer — lait végétal",
            "farine": "Sécher puis moudre — pâtisserie sans gluten",
            "conservation": "2 ans si bien séché",
        },
    },

    "macabo": {
        "noms": {"francais": "Macabo", "fon": "Makabo", "yoruba": "Ikoko"},
        "categorie": "tubercule",
        "cycle": "10-12 mois",
        "zone": "Sud-Est (Pobè, Kétou), terre humide",
        "problemes": {"mildiou": "Comme le taro", "pourriture": "Excès d'eau"},
        "prix_marche": {"Pobè": "Tas de 3 : 1000-1500 FCFA"},
        "recettes_post_recolte": {
            "foufou de macabo": "Bouillir puis piler, collant comme l'igname",
            "ragoût": "Couper en dés, sauce tomate",
        },
    },

    "coleus": {
        "noms": {"francais": "Pomme de terre Hausa", "fon": "Dokouin", "bariba": "Gbere"},
        "categorie": "tubercule",
        "cycle": "5-6 mois",
        "zone": "Atacora, zones de collines",
        "importance": "Culture de soudure, très rustique, résiste à la famine",
        "prix_marche": {"Natitingou": "Petit marché local, tas : 500 FCFA (culture en déclin)"},
        "recettes_post_recolte": {"bouilli": "Goût de haricot, servi en sauce"},
    },
}


# --------------------------------------------------------------------- SOLS
SOLS = {
    "terre de barre": {
        "def": "Sol rouge du Sud Bénin, acide et pauvre",
        "zone": "Atlantique, Ouémé, Plateau",
        "correction": "5 tonnes/ha de fumier + 500 kg/ha de chaux tous les 2 ans",
    },
    "sol ferrugineux": {
        "def": "Sableux et lessivé",
        "zone": "Centre-Nord",
        "correction": "Paillage obligatoire",
    },
    "bas-fond": {
        "def": "Terre basse inondée en saison des pluies",
        "culture": "Riz, maraîchage de contre-saison",
        "risque": "Noyade en cas de forte pluie",
    },
    "sol hydromorphe": {
        "def": "Vallée de l'Ouémé, très fertile si drainé",
    },
}

# --------------------------------------------------------------- TECHNIQUES
TECHNIQUES = {
    "agroécologie": {
        "def": "Applique les principes écologiques et sociaux à des systèmes agricoles durables",
        "exemples": ["association maïs-niébé", "zaï", "agroforesterie"],
    },
    "agroforesterie": {
        "def": "Associer arbres et cultures/animaux sur la même parcelle",
        "arbres_benin": ["karité", "néré", "baobab", "acacia"],
        "avantage": "Restaure la fertilité du sol",
    },
    "agriculture de conservation": {
        "def": "Agriculture qui protège et conserve les sols",
        "principes": ["couverture permanente", "non-labour", "rotation"],
    },
    "zaï": {
        "def": "Trou de 20 cm + poignée de compost, pour capter l'eau",
        "origine": "Technique du Burkina Faso, adaptée au Nord Bénin",
        "usage": "Mil, sorgho, maïs en zone à 200-600 mm de pluie",
        "dose": "10 000 trous/ha, 2 tonnes de compost/ha",
    },
    "buttage": {
        "def": "Monter la terre au pied de la plante",
        "usage": "Igname, maïs, manioc — 3 fois pendant le cycle",
    },
}

# ----------------------------------------------------------------- INTRANTS
INTRANTS = {
    "purin de neem": {
        "recette": "1 kg de feuilles de neem + 10L d'eau, fermenter 3 jours",
        "usage": "Insecticide — 1L de purin pour 10L d'eau, pulvériser le soir",
        "cible": ["chenille", "puceron", "aleurode"],
    },
    "cendre": {
        "usage": "Anti-limace, apport de potasse — 1 poignée par pied",
        "attention": "Ne pas utiliser sur un sol déjà basique",
    },
    "compost": {
        "recette": "Déchets de cuisine + feuilles sèches + fumier, laisser 3 mois",
        "dose": "2-3 tonnes/ha",
    },
}

# --------------------------------------------------------- GLOSSAIRE PAYSAN
GLOSSAIRE_PAYSAN = {
    "advesture": "Récolte sur pied, surtout pour les céréales",
    "août": "Moisson (aoûter = faire la moisson)",
    "cahot": "Petite meule de 10 gerbes laissée au champ en attendant le charroi",
    "dépouille": "Récolte",
}

# ------------------------------------------------- SIGNES VISUELS (diagnostic)
# Mots-clés qu'un paysan peut utiliser pour DÉCRIRE ce qu'il voit sur sa
# plante (pas de vraie vision par ordinateur ici — voir diagnostic.py pour
# l'explication de ce choix). Complète les "problemes" déjà présents dans
# CULTURES avec des synonymes/descriptions supplémentaires par maladie.
SIGNES_VISUELS = {
    "mais": {
        "chenille légionnaire": ["trous feuilles", "trou dans le coeur", "sciure", "chenille"],
        "striga": ["fleur violette a la base", "mais jaune et chetif", "plante parasite"],
        "charbon": ["poudre noire", "epis noirs"],
    },
    "manioc": {
        "mosaïque": ["feuilles jaunes marbrees", "feuilles deformees", "marbre jaune"],
        "cochenille farineuse": ["insectes blancs sous les feuilles", "substance collante", "moisissure noire"],
        "bactériose": ["taches huileuses", "feuilles qui fanent"],
    },
    "igname": {
        "anthracnose": ["taches noires feuilles", "halo jaune", "feuille seche"],
        "cochenille": ["insectes blancs", "masse cotonneuse", "aspect cireux"],
        "nématodes": ["boules sur le tubercule", "tubercule deforme"],
    },
}


# ---------------------------------------------------------- CALENDRIER FON
CALENDRIER_LUNAIRE_FON = {
    "Lidosun":        {"mois": "Mars",     "activite": "Plantation igname, patate, maïs 1ère saison"},
    "Kudosun":        {"mois": "Avril",    "activite": "Suite plantation, 1er buttage igname"},
    "Ayidosun":       {"mois": "Mai",      "activite": "Plantation manioc, coton"},
    "Ayidosun_kple":  {"mois": "Juin",     "activite": "Sarclage, 2e buttage — pas de plantation"},
    "Yakwesun":       {"mois": "Juillet",  "activite": "Entretien, surveillance des chenilles"},
    "Avuvɔsun":       {"mois": "Août",     "activite": "Récolte maïs précoce, 2e saison maïs (Sud)"},
    "Zosun":          {"mois": "Septembre","activite": "Récolte souchet, arachide, plantation maïs 2e saison"},
    "Abɔxwisun":      {"mois": "Octobre",  "activite": "Plantation taro, récolte igname précoce"},
    "Woo_sun":        {"mois": "Novembre", "activite": "Récolte igname en masse, patate"},
    "Woo_sun_kple":   {"mois": "Décembre", "activite": "Récolte manioc, stockage en grenier"},
    "Kɔnyasun":       {"mois": "Janvier",  "activite": "Préparation des champs, brûlis contrôlé"},
    "Kɔnyasun_kple":  {"mois": "Février",  "activite": "Repos de la terre, réparation des outils"},
}
