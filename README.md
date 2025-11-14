# Coach Assistant

Un assistant numérique pour les entraîneurs de football, spécialisé dans l'analyse des matchs et la gestion des entraînements pour l'équipe USAO U8.

## Description

Ce projet fournit des outils automatisés pour analyser les performances des équipes de football, calculer des métriques de momentum, parser les timelines de matchs depuis SportEasy, et gérer les rapports d'entraînements et les profils de joueurs.

## Fonctionnalités

### Analyse de Matchs
- **Parseur de Timeline** : Convertit les données de timeline SportEasy en événements structurés
- **Calcul de Métriques** : Efficacité offensive/défensive, tirs, buts
- **Analyse de Momentum** : Calcule le momentum basé sur les tirs pour/contre sur des intervalles de temps
- **Rapports Automatisés** : Génération de rapports Markdown avec statistiques détaillées

### Gestion des Entraînements
- **Plans d'Entraînement** : Organisation et suivi des séances
- **Évaluations de Drills** : Validation et notation des exercices
- **Rapports d'Entraînement** : Synthèse des performances par équipe

### Gestion des Joueurs
- **Profils de Joueurs** : Analyse individuelle des performances
- **Roster** : Gestion de l'effectif de l'équipe

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/andreaWauhtia/coach-assistant.git
cd coach-assistant
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Pour l'analyse de momentum (optionnel) :
```bash
pip install pandas matplotlib openpyxl
```

## Utilisation

### Parser une Timeline de Match

```bash
python tools/parse_timeline.py --input example_timeline.json --out-dir completed-tasks/competitions/match_reports/
```

Ou en mode interactif :
```bash
python tools/parse_timeline.py --interactive
```

### Analyser un Match

```bash
python tools/analyze_match.py
```

### Calculer le Momentum

```bash
python main.py
```

## Structure du Projet

```
coach-assistant/
├── main.py                    # Script principal pour l'analyse de momentum
├── tools/
│   ├── analyze_match.py       # Analyse complète d'un match
│   └── parse_timeline.py      # Parseur de timeline SportEasy
├── completed-tasks/
│   ├── competitions/
│   │   └── match_reports/     # Rapports de matchs
│   ├── player_reports/        # Profils de joueurs
│   ├── roster/                # Effectif de l'équipe
│   └── trainings/             # Entraînements (drills, plans, rapports)
├── requirements.txt           # Dépendances Python
├── CHANGES.md                 # Historique des changements
└── README.md                  # Ce fichier
```

## Formats de Données

### Timeline JSON
```json
{
  "match_header": "Équipe A 2-3 Équipe B 2025/2026",
  "our_team": "Équipe B",
  "events": [
    {
      "minute": 15,
      "type": "But",
      "player": "Joueur 1",
      "side": "left"
    }
  ]
}
```

### Momentum Excel
Fichier Excel avec colonnes pour les intervalles de temps (0-5, 5-10, etc.) et forces (L, M, H).

## Contribution

Les contributions sont les bienvenues ! Veuillez créer une issue pour discuter des changements majeurs.

## Licence

Ce projet est sous licence MIT.