# Meghan de Biolley : site web

Site statique (HTML/CSS) hébergé sur GitHub Pages. Français à la racine, anglais dans `/en`.

## Photos

Les photos sont dans `images/`. Pour en remplacer une, déposez un nouveau fichier avec **exactement** le même nom (JPG, ~1600 px max). Si un fichier manque, un emplacement beige « MB » s'affiche à sa place.

| Fichier | Où |
|---|---|
| `hero.jpg` | Accueil, en haut |
| `portrait.jpg` | Accueil (« Un mot sur moi ») + À propos |
| `espace.mp4` + `espace-poster.jpg` | À propos, petite vidéo de l'espace de soin |
| `en-seance-1.jpg`, `en-seance-2.jpg`, `en-seance-3.jpg` | Accueil, galerie |
| `sonotherapie.jpg` | Accueil, bloc ateliers et entreprises |
| `soin-visage.jpg`, `massage-drainant.jpg`, `massage-relaxant.jpg`, `corps-visage.jpg`, `duo-corps-visage.jpg`, `visage-sonotherapie.jpg`, `corps-sonotherapie.jpg` | Une par soin |
| `entreprises.jpg`, `atelier-sonotherapie.jpg`, `atelier-auto-massage.jpg`, `eclosion.jpg` | Page Ateliers |
| `bon-cadeau.jpg` | Page Bons cadeaux |
| `og-image.jpg` | Aperçu quand le lien est partagé (WhatsApp, Facebook…), 1200×630 |

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
