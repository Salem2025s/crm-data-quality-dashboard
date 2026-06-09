# Discours oral — soutenance (≈ 11 min + démo)

> Script à dire à voix haute, slide par slide. Le texte est rédigé pour être
> parlé : phrases courtes, ton posé. Les **[indications]** ne se disent pas.
> Adapte « je » / « nous » selon que tu présentes seul ou à deux.

---

## Slide 1 — Titre  *(≈ 30 s)*

« Bonjour à toutes et à tous. Je vais vous présenter mon projet de data
visualisation, intitulé *CRM Data Quality and Campaign Readiness*.

L'idée de départ tient en une question simple, mais que beaucoup d'équipes
marketing se posent rarement : **est-ce qu'on peut vraiment faire confiance aux
données de notre CRM pour lancer nos campagnes ?** C'est à cette question que mon
tableau de bord répond. »

**[Transition]** « Commençons par le contexte. »

---

## Slide 2 — Contexte  *(≈ 1 min)*

« Je me place dans un domaine très concret : le **Go-To-Market en B2B**,
c'est-à-dire les équipes marketing et commerciales qui génèrent et traitent des
prospects — ce qu'on appelle des *leads*.

Le problème, c'est qu'un CRM dégradé coûte cher, et souvent sans qu'on s'en
rende compte. Des emails invalides, et la campagne d'emailing rebondit. Des
téléphones manquants, et les commerciaux n'arrivent pas à joindre les prospects.
Des sources mal renseignées, et on devient incapable de savoir quelles campagnes
fonctionnent. Et au final, on prend des décisions sur des données fausses ou en
double.

L'élément que j'ai choisi de surveiller, c'est donc **la fiabilité et
l'exploitabilité de la base de leads**. Et toute ma démarche tourne autour de
cette question, affichée à droite : *le CRM est-il assez fiable pour piloter les
campagnes, et où faut-il corriger en priorité ?* »

---

## Slide 3 — Les KPI  *(≈ 1 min)*

« Pour répondre, j'ai défini six indicateurs clés, que vous retrouverez en haut
du dashboard.

D'abord le **volume** : 8 000 leads analysés. Ensuite un **score de qualité
moyen** sur 100, qui est à 75 — j'expliquerai comment il est construit. Le
troisième est le plus parlant pour le métier : le pourcentage de leads
*campaign-ready*, c'est-à-dire réellement exploitables — on est à près de 94 %.
Viennent ensuite le taux d'emails valides, le taux de téléphones valides, et
enfin le nombre d'anomalies à corriger : un peu plus de 11 000.

L'intérêt de ces KPI, c'est qu'ils traduisent un diagnostic technique en une
information de pilotage : combien de la base est utilisable, et qu'est-ce qui
bloque. »

---

## Slide 4 — Données & modèle  *(≈ 1 min 15)*

« Côté données, je m'appuie sur un jeu de données relationnel issu d'une
plateforme GTM open source. Quatre tables : les **leads**, 8 000 lignes, c'est ma
table principale ; les **contacts**, 3 000 lignes, rattachés aux comptes ; les
**campagnes** ; et les **activités**, environ 25 000 interactions comme des
ouvertures d'email ou des participations à un webinaire.

Et ici, je veux insister sur un point — l'encadré jaune à droite — parce que
c'est ce qui m'a demandé le plus de réflexion. Les leads **ne contiennent ni
identifiant de contact, ni numéro de téléphone**. Le seul lien fiable vers la
table des contacts passe par le compte, via le champ `converted_account_id`.
Concrètement, ça veut dire que **le téléphone n'apparaît qu'une fois le lead
converti en compte**. Ce n'est pas un défaut de mes données : c'est tout
simplement le reflet du cycle de vente. Et c'est pour ça que mon taux de
téléphone est bas globalement, mais bien plus élevé chez les leads convertis. »

---

## Slide 5 — La démarche  *(≈ 1 min)*

« Ma démarche s'est faite en quatre étapes.

