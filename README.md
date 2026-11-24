# Meghan de Biolley : site web

Site statique (HTML/CSS) hébergé sur GitHub Pages. Français à la racine, anglais dans `/en`.

## Ajouter les photos

Déposez les fichiers dans `images/` avec **exactement** ces noms (JPG, ~1600 px de large max).
Tant qu'un fichier manque, un emplacement beige « MB » s'affiche à sa place.

| Fichier | Où | Format conseillé |
|---|---|---|
| `hero.jpg` | Accueil, en haut | portrait (4:5) |
| `portrait.jpg` | Accueil + À propos | portrait (4:5) |
| `espace.jpg` | À propos (l'espace de soin) | paysage (4:3) |
| `sonotherapie.jpg` | Accueil (bols tibétains) | paysage (4:3) |
| `en-seance-1.jpg`, `en-seance-2.jpg`, `en-seance-3.jpg` | Accueil, galerie « en séance » | portrait (3:4) |
| `soin-visage.jpg`, `massage-drainant.jpg`, `massage-relaxant.jpg`, `corps-visage.jpg`, `duo-corps-visage.jpg`, `visage-sonotherapie.jpg`, `corps-sonotherapie.jpg` | Une par soin | portrait (4:5) |
| `atelier-sonotherapie.jpg`, `atelier-auto-massage.jpg` | Page Ateliers | portrait (4:5) |
| `eclosion.jpg` | Page Ateliers, retraites Éclosion | paysage (4:3) |
| `bon-cadeau.jpg` | Page Bons cadeaux + Accueil (photo du bon) | portrait (4:5) |
| `og-image.jpg` | Aperçu quand le lien est partagé (WhatsApp, Facebook…) | 1200×630 |

## Contenu encore à compléter

Cherchez `class="todo"` dans les fichiers HTML : numéro BCE (`mentions-legales.html`, `en/legal-notice.html`). Supprimez la classe `todo` une fois le texte remplacé.

## Modifier le contenu (prix, textes, avis)

Toutes les pages HTML sont générées par `_outils/build.py`, qui contient les textes FR et EN, les soins et prix (`SOINS`), les avis (`REVIEWS`) et la FAQ.

1. Modifiez le texte dans `_outils/build.py`.
2. Depuis la racine du dépôt, lancez :

   ```bash
   python3 _outils/build.py
   ```

3. Committez les fichiers `.html` régénérés.

Attention : une modification faite directement dans un fichier `.html` sera écrasée au prochain lancement du script. Choisissez l'une ou l'autre méthode.

## Questions à poser à Meghan

- Ateliers et séances de groupe : combien de temps durent-ils (sound healing, auto-massage, ateliers skincare) ? Y a-t-il un nombre minimum de participants ?
- Photos : certaines photos du site ont-elles été prises par un ou une photographe ? Si oui, qui, et faut-il créditer son nom (mentions légales ou sous la photo) ?
