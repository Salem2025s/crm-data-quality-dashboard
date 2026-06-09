# Guide de construction du dashboard — Tableau Public

Dashboard **CRM Data Quality & Campaign Readiness**. Ce guide te permet de
reconstruire le tableau de bord pas à pas dans **Tableau Public** (gratuit) à
partir des fichiers produits par le notebook.

---

## 0. Pré-requis et connexion des données

1. Télécharge et installe **Tableau Public Desktop** (gratuit) :
   <https://public.tableau.com/app/discover>.
2. `Connexion → À un fichier → Fichier texte` et sélectionne
   **`data/processed/crm_quality_clean.csv`**.
   - Vérifie l'encodage **UTF-8** et le séparateur **virgule** dans l'aperçu.
3. Ajoute une 2ᵉ source : `Données → Nouvelle source de données → Fichier texte`
   → **`data/processed/crm_quality_issues.csv`** (pour la page Actions correctives).
   - Ne crée **pas** de relation entre les deux : on les utilise sur des pages
     séparées (sinon Tableau dupliquera les lignes via `lead_id`).

### Conversions de types à vérifier (onglet *Source de données*)
| Champ | Type attendu |
|---|---|
| `lead_created_at`, `lead_converted_at`, `*_activity_date` | Date & heure |
| `quality_score`, `total_activities`, `missing_critical_fields_count` | Nombre (entier) |
| `email_valid`, `phone_valid`, `is_duplicate`, `campaign_ready`, `has_*` | Booléen |
| tous les autres | Chaîne |

### Champs calculés réutilisables (menu *Analyse → Créer un champ calculé*)
```
// Taux campaign-ready (pour les KPI en %)
Taux Campaign Ready = AVG(INT([Campaign Ready]))

// % emails valides
Taux Email Valide = AVG(INT([Email Valid]))

// % téléphones valides
Taux Phone Valide = AVG(INT([Phone Valid]))

// Mois de création (axe temporel)
Mois création = DATETRUNC('month', [Lead Created At])
```
> Formate ces taux en **Pourcentage** (clic droit sur le champ → *Format*).

---

## Page 1 — Vue Direction *(la base est-elle fiable ?)*

**Objectif :** une réponse en un coup d'œil. Tuiles de KPI + 3 graphiques.

**Tuiles KPI** (créer une feuille par indicateur, type *Texte/BAN* — Big Ass Number) :
- Nombre total de leads → `CNTD([Lead Id])` ≈ **8 000**
- Score qualité moyen → `AVG([Quality Score])` ≈ **75,3**
- % campaign-ready → `[Taux Campaign Ready]` ≈ **93,7 %**
- % emails valides → `[Taux Email Valide]` ≈ **93,8 %**
- % téléphones valides → `[Taux Phone Valide]` ≈ **14,2 %**
- Leads critiques → `SUM(IF [Quality Level]="Critique" THEN 1 END)` ≈ **0**

**Graphiques :**
1. **Répartition par `quality_level`** — barres horizontales empilées ou *donut*.
   `Quality Level` en couleur, `CNT(Lead Id)` en taille. Ordonne Excellent →
   Critique. Palette : vert / bleu / orange / rouge.
2. **Évolution de la qualité dans le temps** — courbe : `Mois création` en
   colonnes, `AVG(Quality Score)` en lignes. Ajoute une ligne de référence à 60.
3. **Top sources par score qualité** — barres : `Source Final` en lignes,
   `AVG(Quality Score)` en longueur, trié décroissant.

**Filtres globaux** (à appliquer à tout le dashboard) : `Source Final`,
`Campaign Channel`, `Lead Status Clean`, plage de `Lead Created At`.

---

## Page 2 — Qualité par source marketing *(où investir ?)*

**Objectif :** identifier les sources qui produisent les leads les plus fiables.

- **Tableau à puces / barres** : `Source Final` (lignes) ×
  `AVG(Quality Score)` (barres), trié. Les 10 sources vont de **~73,3**
  (*outbound cold*) à **~76,8** (*partner referral*).