D'abord un **profilage** : je regarde l'état initial — volumétrie, valeurs
manquantes, doublons, types de données. Ensuite le **nettoyage** : je normalise
les emails, je remets les téléphones au format international E.164, je parse les
dates, je crée des clés propres pour comparer. Troisième étape, je construis une
**table analytique** unique, en joignant les leads, les contacts, les campagnes
et les activités. Et enfin le **scoring** : je calcule un score de qualité sur
100, un statut *campaign-ready*, et je génère un journal de toutes les anomalies.

Le message, c'est que la donnée brute n'est pas juste affichée : elle est
**auditée puis transformée**. »

---

## Slide 6 — Le score qualité  *(≈ 1 min)*

« Voici le cœur de la méthode : mon score de qualité sur 100.

Chaque critère rapporte des points. Un email valide, c'est 25 points — c'est le
plus important, parce que sans email, pas de campagne. Un téléphone valide, 15
points. Puis une série de critères à 10 points : un contact exploitable, une
source renseignée, une entreprise connue, une campagne ou une activité associée,
une date cohérente, et l'absence de doublon.

Ce score se traduit ensuite en quatre niveaux, à droite : Excellent au-dessus de
80, Correct au-dessus de 60, À corriger, et Critique. Et un lead est déclaré
*campaign-ready* s'il a un email valide, pas de doublon, une source, et un score
d'au moins 60. L'avantage, c'est qu'on passe d'une multitude d'indicateurs
techniques à **un seul chiffre lisible par tout le monde**. »

---

## Slide 7 — Technologies  *(≈ 45 s)*

« Rapidement, la stack technique. Côté analyse, tout est en **Python**, avec
**pandas** et **NumPy** pour le nettoyage et les calculs, et la librairie
**phonenumbers** pour valider les téléphones au format international.

Côté visualisation, le dashboard est construit avec **Streamlit** pour
l'application web et **Plotly** pour les graphiques interactifs ; l'analyse,
elle, vit dans un **notebook Jupyter**, ce qui rend tout le pipeline
reproductible. J'avais aussi envisagé Tableau Public, que je mentionne en
alternative. »

**[Transition]** « Passons maintenant au dashboard lui-même. »

---

## Slide 8 — Vue Direction  *(≈ 1 min)*

« Le dashboard est organisé en quatre vues. La première, c'est la **vue
Direction** : la réponse en un coup d'œil.

Le graphique en anneau montre la répartition des leads par niveau de qualité :
la grande majorité est en « Correct », avec une part en « Excellent », et une
minorité « À corriger ».

Et le message clé, à droite : **près de 94 % des leads sont exploitables** pour
une campagne, avec un score moyen de 75 sur 100. On a **zéro lead critique et
zéro doublon exact** : la base est saine sur l'essentiel. C'est une bonne
nouvelle pour la direction — mais ça ne veut pas dire qu'il n'y a rien à
faire. »

---

## Slide 9 — Sources  *(≈ 1 min)*

« La deuxième vue répond à une question d'investissement : **quelles sources nous
amènent les leads les plus fiables ?**

Sur ce graphique, je classe les sources par score de qualité moyen. On voit en
haut les sources les plus solides — le référencement naturel, les webinaires,
les recommandations de partenaires. Et en bas, les plus fragiles, comme le
*direct mail* ou l'*outbound* à froid.

Concrètement, ça outille trois décisions : **renforcer** les budgets sur les
sources fiables, **corriger les formulaires** des sources faibles pour récupérer
de meilleures données, et **surveiller** celles qui font du volume mais avec une
qualité moyenne. »

---

## Slide 10 — Actions correctives  *(≈ 1 min)*

« La troisième vue, c'est la plus opérationnelle : **que faut-il corriger en
priorité ?**

Je classe les anomalies par type. Et le constat est clair : la **priorité numéro
un, c'est le téléphone**, avec près de 6 900 cas à enrichir. Viennent ensuite les
doublons probables à vérifier, puis environ 500 emails invalides à corriger
avant tout emailing.

