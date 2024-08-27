# Documentation du Backend pour le Projet de WebApp de Gestion de Mise en Relation

## 1. Introduction

-   **Objectif du Projet**: Construire un backend pour une WebApp de mise en relation entre des annonceurs et des propriétaires de bornes. Intégration d'intelligences artificielles pour adapter les vidéos diffusées en temps réel basées sur la détection et la classification d'humains (homme, femme, âge) et choix des vidéos en temps réel.

## 2. Documentation du Backend

-   **Technologies Utilisées**: Python avec FastAPI, SQLAlchemy, PostgreSQL.
-   **Environnement de Développement**:
    -   Fonctionnement dans des conteneurs Docker.
    -   Commande pour lancer en mode développement ou production: `docker-compose -f docker-compose.dev.yml up --build` ou `docker-compose -f docker-compose.prod.yml up --build`.
-   **API et Base de Données**:
    -   Diagramme des tables disponible en temps réel.
    -   Documentation de l'API accessible via Swagger.

## 3. Utilisation de GitHub

-   **Configuration de Git**: Clonage classique du dépôt.
-   **Workflow Git**:
    -   Travail sur des branches spécifiques (ex. `feature/nomdelafeature`, `fix/choseafix`).
    -   Utilisation de `pre-commit` pour s'assurer que le code est conforme aux normes (linter Python Black).
    -   Création de PR vers la branche `dev`, avec des workflows GitHub pour tester la fonctionnalité.
    -   Importance de la clarté dans les noms et descriptions de PR, ainsi que de commenter le code.

## 4. Tests et Normes de Code

-   **Linter**: Utilisation de Python Black pour vérifier la conformité du code.
-   **Tests**:
    -   Exécution de tests unitaires.
    -   Nécessité d'un certain niveau de couverture de code pour pouvoir pousser les modifications.
-   **Intégration Continue**:
    -   Mise en place dans GitHub.
    -   Déploiement automatique sur un serveur Ubuntu.

## 5. Gestion des Pull Requests (PR) et des Tâches

-   **Examen de PR**:
    -   Les PR sont examinées par le lead backend (vous) ou le lead frontend (Richard).
    -   Si une PR est approuvée, le ticket associé est marqué comme terminé.
-   **Outil de Gestion de Tâches**:
    -   Utilisation de Trello pour le suivi des tickets.
