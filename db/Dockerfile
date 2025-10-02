# Imagen base oficial de MariaDB
FROM mariadb:11.4

# Variables de entorno por defecto
ENV MARIADB_ROOT_PASSWORD=rootpass \
    MARIADB_DATABASE=weatherdb \
    MARIADB_USER=weather \
    MARIADB_PASSWORD=weatherpass

# Copiar script SQL de inicialización
COPY init.sql /docker-entrypoint-initdb.d/