Et l'élément que je trouve le plus utile : cette liste est **filtrable et
exportable en CSV** directement depuis le dashboard. Autrement dit, l'équipe data
récupère une véritable *to-do list* priorisée, prête à être traitée. »

---

## Slide 11 — Décisions  *(≈ 45 s)*

« Si je résume en quatre décisions actionnables : sur l'**acquisition**, on
réinvestit sur les bonnes sources et on revoit les formulaires des mauvaises. Sur
l'**enrichissement**, on lance une campagne pour récupérer les téléphones
manquants. Sur la **délivrabilité**, on nettoie les emails invalides avant
d'envoyer quoi que ce soit. Et sur l'**hygiène du CRM**, on traite les doublons
probables.

L'objectif du dashboard, c'est vraiment ça : produire des décisions, pas
seulement des chiffres. »

---

## Slide 12 — Rigueur & limites  *(≈ 1 min)*

« Un mot sur la rigueur de l'analyse, parce que je tiens à être honnête.

En construisant le projet, j'ai identifié et **corrigé trois bugs dans mon
pipeline** qui faussaient complètement les résultats : un calcul qui marquait
100 % des leads comme doublons, un téléphone valide à 0 %, et une jointure de
campagnes vide. Les corriger a été essentiel pour que les KPI veuillent dire
quelque chose.

Et j'assume aussi les limites : les données sont **synthétiques**, donc avec peu
d'entreprises différentes et pas de vrais doublons exacts ; l'enrichissement
téléphone se limite aux comptes convertis ; et le « doublon probable » par
nom et entreprise reste un signal indicatif, à revoir manuellement. »

---

## Slide 13 — Conclusion  *(≈ 45 s)*

« Pour conclure, la réponse à ma question de départ : **oui, le CRM est
globalement fiable, à 75 sur 100 — mais le téléphone est clairement le chantier
prioritaire.**

Au final, je livre trois choses : un outil de **surveillance continue** de la
qualité de la base, une **to-do list priorisée** pour l'équipe data, et des
**décisions outillées** sur l'acquisition et l'hygiène du CRM.

Je vous remercie de votre attention, et je suis à votre disposition pour vos
questions. »

---

## Réponses prêtes pour les questions fréquentes

- **« Pourquoi seulement 14 % de téléphones valides ? »**
  « Parce que le téléphone vient des contacts, qui ne sont rattachés qu'après
  conversion. Chez les leads convertis, on monte à 73 %. C'est structurel, pas un
  problème de nettoyage. »

- **« Pourquoi zéro doublon ? »**
  « Zéro doublon *exact* sur l'email — chaque email de lead est unique. J'ai
  volontairement écarté le critère nom + entreprise du signal dur, parce qu'avec
  une vingtaine d'entreprises seulement, il marquait presque tout le monde. Je le
  garde quand même affiché, mais comme indicatif à vérifier. »

- **« Le score de qualité n'est-il pas arbitraire ? »**
  « La pondération est un choix, oui, mais il est assumé et documenté dans ma
  note méthodologique. Elle est entièrement paramétrable : on peut l'ajuster
  selon les priorités de l'entreprise. »

- **« Pourquoi Streamlit plutôt que Tableau ? »**
  « Pour rester de bout en bout en Python et garder un pipeline reproductible :
  le notebook produit les données, et le même environnement sert le dashboard.
  Tableau restait une alternative tout à fait possible. »

---

## Repères de timing

| Bloc | Durée cible |
|---|---|
| Slides 1–6 (contexte, méthode) | ~5 min 30 |
| Slide 7 (techno) | ~45 s |
| Slides 8–11 (démo dashboard) | ~3 min 45 |
| Slides 12–13 (rigueur, conclusion) | ~1 min 45 |
| **Total exposé** | **~11–12 min** |
| Questions | 3–5 min |

> Astuce : à la slide 8, **bascule sur le dashboard Streamlit en live** et
> montre un filtre (une source ou une période) avant de revenir aux slides.
