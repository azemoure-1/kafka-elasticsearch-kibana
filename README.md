# Projet : Système de Recommandation de Films en Temps Réel pour Jay-Zz Entertainment

## Présenté par AZEMOUR Amine

## Résumé

Ce projet vise à améliorer l'expérience utilisateur sur la plateforme de streaming de Jay-Zz Entertainment en mettant en place un système de recommandation de films en temps réel. La solution intègre la stack EK (Elasticsearch, Kafka) et une API de recommandation personnalisée. Les principales étapes incluent la configuration de Kafka, le traitement des données avec SparkStreaming, la modélisation et le stockage dans Elasticsearch, le développement de l'API de recommandation, la visualisation des données avec Kibana, et une approche robuste de gouvernance des données.

## Objectifs du Projet

Le projet a pour objectif de créer un système de recommandation de films en temps réel utilisant des technologies Big Data pour fournir des recommandations personnalisées aux utilisateurs de la plateforme de streaming Jay-Zz Entertainment. L'ajout d'une couche de gouvernance des données garantit la qualité, la confidentialité, et la conformité des données.

## Compétences Mises en Œuvre

Le projet met en œuvre diverses compétences, notamment :

- Configuration et gestion de clusters Kafka.
- Utilisation de SparkStreaming pour le traitement en temps réel des données.
- Modélisation et stockage efficace des données dans Elasticsearch.
- Développement d'une API REST avec Flask.
- Visualisation des données avec Kibana.
- Gestion de projet avec Git.
- Pratiques de gouvernance des données.

## Étapes du Projet

### Problèmes Rencontrés

- **Installation et Compatibilité :** La configuration initiale de Kafka a rencontré des défis, notamment en ce qui concerne la compatibilité des versions avec d'autres composants de la stack. Des ajustements ont été nécessaires pour garantir une intégration fluide entre Kafka, SparkStreaming, et Elasticsearch.

### Configuration de Kafka

- Mise en place d'un cluster Kafka.
- Configuration des producteurs pour l'envoi des données d'interactions utilisateur vers des topics spécifiques.

### Traitement avec SparkStreaming

- Création de pipelines pour consommer les données de Kafka.
- Application de transformations, telles que l'enrichissement des données et la normalisation.

### Modélisation et Stockage dans Elasticsearch

- Conception d'indices et de modèles de données pour un stockage optimisé des informations des films et des utilisateurs.

![4](https://github.com/azemoure-1/kafka-elasticsearch-kibana/assets/113553607/1cb7a11c-a290-4a66-857f-9a4c46028b97)


### Développement de l'API de Recommandation

- Programmation d'une API REST avec Flask, interagissant avec Elasticsearch pour récupérer et servir les recommandations.

![3](https://github.com/azemoure-1/kafka-elasticsearch-kibana/assets/113553607/2b7f91b1-9260-4067-b0ac-e738094c4efb)



### Gouvernance des Données


Dans le cadre de ce flux de traitement de données, une attention particulière a été portée à la gouvernance des données, en conformité avec le Règlement Général sur la Protection des Données (RGPD). Des pratiques rigoureuses de gouvernance des données ont été intégrées pour garantir la qualité, la confidentialité et la conformité des informations extraites de l'API The Movie Database. Les données sont collectées de manière sécurisée, avec la prise en compte des principes de minimisation et de pertinence, afin de limiter la quantité de données traitées et de s'assurer qu'elles sont directement liées à l'objectif du traitement. De plus, des mesures de sécurité, telles que l'utilisation de clés d'API, ont été mises en place pour protéger l'accès aux données sensibles. En outre, le processus intègre des mécanismes de contrôle de la qualité des données pour garantir leur exactitude avant l'envoi aux systèmes ultérieurs, et des étapes de pseudonymisation ont été appliquées lorsque cela est approprié. Ces pratiques reflètent l'engagement envers la protection des données personnelles et la conformité aux normes éthiques et juridiques en vigueur.

### Visualisation avec Kibana

- Création de tableaux de bord pour des visualisations significatives, telles que la répartition des films par date de sortie, les films populaires, etc.

![2](https://github.com/azemoure-1/kafka-elasticsearch-kibana/assets/113553607/e6a12478-d1ef-4722-b79e-30e5c72e4738)


## Complications et Solutions

Au cours du projet, des difficultés ont été rencontrées, principalement liées à l'installation initiale et à la gestion de la compatibilité des versions entre les différents composants de la stack. Cependant, ces obstacles ont été surmontés grâce à une collaboration étroite de l'équipe, à des ajustements minutieux des configurations, et à des recherches approfondies pour résoudre les problèmes spécifiques.

## Conclusion

Malgré les défis initiaux, le système de recommandation en temps réel représente une avancée significative pour Jay-Zz Entertainment. Il offre une expérience utilisateur améliorée tout en répondant aux exigences de qualité et de conformité des données. Ce projet souligne l'importance de la résilience et de la collaboration dans le développement de solutions Big Data complexes.



*Fin du README*
