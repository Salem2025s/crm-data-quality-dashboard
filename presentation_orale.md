# Présentation orale — trame (≈ 10–12 min + démo)

Dashboard **CRM Data Quality & Campaign Readiness**
*Data Visualisation — Projet de validation M2*

---

### Slide 1 — Titre
- Titre du projet, votre nom, date.
- Une phrase d'accroche : *« Peut-on faire confiance à notre CRM pour piloter le marketing ? »*

### Slide 2 — Contexte & domaine
- Domaine : **Go-To-Market B2B** (Marketing & Sales Operations).
- Le problème : un CRM dégradé = emails qui rebondissent, prospects injoignables,
  attribution faussée, budget gaspillé.
- L'élément à surveiller : **la qualité et l'exploitabilité de la base leads**.

### Slide 3 — Question métier & KPI
- Question : *Le CRM est-il assez fiable pour piloter campagnes et décisions, et
  où agir en priorité ?*
- Les 6 KPI : score qualité, % campaign-ready, % email valide, % téléphone valide,
  doublons, problèmes à corriger.

### Slide 4 — Données & modèle
- 4 tables (leads, contacts, campagnes, activités), 8 000 leads.
- **Le point subtil :** les leads n'ont pas de téléphone ; on l'enrichit via
  `converted_account_id → account_id`. Le téléphone n'existe **qu'après
  conversion**. (Montre le schéma relationnel.)

### Slide 5 — Démarche (EDA → nettoyage → scoring)
- Profilage → nettoyage (emails, téléphones E.164, dates) → table analytique →
  flags qualité → **score /100** → journal d'anomalies.
- Insister : la donnée brute a été **auditée puis transformée**, pas juste tracée.

### Slide 6 — Le score qualité (le cœur méthodo)
- Grille de points (email 25, téléphone 15, …).
- Traduit un diagnostic technique en **indicateur métier unique** et en niveaux
  (Excellent / Correct / À corriger / Critique).

### Slide 7 — DÉMO du dashboard Streamlit (le moment fort)
Lancer `streamlit run streamlit_app.py` et dérouler les 4 onglets en racontant
une histoire (montrer un filtre live, ex. source ou période) :
1. **Direction** : « 93,7 % de la base est exploitable, score moyen 75/100. »
2. **Sources** : « *partner referral* et *event* sont les plus fiables ;
   *outbound cold* traîne. »
3. **Campagnes** : « voici les campagnes à fort volume mais qualité moyenne. »
4. **Actions correctives** : « la priorité n°1 = enrichir les téléphones
   (6 866 cas), puis corriger 497 emails invalides. »

### Slide 8 — Décisions actionnables
- Investir sur les sources fiables, corriger les formulaires des sources faibles.
- Lancer une campagne d'enrichissement téléphone (E.164).
- Nettoyer les 497 emails avant tout emailing.
- Revue manuelle des doublons probables nom+entreprise.

### Slide 9 — Rigueur & honnêteté de l'analyse
- Mentionner les **3 bugs de pipeline corrigés** (doublons à 100 %, téléphone à
  0 %, jointure campagnes vide) → montre l'esprit critique sur ses propres KPI.
- Limites : données synthétiques, peu d'entreprises, pas de vrais doublons exacts.

### Slide 10 — Conclusion
- Réponse à la question : *oui, le CRM est globalement fiable (75/100), mais le
  téléphone est le chantier prioritaire.*
- Valeur : un outil de **surveillance continue** + une **to-do list** pour
  l'équipe data.

---

## Conseils de soutenance
- **Temps :** ~1 min/slide, gardez ~4 min pour la démo live et 2 min de questions.
- **Commencez par la question métier**, pas par la technique.
- **Chaque visuel = une phrase-réponse**, pas une description de graphique.
- Anticipez les questions :
  - *« Pourquoi 14 % de téléphones seulement ? »* → structurel : enrichi après
    conversion (73 % chez les convertis).
  - *« Pourquoi 0 doublon ? »* → 0 **exact** (email) ; les doublons probables
    nom+entreprise sont signalés pour revue.
  - *« Le score est-il arbitraire ? »* → pondération assumée et documentée dans
    la note méthodologique, ajustable.
- Terminez sur **l'action**, pas sur le chiffre.

## Checklist de rendu (avant l'oral)
- [ ] Notebook exécuté de bout en bout, sans erreur.
- [ ] 4 CSV présents dans `data/processed/` + `reports/kpi_summary.csv`.
- [ ] Dashboard Streamlit lancé et testé (`streamlit run streamlit_app.py`).
- [ ] `note_methodologique.md` relue.
- [ ] Slides exportées en PDF.
