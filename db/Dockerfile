# Imagen de MariaDB
FROM mariadb:11.4

# Variables de entorno 
ENV MARIADB_ROOT_PASSWORD=rootpass \
    MARIADB_DATABASE=weatherdb \
    MARIADB_USER=weather \
    MARIADB_PASSWORD=weatherpass

# Copiar script SQL 
COPY init.sql /docker-entrypoint-initdb.d/
