# SoftDesk, API sécurisée de suivi de problèmes techniques d'applications collaboratives


## Prérequis

-Python 3.x

-pip (pour installer les dépendances)

## Installation

1. Ouvrez un terminal de commande et naviguez jusqu'au chemin où vous désirez cloner le répertoire.

2. Tapez la commande suivante : git clone https://github.com/Clement-Mchar/P10_Clement_Mchar_Creez_Une_API_Securisee_RESTFul_En_Utilisant_Django_REST_05_04_2024

3. Placez-vous dans le dossier "SoftDesk".

4. Exécutez la commande "pip install -r requirements.txt" pour installer les dépendances nécessaires au fonctionnement de l'API.

5. Exécutez la commande "pipenv shell" pour créer et activer votre environnement virtuel.

## Utilisation

1. Lancez Postman pour utiliser les différents endpoints de l'API :
   Vous pouvez, grâce à django extensions, afficher la liste des endpoints grâce à la commande python manage.py show_urls.
   Tous les endpoints nécéssitent un token d'authentification JWT, excepté celui de création de compte et d'obtention/rafraîchissement dudit JWT.
   
2. Pour pouvoir utiliser l'API, entrez la commande python manage.py runserver dans le terminal de commandes afin d'activer le serveur local.
