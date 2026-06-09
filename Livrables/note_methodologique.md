# Note méthodologique — Dashboard *CRM Data Quality & Campaign Readiness*

**Projet de validation — Data Visualisation (M2)**
**Domaine d'activité :** Go-To-Market / Marketing & Sales Operations (B2B SaaS)

---

## 1. Question métier et KPI

> **Question :** *Le CRM est-il assez fiable pour piloter les campagnes marketing et la prise de décision commerciale, et où faut-il agir en priorité pour l'améliorer ?*

Un CRM dégradé coûte cher : emails qui rebondissent, prospects injoignables,
attribution marketing faussée, doublons qui polluent les relances. Avant
d'investir en acquisition, l'équipe *RevOps* doit savoir **quelle part de la
base est réellement exploitable** et **quels défauts corriger en premier**.

De cette question découlent les **KPI** suivis dans le dashboard :

| KPI | Définition | Valeur observée |
|---|---|---|
| Score qualité moyen | Score CRM sur 100 (voir §4) | **75,3 / 100** |
| % leads *campaign-ready* | Leads exploitables pour une campagne | **93,7 %** |
| % emails valides | Email au format correct | **93,8 %** (497 à corriger) |
| % téléphones valides | Numéro exploitable (E.164) | **14,2 %** global / **73,5 %** parmi les convertis |
| Doublons exacts | Même email de lead saisi plusieurs fois | **0** |
| Leads critiques | Score < 40 | **0** |
| Problèmes qualité recensés | Lignes du journal d'anomalies | **11 280** |

---

## 2. Jeux de données

Bundle GTM relationnel `astronomer/mini-gtm-data-platform`, 4 tables :

| Table | Lignes | Rôle |
|---|---:|---|
| `leads.csv` | 8 000 | Table principale (prospects) |
| `contacts.csv` | 3 000 | Contacts rattachés aux comptes (porteurs du téléphone) |
| `campaigns.csv` | ~200 | Référentiel des campagnes marketing |
| `lead_activities.csv` | ~25 000 | Interactions (ouverture email, clic, webinaire…) |

**Modèle relationnel réel (point clé)** : `leads` ne possède **ni `contact_id`
ni téléphone**. Le seul lien fiable vers `contacts` est
`leads.converted_account_id` → `contacts.account_id`. Le téléphone n'est donc
disponible **qu'après conversion** d'un lead en compte — ce n'est pas un défaut
de données mais une réalité du cycle de vente, que le dashboard explicite.

---

## 3. Démarche d'analyse (EDA → nettoyage → scoring)

1. **Profilage initial** : volumétrie, taux de valeurs manquantes, doublons
   exacts, types.
2. **Nettoyage table par table** :
   - *emails* : normalisation (minuscules, espaces) + validation regex ;
   - *téléphones* : extraction des chiffres et extensions, conversion `E.164`
     via `phonenumbers` (repli robuste si la librairie est absente), typage des
     erreurs (`trop court`, `trop long`, `manquant`, `indicatif ambigu`…) ;
   - *dates* : parsing tolérant + détection des dates futures incohérentes ;
   - *textes* : clés normalisées (sans accents/casse) pour comparaisons.
3. **Table analytique** : jointures leads + contacts (via `account_id`) +
   campagnes + activités agrégées par lead.
4. **Flags qualité** : complétude, validité email/téléphone, cohérence
   relationnelle, doublons, dates futures.
5. **Score qualité & statut** : note /100, niveau, *campaign-ready*, priorité de
   correction.
6. **Journal des anomalies** : une ligne par problème, avec sévérité et action
   recommandée (table dédiée à la page « Actions correctives »).

---

## 4. Score qualité CRM (sur 100)

| Critère | Points |
|---|---:|
| Email valide | 25 |
| Téléphone valide | 15 |
| Contact exploitable | 10 |
| Source marketing renseignée | 10 |
| Entreprise renseignée | 10 |
| Campagne **ou** activité associée | 10 |
| Date de création valide et non future | 10 |
| Pas de doublon | 10 |

**Niveaux :** Excellent (≥ 80), Correct (≥ 60), À corriger (≥ 40), Critique (< 40).
Le score traduit un diagnostic technique en **indicateur métier** unique.

`campaign_ready` = email valide **ET** non-doublon **ET** source renseignée
**ET** score ≥ 60.

---

## 5. Choix méthodologiques notables (et pourquoi)

- **Téléphone via `account_id`, pas `contact_id`.** Faute de clé directe, on
  enrichit les leads convertis avec le meilleur contact du compte (téléphone
  valide prioritaire). On expose donc le téléphone comme un **attribut de
  compte**, et non du lead.
- **Doublon = email de lead répété, et rien d'autre.** Le couple nom+entreprise
  a été **écarté** du signal dur : avec seulement ~20 entreprises dans le jeu
  synthétique, il marquait quasi toutes les lignes. Il reste calculé
  (`duplicate_company_name`) et affiché comme « doublon probable à vérifier ».
  On a aussi exclu le téléphone du calcul de doublon, car il est partagé par
  construction entre les leads d'un même compte.
- **Honnêteté des KPI.** Un téléphone valide à 14 % global n'est pas masqué :
  on le contextualise par le taux parmi les convertis (73,5 %), ce qui en fait
  une **opportunité d'enrichissement** plutôt qu'un simple constat négatif.

---

## 6. Limites

- Données **synthétiques** : faible diversité d'entreprises, pas de vrais
  doublons exacts — les volumes sont illustratifs.
- L'enrichissement téléphone ne couvre que les comptes convertis présents dans
  `contacts` (736 comptes sur 772).
- Le « doublon probable nom+entreprise » est un signal indicatif nécessitant une
  revue manuelle, pas une fusion automatique.

---

## 7. Livrables

| Livrable | Fichier |
|---|---|
| Notebook d'analyse | `crm_data_quality_gtm_bundle_notebook_v2_corrige.ipynb` |
| **Dashboard de visualisation (Streamlit)** | `streamlit_app.py` (+ `.streamlit/config.toml`) |
| Table propre (source du dashboard) | `data/processed/crm_quality_clean.csv` |
| Journal d'anomalies | `data/processed/crm_quality_issues.csv` |
| Dictionnaire de données | `data/processed/data_dictionary.csv` |
| Synthèse KPI | `reports/kpi_summary.csv` |
| Guide d'exécution | `README.md` |
| Variante Tableau (optionnelle) | `guide_tableau.md` |
| Note méthodologique | `note_methodologique.md` (ce document) |
| Diaporama de soutenance | `presentation_dashboard.pptx` (12 slides) |
| Trame / script de l'oral | `presentation_orale.md` |

> **Outil de visualisation :** le dashboard est livré en **Streamlit + Plotly**
> (`streamlit run streamlit_app.py`). Quatre vues interactives — Direction,
> Sources, Campagnes, Actions correctives — avec filtres globaux (période,
> source, canal, statut, niveau de qualité) et export CSV de la liste de
> corrections.
