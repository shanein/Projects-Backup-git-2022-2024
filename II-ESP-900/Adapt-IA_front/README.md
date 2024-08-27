# Adapt-IA

# PRODUCTION SERVER

# Pour lancer la version "production" en visant l'api en local:

docker compose --env-file ./.prod.local.env -f docker-compose.prod.yml up --build

# Pour lancer la version "production" en visant l'api en deployée:

docker compose --env-file ./.prod.env -f docker-compose.prod.yml up --build

<!-- ------------------------------------------------------------- -->

# DEVELOPMENT SERVER

# Pour lancer la version "developpement" en visant l'api en local :

docker compose --env-file ./.dev.local.env -f docker-compose.dev.yml up --build

# Pour lancer la version "developpement" en visant l'api en deployée :

docker compose --env-file ./.dev.env -f docker-compose.dev.yml up --build

<!-- ------------------------------------------------------------- -->

# ERROS & FIXES

# Si vous avez des problèmes avec les builds ou images docker, vous pouvez les résoudre avec les commandes suivantes :

docker compose --env-file ./.dev.local.env -f docker-compose.dev.yml build --no-cache && docker compose --env-file ./.dev.local.env -f docker-compose.dev.yml up --build --force-recreate

# ou

docker compose --env-file ./.prod.local.env -f docker-compose.prod.yml build --no-cache && docker compose --env-file ./.prod.local.env -f docker-compose.prod.yml up --build
