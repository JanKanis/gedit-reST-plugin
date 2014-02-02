Documentation de reStructuredText plugin
========================================

Cette documentation est très restreinte, merci de patienter qu'elle s'étoffe 
un peu.

Dépendances
------------

- Python >= 2.5
- Pygments [http://pygments.org/]
- Docutils [http://docutils.sourceforge.net/]
- OdtWriter [http://www.rexx.com/~dkuhlman/odtwriter.html]

Installation
------------

Placez le fichier ``reSt.gedit-plugin`` dans votre dossier plugins de Gedit.
Le mien se situe ici par exemple :
/home/kib/.gnome2/gedit/plugins

Ensuite, copier /coller le dossier nommé ``reStPlugin`` dans ce même 
répertoire.

Les fichiers Readme.rst et Readme.odt ne sont là que pour vous aider, vous 
pourrez ensuite les placer à la poubelle si le coeur vous en dit !

L'arborescence devrait donc être la suivante : ::

    .../plugins/
            reSt.gedit-plugin
            reStPlugin/
                __init__.py
                makeTable.py
                etc.

Utilisation
-----------

Activez le plugin via Editions/Préférences onglet Plugins et cochez 
``reStructuredText plugin``.

Le plugin est actif, vous devriez obtenir un nouvel onglet dans votre panneau 
inférieur nommé ``reSt Preview``.

Raccourcis
##########

Ctrl+Maj+R permet d'afficher le contenu de votre fichier reSt (extension .rst) 
dans le nouveau panneau. Si une selection est active, la conversion ne se fera
que sur celle-ci, sinon c'est tout le document qui est pris en charge.

Menu
####

Le menu ``Outils`` dispose maintenant de plusieurs options :

- ``reSt Preview`` a déjà été détaillé précédemment;
- ``Create table`` permet de réaliser des tableaux simples.

  Exemple : Entrer ces deux lignes, sélectionnez-les et activez ``Create table``
  
  un,deux,trois
  
  premiere,seconde,troisieme
  
  Cela donne :

============  ===========  =============
 un           deux         trois    
============  ===========  =============
premiere      seconde      troisieme  
============  ===========  =============

- ``Paste Code`` permet de copier/coller des codes sources façon Pygments.
  Selectionnez juste du code à copier, et utilisez cette macro. Vous devrez 
  ensuite ajuster le langage vous même.

- ``--> HTML``, ``--> LaTeX``, ``--> OpenOffice``: permettent respectivement
  un export de votre document dans ces formats respectifs. L'export à lieu 
  dans le même dossier que votre document initial. Des feuilles de style sont
  fournies, ce sera à vous de les adapter à vos besoins.

En espérant que ce petit plugin vous aidera, n'hésitez-pas à me contacter :

Kib.