- **Carte de chaleur** : `Source Final` (lignes) × mesures en colonnes
  (`Taux Email Valide`, `Taux Phone Valide`, `Taux Campaign Ready`), couleur =
  valeur. Repère vite les sources faibles.
- **Volume vs qualité** : nuage de points `CNT(Lead Id)` (x) ×
  `AVG(Quality Score)` (y), `Source Final` en couleur → distingue les sources
  *grosses mais fragiles*.

**Décisions outillées :** renforcer les sources fiables, corriger les
formulaires des sources faibles, surveiller celles qui génèrent des emails
invalides.

---

## Page 3 — Qualité par campagne *(quelles campagnes pilotent bien ?)*

**Objectif :** comparer les ~174 campagnes (`campaign_name` renseigné à 97 %).

- **Barres Top N** : `Campaign Name` × `CNT(Lead Id)`, filtre *Top 15 par volume*.
- **Score par campagne** : mêmes campagnes × `AVG(Quality Score)`, couleur =
  `Campaign Channel`.
- **Taux campaign-ready par canal** : `Campaign Channel` × `[Taux Campaign Ready]`.
- **Activités par campagne** : `Campaign Name` × `SUM(Total Activities)`.

> Astuce : ajoute un filtre `N° Top` paramétrable pour basculer Top 10 / 20.

---

## Page 4 — Actions correctives *(quoi corriger d'abord ?)*

**⚠️ Cette page utilise la source `crm_quality_issues.csv`** (11 280 lignes).

- **Problèmes par type** : barres `Issue Type` × `CNT(Lead Id)` trié décroissant.
  Principaux volumes : *Téléphone invalide/manquant* (6 866), *Doublon probable
  nom+entreprise* (3 671), *Email invalide* (497), *Source manquante* (244),
  *Campagne non associée* (236).
- **Problèmes par sévérité** : barres empilées `Severity` (Haute / Moyenne /
  Faible) en couleur (rouge / orange / gris).
- **Détail erreurs téléphone** : barres `Issue Detail` (filtré
  `Field Name = phone`) × `CNT`.
- **Liste opérationnelle filtrable** : tableau `Lead Id`, `Issue Type`,
  `Field Name`, `Severity`, `Recommended Action`, `Issue Detail`, avec filtres
  `Severity` et `Issue Type` → la *to-do list* de l'équipe data.

**Décisions :** corriger les emails invalides avant tout emailing ; enrichir les
téléphones au format E.164 ; vérifier les doublons probables ; compléter les
sources manquantes.

---

## 5. Assemblage du dashboard et storytelling

1. `Tableau de bord → Nouveau` pour chaque page (format *Automatique* ou
   *1366×768*).
2. Glisse les feuilles, ajoute un **titre** et un bandeau de KPI en haut.
3. **Actions de filtre** : `Tableau de bord → Actions → Ajouter une action →
   Filtre` pour que cliquer sur une source/campagne filtre les autres vues.
4. Utilise **« Utiliser comme filtre »** sur les graphiques de répartition.
5. Navigation : ajoute des boutons de page (objet *Navigation*) entre les 4 vues.

### Bonnes pratiques visuelles
- Palette sobre et **sémantique** (vert = bon, rouge = à corriger), cohérente
  partout.
- Une idée par graphique ; titres formulés comme des **réponses**
  (« 93,7 % des leads sont exploitables »).
- Infobulles enrichies (`lead_id`, score, action recommandée).
- Toujours afficher le **dénominateur** d'un pourcentage.

---

## 6. Publication

`Serveur → Tableau Public → Enregistrer dans Tableau Public As…`, connecte ton
compte, publie. Récupère l'URL publique pour la présentation orale et le rendu.

> Alternative 100 % Python : les mêmes 4 vues sont réalisables avec
> `plotly`/`dash` à partir de `crm_quality_clean.csv` si tu préfères livrer un
> dashboard HTML autonome.
