# CRM Data Quality & Campaign Readiness — Dashboard

Projet de validation **Data Visualisation (M2)**.
Domaine : Go-To-Market B2B (Marketing & Sales Operations).

> **Question métier :** le CRM est-il assez fiable pour piloter les campagnes
> marketing, et où faut-il corriger en priorité ?

Le dashboard est réalisé en **Streamlit + Plotly** (4 vues : Direction, Sources,
Campagnes, Actions correctives).

---

## 🚀 Lancer le dashboard

```bash
# 1. (optionnel) créer un environnement
python -m venv .venv && .venv\Scripts\activate    # Windows
# source .venv/bin/activate                         # macOS / Linux

# 2. installer les dépendances
pip install -r requirements.txt

# 3. lancer l'application
streamlit run streamlit_app.py
```

L'application s'ouvre sur <http://localhost:8501>. Utilisez la **barre latérale**
pour filtrer par période, source, canal, statut ou niveau de qualité — tous les
graphiques et KPI se mettent à jour.

> Les données affichées proviennent de `data/processed/`, générées par le
> notebook. Pour les régénérer :
> ```bash
> jupyter nbconvert --to notebook --execute --inplace \
>   crm_data_quality_gtm_bundle_notebook_v2_corrige.ipynb
> ```

---

## 📊 Chiffres clés (base actuelle)

| Indicateur | Valeur |
|---|---|
| Leads analysés | 8 000 |
| Score qualité moyen | 75,3 / 100 |
| Leads campaign-ready | 93,7 % |
| Emails valides | 93,8 % (497 à corriger) |
| Téléphones valides | 14,2 % global · 73,5 % parmi les convertis |
| Doublons exacts | 0 |
| Anomalies recensées | 11 280 |

---

## 📁 Structure du projet

```
.
├── streamlit_app.py                # Dashboard Streamlit (livrable visualisation)
├── crm_data_quality_..._corrige.ipynb  # Notebook d'analyse (audit, nettoyage, scoring)
├── note_methodologique.md          # Note méthodologique
├── presentation_dashboard.pptx     # Diaporama de soutenance (12 slides)
├── presentation_orale.md           # Trame / script de la soutenance
├── guide_tableau.md                # Variante Tableau (optionnelle)
├── requirements.txt
├── .streamlit/config.toml          # Thème de l'application
├── data/
│   ├── raw/                        # CSV bruts (leads, contacts, campaigns, activities)
│   └── processed/                  # Exports nettoyés (alimentent le dashboard)
│       ├── crm_quality_clean.csv
│       ├── crm_quality_issues.csv
│       └── data_dictionary.csv
└── reports/kpi_summary.csv
```

---

## 🧭 Les 4 vues du dashboard

1. **Direction** — fiabilité globale : jauge de score, répartition par niveau de
   qualité, évolution temporelle, top sources.
2. **Sources** — quelles sources produisent les leads les plus fiables (score,
   carte de chaleur des taux, volume vs qualité).
3. **Campagnes** — comparaison des ~174 campagnes (volume, score, ready par canal).
4. **Actions correctives** — anomalies par type/sévérité, détail téléphone, et
   **liste opérationnelle filtrable exportable en CSV**.

Voir `note_methodologique.md` pour la démarche et les choix de modélisation.
