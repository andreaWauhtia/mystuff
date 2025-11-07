# INDEX — Match 2025-09-17 : USAO U8 4-11 Jeunesse MSN Tilleur

## 📍 Localisation

**Dossier principal** : `.memory-bank/competitions/analysis/2025-09-17/`

## 📎 Fichiers d'analyse

### Données Brutes
- **`match_2025-09-17_msn_tilleur_complete.json`** — Source brute extraite des captures d'écran SportEasy
- **`parsed_by_side.csv`** — Événements parsés avec classifications (minute, joueur, type, team, etc.)

### Rapports
- **`2025-09-17_USAO_vs_MSN_Tilleur.md`** — Timeline chronologique complète du match
- **`rapport_analyse_complete.md`** — Analyse synthétique avec métriques, performances individuelles et recommandations

## 🎯 Contenu clé

| Section | Fichier | Détails |
|---------|---------|---------|
| Données brutes | `parsed_by_side.csv` | 23 événements parsés |
| Timeline | `2025-09-17_USAO_vs_MSN_Tilleur.md` | Ordre chronologique complet |
| Analyse offensive | `rapport_analyse_complete.md` | 4 buts / 6 tirs = 66,7% efficacité |
| Analyse défensive | `rapport_analyse_complete.md` | 11 buts concédés / ~14 tirs = 78,6% |
| Performances | `rapport_analyse_complete.md` | Nestor 2 buts, Tiago 1, Nathan 1 |

## 📊 Résumé Exécutif

- **Score final** : 4-11 (défaite)
- **Efficacité USAO** : 66,7% (4 buts / 6 tirs)
- **Top scoreur** : Nestor Arnould (2 buts)
- **Résultat clé** : Défaite due au manque de volume (6 tirs vs 14+ de l'adversaire)

## 🔄 Traçabilité

**Génération du pipeline** :
1. Extraction manuelle → `match_2025-09-17_msn_tilleur_complete.json`
2. Parsing automatique → `parsed_by_side.csv` + `2025-09-17_USAO_vs_MSN_Tilleur.md`
3. Analyse synthétique → `rapport_analyse_complete.md`
4. Archivage → Ce fichier INDEX.md

**Date de génération** : 2025-11-07  
**Script utilisé** : `tools/parse_timeline.py` (détection HOME/AWAY automatique)
